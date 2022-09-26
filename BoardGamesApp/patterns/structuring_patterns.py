from time import time


class AppendRoute:
    """Класс для добавлнения url (структурный паттерн декоратор)"""
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """Класс для замеров времени выполнения методов и функций (структурный паттерн декоратор)"""
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def time_speed(method):
            def timed(*args, **kwargs):
                time_start = time()
                meter_method = method(*args, **kwargs)
                time_end = time()
                delta = time_end - time_start

                print(f'debug --- {self.name} скорость выполнения {delta:2.2f} microseconds')
                return meter_method
            return timed
        return time_speed(cls)


if __name__ == '__main__':
    routes_test = dict()

    class Test:
        @Debug(name='Test')
        def test_list_creator(self):
            list_result = list()
            for num in range(10000000):
                list_result.append(num * 33)
            return list_result

    @AppendRoute(routes=routes_test, url='/test/')
    class Test2:
        def __call__(self):
            return 'test2'


    Test().test_list_creator()
    test2 = Test2
    print(routes_test)
