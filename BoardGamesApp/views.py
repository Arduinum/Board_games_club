from robot_framework.templator import render
from data import games


class Index:
    """Класс вьюха главной страницы"""
    def __call__(self, request):
        return '200 OK', render('index.html')


class Contact:
    """Класс вьюха страницы контактов"""
    def __call__(self, request):
        return '200 OK', render('contact.html')


class Events:
    """Класс вьюха страницы расписание мероприятий"""
    def __call__(self, request):
        return '200 OK', render('events.html', date=request.get('date', None), data=[games])


class AboutUs:
    """Класс вьюха страницы о нас"""
    def __call__(self, request):
        return '200 OK', render('about_us.html')
