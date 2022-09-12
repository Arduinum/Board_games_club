from quopri import decodestring
from robot_framework.robot_requests import RobotRequests
from json import dump


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

        request = dict()
        method_now = environ['REQUEST_METHOD']
        request['method_now'] = method_now

        if method_now == 'POST':
            data_post = RobotRequests().get_request_params(environ, 'POST')
            request['data_post'] = self.decode_value(data_post)
            if request["data_post"]:
                self.saver_form_data(request['data_post'])
                print(f'На сервер пришёл POST-запрос - {request["data_post"]}')
        if method_now == 'GET':
            data_get = RobotRequests().get_request_params(environ, 'GET')
            request['data_get'] = self.decode_value(data_get)
            if request['data_get']:
                print(f'На сервер пришли GET-параметры - {request["data_get"]}')

        if path in self.list_routes:
            view = self.list_routes[path]
        else:
            view = PageError404()

        for front in self.list_fronts:
            front(request)

        code, body = view(request)

        response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """Метод класса для правильного декодирования в utf-8"""
        updated_data = dict()
        for key, value in data.items():
            value = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            value_decode_str = decodestring(value).decode('UTF-8')
            updated_data[key] = value_decode_str
        return updated_data

    @staticmethod
    def saver_form_data(data):
        """Метод класса для сохранения данных формы регистрации на игру в json документ"""
        with open(f'form_register_{data["name"]}.json', 'w', encoding='utf-8') as file:
            dump(data, file, indent=4, ensure_ascii=False)
