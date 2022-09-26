from robot_framework.templator import render
from data import games
from patterns.creationing_patterns import Engine, Logger
from patterns.structuring_patterns import AppendRoute, Debug


site = Engine()
logger = Logger('main')
routes = dict()


@AppendRoute(routes=routes, url='/')
class Index:
    """Класс вьюха главной страницы"""
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', data_list=site.categories)


# @AppendRoute(routes=routes, url='/news-1/')
# class PageNews1:
#     """Класс вьюха для новостной статьи"""
#     @Debug(name='PageNews1')
#     def __call__(self, request):
#         return '200 OK', render('page_news_1.html')
#
#
# @AppendRoute(routes=routes, url='/news-2/')
# class PageNews2:
#     """Класс вьюха для новостной статьи"""
#     @Debug(name='PageNews2')
#     def __call__(self, request):
#         return '200 OK', render('page_news_2.html')


class PageNewsPrototype:
    """Класс прототип для вьюх статей"""
    def __init__(self, num_page_news):
        self.num_page_news = num_page_news

    @Debug(name='PageNews')
    def __call__(self, request):
        return '200 OK', render(f'page_news_{self.num_page_news}.html')


class PageNewsFactory:
    """Класс для новостных создания новостных статей"""
    page_nums = [num for num in range(1, 3)]

    @classmethod
    def create_pages(cls):
        """Метод для создания новостных статей (порождающий паттерн фабричный метод)"""
        for num_page in cls.page_nums:
            new_page_news = PageNewsPrototype(num_page)
            routes[f'/news-{num_page}/'] = new_page_news


PageNewsFactory().create_pages()


@AppendRoute(routes=routes, url='/contact/')
class Contact:
    """Класс вьюха страницы контактов"""
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html')


@AppendRoute(routes=routes, url='/events/')
class Events:
    """Класс вьюха страницы расписание мероприятий"""
    @Debug(name='Events')
    def __call__(self, request):
        return '200 OK', render('events.html', date=request.get('date', None), data=[games])


@AppendRoute(routes=routes, url='/about/')
class AboutUs:
    """Класс вьюха страницы о нас"""
    @Debug(name='AboutUs')
    def __call__(self, request):
        return '200 OK', render('about_us.html')


@AppendRoute(routes=routes, url='/games-list/')
class GamesList:
    """Класс контроллер список игр"""
    @Debug(name='GamesList')
    def __call__(self, request):
        logger.log('Список игр')
        try:
            category = site.get_category_by_id(int(request['data_get']['id']))
            return '200 OK', render('games_list.html', data_list=category.games, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Games have not been added yet!'


@AppendRoute(routes=routes, url='/create-game/')
class CreateGame:
    """Класс контроллер для создания игры"""
    category_id = 0

    @Debug(name='CreateGame')
    def __call__(self, request):
        if request['method_now'] == 'POST':
            data = request['data_post']
            name = data['name']

            name = site.decode_value(name)
            category = None

            if self.category_id != 0:
                category = site.get_category_by_id(int(self.category_id))
                game = site.create_game('live_game', name, category)
                site.games.append(game)

                category.games.append(game)
                category.game_count()
            return '200 OK', render('games_list.html', data_list=site.games, name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['data_get']['id'])
                category = site.get_category_by_id(self.category_id)
                return '200 OK', render('create_game.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Categories have not been added yet!'


@AppendRoute(routes=routes, url='/create-category/')
class CreateCategory:
    """Класс контроллер для создания категории"""

    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method_now'] == 'POST':
            data = request['data_post']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None

            if category_id:
                category = site.get_category_by_id(int(category_id))

            create_category = site.create_category(name, category)
            site.categories.append(create_category)

            return '200 OK', render('index.html', data_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppendRoute(routes=routes, url='/category-list/')
class CategoryList:
    """Класс контроллер список категорий"""

    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', data_list=site.categories)


@AppendRoute(routes=routes, url='/copy-game/')
class CopyGame:
    """Класс контроллер для копирования игры"""

    @Debug(name='CopyGame')
    def __call__(self, request):
        data_get = request['data_get']
        clone_game = None
        try:
            name = data_get['name']
            old_game = site.get_game(name)

            if old_game:
                clone_name = f'copy_{name}'
                clone_game = old_game.clone()
                clone_game.name = clone_name
                site.games.append(clone_game)
            return '200 OK', render('game_list.html', data_list=site.games, name=clone_game.category.name)
        except KeyError:
            return '200 OK', 'Games have not been added yet!'
