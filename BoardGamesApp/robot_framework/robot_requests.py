class RobotRequests:
    """Класс родитель, для работы с запросами"""
    @staticmethod
    def parse_str_data(data: str):
        """Метод класса, который парсит строку, кладя данные в словарь"""
        data_dict = dict()
        if data:
            data = data.split('&')
            for key_value in data:
                data_dict[key_value.split('=')[0]] = key_value.split('=')[1]
        return data_dict


class GetRequest(RobotRequests):
    """Класс для работы с get запросами"""
    def get_request_params(self, environ):
        """Метод класса для получения параметров запроса в виде словаря"""
        query_str = environ['QUERY_STRING']
        return self.parse_str_data(query_str)


class PostRequest(RobotRequests):
    """Класс для работы с post запросами"""
    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        """Метод класса для проверки содержимого post запроса"""
        content_len_data = int(environ['CONTENT_LENGTH'])
        if content_len_data == 0:
            return b''
        else:
            return environ['wsgi.input'].read(content_len_data)

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """Метод класса для декодирования и сборки данных из post запроса"""
        if data:
            bytes_decode = data.decode(encoding='utf-8')
            return self.parse_str_data(bytes_decode)

    def get_request_params(self, environ):
        """Метод класса для получения параметров запроса в виде словаря"""
        data = self.get_wsgi_input_data(environ)
        return self.parse_wsgi_input_data(data)


if __name__ == '__main__':
    str_parse = RobotRequests.parse_str_data('id=2&category=12')
    print(str_parse)

    bytes_parse = PostRequest().parse_wsgi_input_data(b'id=5&category=13')
    print(bytes_parse)

    bytes_parse = PostRequest().parse_wsgi_input_data(b'')
    print(bytes_parse)
