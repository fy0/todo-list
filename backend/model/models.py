# coding:utf-8

from model import db
from model.user import User
from model.todo import Todo

db.connect()
db.create_tables([User, Todo], safe=True)
