class PageError404:
    """Класс, отвечающий за информацию о не найденой странице"""
    def __call__(self, request):
        return '404 ERROR', '404 Page Not Found'


class RobotFramework:
    """Класс, отвечающий за работу фреймворка"""

    def __init__(self, routes, fronts):
        self.list_routes = routes
        self.list_fronts = fronts

    def __call__(self, environ, response):
        path = environ['PATH_INFO']

        if path[-1] != '/':
            path = f'{path}/'

        if path in self.list_routes:
            view = self.list_routes[path]
        else:
            view = PageError404()
        request = {}

        for front in self.list_fronts:
            front(request)

        code, body = view(request)
        # print(body)
        response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
