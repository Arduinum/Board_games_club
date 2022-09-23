from copy import deepcopy
from quopri import decodestring
from sys import path
path.append('../')
from errors import IdItemError, NameItemError


class User:
    """Класс для абстрактного пользователя"""
    pass


class Gamer(User):
    """Класс для игрока в настольные игры"""
    pass


class DungeonMaster(User):
    """Класс для ведущего настольной игры"""
    pass


class UserFactory:
    """Класс для создания пользователей"""
    types_users = {
        'gamer': Gamer,
        'dungeon_master': DungeonMaster
    }

    @classmethod
    def create_user(cls, type_user):
        """Метод класса для создания пользователя (порождающий паттерн Фабричный метод)"""
        return cls.types_users[type_user]()


class GamePrototype:
    """Класс прототип настольных игр (порождающий паттерн Прототип)"""
    def clone(self):
        """Метод класса кланирует класс"""
        return deepcopy(self)


class Game(GamePrototype):
    """Класс настольная игра"""
    def __init__(self, name, category):
        self.name = name
        self.category = category


class LiveGame(Game):
    """Класс живая игра с данжен мастером в клубе настольных игр"""
    pass


class RecordGame(Game):
    """Класс игра, которая в виде видеозаписи"""
    pass


class StreamGame(Game):
    """Класс стрим игры в реальном времени"""
    pass


class GameFactory:
    """Класс для создания игр"""
    types_games = {
        'live_game': LiveGame,
        'record_game': RecordGame,
        'stream_game': StreamGame
    }

    @classmethod
    def create_game(cls, type_game, name, category):
        """Метод для создания игр (порождающий паттерн фабричный метод)"""
        return cls.types_games[type_game](name, category)


class Category:
    """Класс категория настольной игры"""
    num_id = 0

    def __init__(self, name, category):
        Category.num_id += 1
        self.id = Category.num_id
        self.name = name
        self.category = category
        self.games = list()

    def game_count(self):
        """Метод класса, который считает колличество игр"""
        count = len(self.games)
        if self.category:
            count += 1
        return count


class Engine:
    """Класс интерфейс проекта"""
    def __init__(self):
        self.gamers = list()
        self.dungeon_masters = list()
        self.games = list()
        self.categories = list()

    @staticmethod
    def create_user(type_user):
        """Метод класса, вызывающий метод создания пользователя"""
        return UserFactory.create_user(type_user)

    @staticmethod
    def create_category(name, category=None):
        """Метод класса, вызывающий класс категорию для создания категории"""
        return Category(name, category)

    def get_category_by_id(self, id):
        """Метод класса для получения категории по её id"""
        try:
            for category in self.categories:
                if category.id == id:
                    return category
            raise IdItemError
        except IdItemError as err:
            print(f'Нет категории где id={id}, {err}')

    @staticmethod
    def create_game(tape_game, name, category):
        """Метод класса, вызывающий метод для создания игры"""
        return GameFactory.create_game(tape_game, name, category)

    def get_game(self, name):
        """Метод класса для получения игры по её названию"""
        try:
            for game in self.games:
                if game.name == name:
                    return game
            raise NameItemError
        except NameItemError as err:
            print(f'Нет игры где name={name}, {err}')

    @staticmethod
    def decode_value(value):
        """Метод класса для правильного декодирования в utf-8"""
        value_bytes = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
        value_decode_str = decodestring(value_bytes)
        return value_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Класс порождающий паттерн Сингл тон для того чтоб у класса был один экземпляр имени"""
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """Класс для логирования"""
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        """Метод выполняющий логирование"""
        print('log ---- ', text)


if __name__ == '__main__':
    engine = Engine()
    category_18 = engine.create_category('+18')
    print(category_18.id, category_18.name, category_18.category)
    category_16 = engine.create_category('+16')
    print(category_16.id, category_16.name, category_16.category)

    user_gamer = engine.create_user('gamer')
    print(user_gamer)
    user_master = engine.create_user('dungeon_master')
    print(user_master)

    game_1 = engine.create_game('live_game', 'D&D', '+16')
    print(game_1.name, game_1.category)
