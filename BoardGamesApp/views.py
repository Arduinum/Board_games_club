from robot_framework.templator import render
from data import games
from patterns.creationing_patterns import Engine, MapperRegistry
from patterns.structuring_patterns import AppendRoute, Debug
from patterns.behavioring_patterns import TelegramNotifier, EmailNotifier, ListView, CreateView, BaseSerializer, \
    ConsoleWriter, FileWriter
from patterns.archetecturing_patterns import UnitOfWork


site = Engine()
logger_console = ConsoleWriter()
loger_file = FileWriter()
routes = dict()
telegram_notifier = TelegramNotifier()
email_notifier = EmailNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppendRoute(routes=routes, url='/')
class Index:
    """Класс вьюха главной страницы"""
    @Debug(name='Index')
    def __call__(self, request):
        logger_console.writer('Главная страница')
        loger_file.writer('Главная страница (Index)')
        return '200 OK', render('index.html', data_list=site.categories)


class PageNewsPrototype:
    """Класс прототип для вьюх статей"""
    def __init__(self, num_page_news):
        self.num_page_news = num_page_news

    @Debug(name='PageNews')
    def __call__(self, request):
        logger_console.writer('Новостная страница')
        loger_file.writer('Новостная страница (PageNews)')
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
        logger_console.writer('Страница контактов')
        loger_file.writer('Страница контактов (Contact)')
        return '200 OK', render('contact.html')


@AppendRoute(routes=routes, url='/events/')
class Events:
    """Класс вьюха страницы расписание мероприятий"""
    @Debug(name='Events')
    def __call__(self, request):
        logger_console.writer('Страница расписаний игр')
        loger_file.writer('Страница расписаний игр (Events)')
        return '200 OK', render('events.html', date=request.get('date', None), data=[games])


@AppendRoute(routes=routes, url='/about/')
class AboutUs:
    """Класс вьюха страницы о нас"""
    @Debug(name='AboutUs')
    def __call__(self, request):
        logger_console.writer('Страница о нас')
        loger_file.writer('Страница о нас (AboutUs)')
        return '200 OK', render('about_us.html')


@AppendRoute(routes=routes, url='/games-list/')
class GamesList:
    """Класс контроллер список игр"""
    @Debug(name='GamesList')
    def __call__(self, request):
        # logger.log('Список игр')
        logger_console.writer('Страница список игр')
        loger_file.writer('Страница список игр (GamesList)')
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
                game.observers.append(email_notifier)
                game.observers.append(telegram_notifier)

                site.games.append(game)
                category.games.append(game)
                category.game_count()

            logger_console.writer('Страница список игр')
            loger_file.writer('Страница список игр (GamesList)')

            return '200 OK', render('games_list.html', data_list=site.games, name=category.name, id=category.id)
        else:
            try:
                logger_console.writer('Страница создать игру')
                loger_file.writer('Страница создать игру (CreateGame)')

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

            logger_console.writer('Главная страница')
            loger_file.writer('Главная страница (Index)')

            return '200 OK', render('index.html', data_list=site.categories)
        else:
            logger_console.writer('Страница создать категорию')
            loger_file.writer('Страница создать категорию (CreateCategory)')

            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppendRoute(routes=routes, url='/category-list/')
class CategoryList:
    """Класс контроллер список категорий"""

    @Debug(name='CategoryList')
    def __call__(self, request):
        logger_console.writer('Страница список категорий')
        loger_file.writer('Страница список категорий (CategoryList)')
        return '200 OK', render('category_list.html', data_list=site.categories)


@AppendRoute(routes=routes, url='/copy-game/')
class CopyGame:
    """Класс контроллер для копирования игры"""

    @Debug(name='CopyGame')
    def __call__(self, request):
        logger_console.writer('Страница список игр')
        loger_file.writer('Страница список игр (GamesList)')

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
            return '200 OK', render('games_list.html', data_list=site.games, name=clone_game.category.name)
        except KeyError:
            return '200 OK', 'Games have not been added yet!'


@AppendRoute(routes=routes, url='/gamer-list/')
class GamerListView(ListView):
    """Класс вьюха для списка игроков"""
    queryset = site.gamers
    template_name = 'gamer_list.html'

    def get_queryset(self):
        """Метод класса для получения запроса"""
        mapper = MapperRegistry.get_current_mapper('gamer')
        return mapper.all()


@AppendRoute(routes=routes, url='/create-gamer/')
class GamerCreateView(CreateView):
    """Класс вьюха для создания игрока"""
    template_name = '/create_gamer.html/'

    def create_object(self, data: dict):
        """Метод класса для создания объекта игрок"""
        name = site.decode_value(data['name'])
        new_gamer = site.create_user('gamer', name)
        site.gamers.append(new_gamer)
        new_gamer.mark_new()
        UnitOfWork.get_current().commit()


@AppendRoute(routes=routes, url='/add-gamer/')
class AddGamerForGameCreateView(CreateView):
    """Класс вьюха для добавления игрока для игры"""
    template_name = 'add_gamer.html'

    def get_context_data(self):
        """Метод класса для возврата контекста"""
        context = super().get_context_data()
        context['games'] = site.games
        context['gamers'] = site.gamers
        return context

    def create_object(self, data: dict):
        """Метод класса для создания объекта"""
        game_name = site.decode_value(data['game_name'])
        game = site.get_game(game_name)
        gamer_name = site.decode_value(data['gamer_name'])
        gamer = site.get_gamer(gamer_name)
        game.add_gamer(gamer)


@AppendRoute(routes=routes, url='/dungeon_master-list/')
class DungeonMasterListView(ListView):
    """Класс вьюха для списка данжен мастеров"""
    queryset = site.dungeon_masters
    template_name = 'dungeon_master_list.html'

    def get_queryset(self):
        """Метод класса для получения запроса"""
        mapper = MapperRegistry.get_current_mapper('dungeon_master')
        return mapper.all()


@AppendRoute(routes=routes, url='/create-dungeon_master/')
class DungeonMasterCreateView(CreateView):
    """Класс вьюха для создания данжен мастера"""
    template_name = '/create_dungeon_master.html/'

    def create_object(self, data: dict):
        """Метод класса для создания объекта данжен мастер"""
        name = site.decode_value(data['name'])
        new_dungeon_master = site.create_user('dungeon_master', name)
        site.dungeon_masters.append(new_dungeon_master)
        new_dungeon_master.mark_new()
        UnitOfWork.get_current().commit()


@AppendRoute(routes=routes, url='/add-dungeon_master/')
class AddDungeonMasterForGameCreateView(CreateView):
    """Класс вьюха для добавления данжен мастера на игру"""
    template_name = 'add_dungeon_master.html'

    def get_context_data(self):
        """Метод класса для возврата контекста"""
        context = super().get_context_data()
        print(context)
        context['games'] = site.games
        print(site.games)
        context['dungeon_masters'] = site.dungeon_masters
        print(site.dungeon_masters)
        return context

    def create_object(self, data: dict):
        """Метод класса для создания объекта"""
        game_name = site.decode_value(data['game_name'])
        game = site.get_game(game_name)
        dungeon_master_name = site.decode_value(data['dungeon_master_name'])
        dungeon_master = site.get_gamer(dungeon_master_name)
        game.add_dungeon_master(dungeon_master)


@AppendRoute(routes=routes, url='/api/')
class GameApi:
    """Класс api для игр"""
    @Debug(name='GameApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.games).coding_data()
