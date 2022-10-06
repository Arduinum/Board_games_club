from json import dumps, loads
from pprint import pprint
from BoardGamesApp.robot_framework.templator import render


class Observer:
    """Класс наблюдатель (паттерн наблюдатель)"""
    def update_list_gamers(self, subject):
        """Метод класса для обновления списка игроков"""
        pass


class Subject:
    """Класс субьект, за которым наблюдают"""
    def __init__(self):
        self.observers = list()

    def inform(self):
        """Метод класа для информирования об изменениях"""
        for subject in self.observers:
            subject.update(self)


class TelegramNotifier(Observer):
    """Класс для оповещения в мессенджере телеграм"""
    @staticmethod
    def update(subject):
        """Метод класса дял информирования в Телеграм"""
        print(f'Telegram ---- присоединился игрок - {subject.gamers[-1].name}')


class EmailNotifier(Observer):
    """Класс для оповещения по электронной почте"""
    @staticmethod
    def update(subject):
        """Метод класса для информирования по электронной почте"""
        print(f'Email ---- присоединился игрок - {subject.gamers[-1].name}')


class BaseSerializer:
    """Базовый класс для сериализации json данных"""
    def __init__(self, data):
        self.data = data

    def coding_data(self):
        """Метод класса для кодирования данных json"""
        return dumps(self.data)

    @staticmethod
    def decode_data(data):
        """Метод класса для декодирования данных json"""
        return loads(data)


class TemplateView:
    """Класс для работы с шаблоном (поведенческий паттерн шаблонный метод)"""
    template_name = 'template.html'

    def get_context_data(self):
        """Метод класса для возврата контекста"""
        return dict()

    def render_template(self):
        """Метод класса для рендеринга шаблона с контекстом"""
        context = self.get_context_data()
        return '200 OK', render(self.template_name, **context)

    def __call__(self, request):
        return self.render_template()


class ListView(TemplateView):
    """Класс для работы с шаблоном где список данных"""
    queryset = list()
    template_name = 'list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        """Метод класса для получения списка данных"""
        return self.queryset

    def get_context_data(self):
        """Метод класса для возврата контекста"""
        queryset = self.get_queryset()
        context = {self.context_object_name: queryset}
        return context


class CreateView(TemplateView):
    """Класс для работы с шаблоном создания объекта"""
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        """Метод класса для возврата данных запроса"""
        return request['data_post']

    def create_object(self, data):
        """Метод класса для создания объекта"""
        pass

    def __call__(self, request):
        if request['method_now'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return self.render_template()
        else:
            return super().__call__(request)


class ConsoleWriter:
    """Класс для вывода информации в консоль (поведенческий паттерн - шаблон стратегия)"""
    @staticmethod
    def writer(text):
        """Метод класса для вывода данных в консоль"""
        pprint(f'logger console ---- {text}')


class FileWriter:
    """Класс для записи данных в файл"""
    def __init__(self):
        self.file_name = 'log_file'

    def writer(self, text):
        """Метод класса для записи данных в файл"""
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'logger file ---- {text}\n')
