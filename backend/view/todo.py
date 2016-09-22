
import config
from model.todo import Todo
from lib import markdown
from view import route, AjaxView, AjaxLoginView, url_for


@route('/api/todo/new', name='todo_new')
class TopicNew(AjaxView):
    def post(self):
        title = self.get_argument('title', '').strip()
        content = self.get_argument('content', '').strip()
        if title and config.TITLE_LENGTH_MIN <= len(title) <= config.TITLE_LENGTH_MAX:
            t = Todo.new(title, self.current_user() or 0, content)
            self.finish({'code': 0, 'topic': {'id': t.id}})
        else:
            # 非标准提交
            self.finish({'code': -1})


@route('/api/todo/(\d+)', name='todo')
class TopicPage(AjaxView):
    def get(self, todo_id):
        todo = Todo.get_by_pk(todo_id)
        if todo:
            todo = todo.to_dict()
            todo['content'] = markdown.render(todo['content'])
            self.finish({'code': 0, 'data': todo})
        else:
            self.finish({'code': -1})


@route('/api/get_all', name='get_all')
class Recent(AjaxView):
    def get(self):
        page = self.get_argument('p', '1')
        count, query = Todo.get_list()
        self.finish({'code': 0, 'data': list(query)})
