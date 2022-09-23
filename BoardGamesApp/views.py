from robot_framework.templator import render
from data import games
from patterns.creationing_patterns import Engine, Logger


site = Engine()
logger = Logger('main')


class Index:
    """Класс вьюха главной страницы"""
    def __call__(self, request):
        return '200 OK', render('index.html', data_list=site.categories)


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


class GamesList:
    """Класс контроллер список игр"""
    def __call__(self, request):
        logger.log('Список игр')
        try:
            category = site.get_category_by_id(int(request['data_get']['id']))
            return '200 OK', render('games_list.html', data_list=category.games, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Games have not been added yet!'


class CreateGame:
    """Класс контроллер для создания игры"""
    category_id = 0

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


class CreateCategory:
    """Класс контроллер для создания категории"""
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


class CategoryList:
    """Класс контроллер список категорий"""
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', data_list=site.categories)


class CopyGame:
    """Класс контроллер для копирования игры"""
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
