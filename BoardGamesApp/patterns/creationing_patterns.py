from copy import deepcopy
from sqlite3 import connect
from quopri import decodestring
from sys import path
path.append('../')
from errors import IdItemError, NameItemError, DbCommitError, DbUpdateError, DbDeleteError, DbRecNotFoundError
from patterns.behavioring_patterns import Subject
from patterns.archetecturing_patterns import DomainObject


class User:
    """Класс для абстрактного пользователя"""
    def __init__(self, name):
        self.name = name


class Gamer(User, DomainObject):
    """Класс для игрока в настольные игры"""
    def __init__(self, name):
        self.games = list()
        super().__init__(name)


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
    def create_user(cls, type_user, name):
        """Метод класса для создания пользователя (порождающий паттерн Фабричный метод)"""
        return cls.types_users[type_user](name)


class GamePrototype:
    """Класс прототип настольных игр (порождающий паттерн Прототип)"""
    def clone(self):
        """Метод класса кланирует класс"""
        return deepcopy(self)


class Game(GamePrototype, Subject):
    """Класс настольная игра"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.gamers = list()
        super().__init__()

    def __getitem__(self, gamer):
        return self.gamers[gamer]

    def add_gamer(self, gamer: Gamer):
        """Метод класса для добавления нового игрока"""
        self.gamers.append(gamer)
        gamer.games.append(self)
        self.inform()


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
    def create_user(type_user, name):
        """Метод класса, вызывающий метод создания пользователя"""
        return UserFactory.create_user(type_user, name)

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

    def get_gamer(self, name) -> Gamer:
        """Метод класса для возврта игрока"""
        for gamer in self.gamers:
            if name == gamer.name:
                return gamer

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


class GamerMapper:
    """Класс для взаимодействия с бд"""
    def __init__(self, connect):
        self.connect = connect
        self.cursor = connect.cursor()
        self.table_name = 'gamer'

    def all(self):
        """Метод класса для получения списка данных из бд"""
        list_items = list()
        query_to_db_str = f'SELECT * from {self.table_name}'  # sql запрос в str
        self.cursor.execute(query_to_db_str)  # выполнение запроса
        for item in self.cursor.fetchall():  # проход по всем данным таблиц
            id_item, name = item
            gamer = Gamer(name)
            gamer.id = id_item
            list_items.append(gamer)
        return list_items

    def get_by_id(self, id_item):
        """Метод класса для получения данных по id из таблицы бд"""
        query_to_db_str = f'SELECT id, name from {self.table_name} WHERE id=?'
        self.cursor.execute(query_to_db_str, (id_item, ))
        result = self.cursor.fetchone()
        if result:
            return Gamer(*result)

    def insert(self, obj):
        """Метод класса для вставки новых данных в таблицу бд"""
        query_to_db_str = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(query_to_db_str, (obj.name, ))
        try:
            self.connect.commit()
        except Exception as err:
            raise DbCommitError(err)

    def update(self, obj):
        """Метод класса для обновления данных в таблицу бд"""
        query_to_db_str = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(query_to_db_str, (obj.name, obj.id))
        try:
            self.connect.commit()
        except Exception as err:
            raise DbUpdateError(err)

    def delete(self, obj):
        """Метод класса для удаления данных из таблицы бд"""
        query_to_db_str = f'DELETE {self.table_name} WHERE id=?'
        self.cursor.execute(query_to_db_str, (obj.id, ))
        try:
            self.connect.commit()
        except Exception as err:
            raise DbDeleteError(err)


connection = connect('patterns.sqlite')


class MapperRegistry:
    """Класс регистр мапперов (архетектурный системный паттерн - Data Mapper)"""
    mappers = {
        'gamer': GamerMapper
    }

    @staticmethod
    def get_mapper(obj):
        """Метод класса для возврата нужнного маппера"""
        if isinstance(obj, Gamer):
            return GamerMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        """Метод класса вернёт текущий маппер"""
        return MapperRegistry.mappers[name](connection)


# class Logger(metaclass=SingletonByName):
#     """Класс для логирования"""
#     def __init__(self, name):
#         self.name = name
#
#     @staticmethod
#     def log(text):
#         """Метод выполняющий логирование"""
#         print('log ---- ', text)


if __name__ == '__main__':
    engine = Engine()
    category_18 = engine.create_category('+18')
    print(category_18.id, category_18.name, category_18.category)
    category_16 = engine.create_category('+16')
    print(category_16.id, category_16.name, category_16.category)

    user_gamer = engine.create_user('gamer', 'Nemo')
    print(user_gamer)
    user_master = engine.create_user('dungeon_master', 'Garry')
    print(user_master)

    game_1 = engine.create_game('live_game', 'D&D', '+16')
    print(game_1.name, game_1.category)
