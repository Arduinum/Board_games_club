from views import Index, Contact, Events, AboutUs
from datetime import date


# for front controller
def date_front(request):
    """Функция назначает ключ значение для даты в словаре запроса"""
    request['date'] = date.today()


def other_front(request):
    """Функция назначает ключ значение для прочих данных в словаре запроса"""
    request['key'] = 'key'


fronts = [date_front, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/events/': Events(),
    '/about/': AboutUs()
}
