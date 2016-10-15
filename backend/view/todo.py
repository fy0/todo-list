import json

import config
from model.todo import Todo
from lib import markdown
from view import route, AjaxView, AjaxLoginView, url_for


@route('/api/todo/add', name='todo_add')
class TodoAdd(AjaxLoginView):
    def post(self):
        title = self.get_argument('title', '').strip()
        content = self.get_argument('content', '').strip()
        if title and config.TITLE_LENGTH_MIN <= len(title) <= config.TITLE_LENGTH_MAX:
            t = Todo.new(title, self.current_user() or 0, content)
            self.finish({'code': 0, 'todo': t.to_dict()})
        else:
            # 非标准提交
            self.finish({'code': -1})


@route('/api/todo/remove', name='todo_remove')
class TodoRemove(AjaxLoginView):
    def post(self):
        todo_id = self.get_argument('todo_id')
        if todo_id:
            todo = Todo.get_by_pk(todo_id)
            if todo and todo.can_edit(self.current_user()):
                todo.remove()
                self.finish({'code': 0})
            else:
                self.finish({'code': -2})
        else:
            self.finish({'code': -1})


@route('/api/todo/batch_save', name='todo_batch_save')
class TodoBatchSave(AjaxLoginView):
    def post(self):
        todo_text = self.get_argument('todo_lst', '[]')
        todo_lst = json.loads(todo_text)
        user = self.current_user()
        mods = []
        for i in todo_lst:
            t = Todo.get_by_pk(i['id'])
            #if t.can_edit(user):  # 姑且不对权限做限制
            if t.edit(i, user):
                mods.append(t.to_dict())
        self.finish({'code': 0, 'modified': mods})


@route('/api/todo/(\d+)', name='todo')
class TodoInfo(AjaxView):
    def get(self, todo_id):
        todo = Todo.get_by_pk(todo_id)
        if todo:
            todo = todo.to_dict()
            todo['content'] = markdown.render(todo['content'])
            self.finish({'code': 0, 'data': todo})
        else:
            self.finish({'code': -1})


@route('/api/get_all', name='get_all')
class TodoGetAll(AjaxView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Todo.get_list()
        self.finish({'code': 0, 'data': list(map(Todo.to_dict, query))})
