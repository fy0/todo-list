# coding:utf-8

from view import route, url_for, AjaxView


@route('/', name='index')
class Index(AjaxView):
    def get(self):
        self.finish({'code': 0, 'status': 'ready'})

    def post(self):
        self.finish({'code': 0, 'status': 'ready'})
