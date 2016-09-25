# coding:utf-8
import time
from peewee import *
from model import db, BaseModel
from model.user import User
from lib.state_obj import StateObject


class TODO_STATE(StateObject):
    DEL = 0
    HIDE = 10
    NORMAL = 50
    DONE = 80

    txt = {DEL: "删除", HIDE: "隐藏", NORMAL:"正常", DONE: '完成'}

TODO_STATE.init()


class Todo(BaseModel):
    title = CharField(index=True, max_length=50)
    user = ForeignKeyField(User, index=True)
    time = BigIntegerField(index=True)
    state = IntegerField(default=TODO_STATE.NORMAL, index=True)

    edit_time = BigIntegerField(index=True, null=True)
    last_edit_user = ForeignKeyField(User, related_name="last_edit_user_id", null=True)
    content = CharField(max_length=5000)

    priority = IntegerField(default=0) # 紧急、暂缓、长期
    category = IntegerField(default=0) # 后端、前端、TODO
    partner1 = ForeignKeyField(User, related_name="fk_partner1", null=True) # 最多允许三个人从事同一任务
    partner2 = ForeignKeyField(User, related_name="fk_partner2", null=True)
    partner3 = ForeignKeyField(User, related_name="fk_partner3", null=True)

    sticky_weight = IntegerField(index=True, default=0)  # 置顶权重
    weight = IntegerField(index=True, default=0) # 排序权值，越大越靠前，默认权重与id相同

    class Meta:
        db_table = 'todo'

    def can_edit(self, user):
        if self.user == user:
            return True

    def edit(self, data, user):
        if 'title' in data:
            self.title = data['title']
        if 'content' in data:
            self.content = data['content']
        self.last_edit_user = user
        self.edit_time = int(time.time())
        self.save()

    @classmethod
    def new(cls, title, user, content=None):
        with db.atomic():
            ret = cls.create(title=title, user=user, time=int(time.time()), content=content)
            ret.weight = ret.id
            ret.save()
        return ret

    @classmethod
    def get_list(cls):
        q = cls.select().where(cls.state>TODO_STATE.HIDE).order_by(cls.weight.desc(), cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_order_by_time(cls, state=-1):
        if state == -1:
            q = cls.select().order_by(cls.time.desc())
        else:
            q = cls.select().where(cls.state==TODO_STATE.HIDE).order_by(cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_by_board(cls, board):
        q = cls.select().where(cls.board==board, cls.state>TODO_STATE.HIDE)\
                .order_by(cls.sticky_weight.desc(), cls.weight.desc(), cls.time.desc())
        return q.count(), q

    @classmethod
    def get_list_by_user(cls, user):
        q = cls.select().where(cls.user==user, cls.state>TODO_STATE.HIDE)
        return q.count(), q
