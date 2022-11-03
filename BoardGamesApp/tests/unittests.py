from unittest import TestCase, main
from sys import path
from sqlite3 import connect
path.append('../')
from os.path import dirname
from errors import DbRecNotFoundError
from create_db import create_db
from patterns.creationing_patterns import GamerMapper, DungeonMasterMapper, CategoryMapper, GameMapper, Engine


connection = connect('test_bd.sqlite')
gamers_list = ['Arduinum628', 'Mag228']
dungeon_masters_list = ['Diego', 'Alduin72']
categories_list = ['+18', '+12', '+16']
games_dict = {
    'game_1': {'type': 'live_game', 'name': 'DnD'},
    'game_2': {'type': 'record_game', 'name': 'Blades in the Dark'},
    'game_3': {'type': 'stream_game', 'name': 'City of Mist'}
}


class TestCreateDB(TestCase):
    """Класс для тестирования создания базы данных и создания таблиц"""
    def test_create_db(self):
        """Тест создание бд"""
        create_db(f'{dirname(__file__)}/test_bd.sqlite', f'{dirname(__file__)}/../create_db.sql')


class TestCreateTables(TestCase):
    """Класс для тестирования создания данных в таблицах бд"""
    def test_create_gamer(self):
        """Метод класса для тестирования создания игрока"""
        for gamer in gamers_list:
            gamer_obj = Engine().create_user('gamer', gamer)
            GamerMapper(connection).insert(gamer_obj)

    def test_create_dungeon_master(self):
        """Метод класса для тестирования создания данжен мастера"""
        for dungeon_master in dungeon_masters_list:
            dungeon_master_obj = Engine().create_user('dungeon_master', dungeon_master)
            DungeonMasterMapper(connection).insert(dungeon_master_obj)

    def test_create_category(self):
        """Метод класса для тестирования создания категории"""
        for category in categories_list:
            category_obj = Engine().create_category(category)
            CategoryMapper(connection).insert(category_obj)

    def test_create_game(self):
        """Метод класса для тестирования создания игры"""
        for i, key in enumerate(games_dict.keys()):
            game_obj = Engine().create_game(games_dict[key]['type'], games_dict[key]['name'], categories_list[i])
            GameMapper(connection).insert(game_obj)


class TestReadListTables(TestCase):
    """Класс для тестирования получения данных из таблицы в виде списка"""
    def test_read_list_gamers(self):
        """Метод класса для тестирования чтения данных в виде списка из таблицы gamer"""
        gamers = GamerMapper(connection).all()

        for gamer in gamers:
            print(gamer.id, '-', gamer.name)

        self.assertEqual(type(gamers), type(list()))
        self.assertGreater(len(gamers), 0)

    def test_read_list_dungeon_masters(self):
        """Метод класса для тестирования чтения данных в виде списка из таблицы dungeon_master"""
        dungeon_masters = DungeonMasterMapper(connection).all()

        for dm in dungeon_masters:
            print(dm.id, '-', dm.name)

        self.assertEqual(type(dungeon_masters), type(list()))
        self.assertGreater(len(dungeon_masters), 0)

    def test_read_list_categories(self):
        """Метод класса для тестирования чтения данных в виде списка из таблицы category"""
        categories = CategoryMapper(connection).all()

        for category in categories:
            print(category.id, '-', category.name)

        self.assertEqual(type(categories), type(list()))
        self.assertGreater(len(categories), 0)

    def test_read_list_games(self):
        """Метод класса дял тестирования чтения данных в виде списка из таблицы game"""
        games = GameMapper(connection).all()

        for game in games:
            print(game.id, '-', game.name, '-', game.type_game)

        self.assertEqual(type(games), type(list()))
        self.assertGreater(len(games), 0)


class TestGetByIdItemTables(TestCase):
    """Класс для тестирования поиска item из таблицы по его id"""

    def test_get_by_id_gamer(self):
        """Метод класса для тестирования поиска gamer в таблице по его id"""
        gamer = GamerMapper(connection).get_by_id(1)
        print(gamer.id, '-', gamer.name)
        self.assertEqual(gamer.id, 1)
        self.assertEqual(gamer.name, 'Arduinum628')

    def test_get_by_id_dungeon_master(self):
        """Метод для тестирования поиска dungeon_master в таблице по его id"""
        dungeon_master = DungeonMasterMapper(connection).get_by_id(2)
        print(dungeon_master.id, '-', dungeon_master.name)
        self.assertEqual(dungeon_master.id, 2)
        self.assertEqual(dungeon_master.name, 'Alduin72')

    def test_get_by_id_category(self):
        """Метод для тестирования поиска category в таблице по её id"""
        category = CategoryMapper(connection).get_by_id(3)
        print(category.id, '-', category.name)
        self.assertEqual(category.id, 3)
        self.assertEqual(category.name, '+16')

    def test_get_by_id_game(self):
        """Метод для тестирования поиска game в таблице по её id"""
        game = GameMapper(connection).get_by_id(2)
        print(game.id, '-', game.name, '-', game.type_game, '-', game.category)
        self.assertEqual(game.id, 2)
        self.assertEqual(game.name, 'Blades in the Dark')
        self.assertEqual(game.type_game, 'record_game')
        self.assertEqual(game.category, '+12')


class TestUpdateTables(TestCase):
    """Класс для тестирования обновления данных таблиц"""
    def test_update_gamer(self):
        """Метод класса для тестирования обновление данных в таблице gamer"""
        gamer = GamerMapper(connection).get_by_id(2)
        new_name = 'Mag628'
        gamer.name = new_name
        GamerMapper(connection).update(gamer)
        gamer = GamerMapper(connection).get_by_id(2)
        self.assertEqual(gamer.name, new_name)

    def test_update_dungeon_master(self):
        """Метод класса для тестирования обновление данных в таблице dungeon_master"""
        dungeon_master = DungeonMasterMapper(connection).get_by_id(1)
        new_name = 'Diego224'
        dungeon_master.name = new_name
        DungeonMasterMapper(connection).update(dungeon_master)
        dungeon_master = DungeonMasterMapper(connection).get_by_id(1)
        self.assertEqual(dungeon_master.name, new_name)

    def test_update_category(self):
        """Метод класса для тестирования обновления данных в таблице category"""
        category = CategoryMapper(connection).get_by_id(2)
        new_name = '+14'
        category.name = new_name
        CategoryMapper(connection).update(category)
        category = CategoryMapper(connection).get_by_id(2)
        self.assertEqual(category.name, new_name)

    def test_update_game(self):
        """Метод класса для тестирования обновления данных в таблице game"""
        game = GameMapper(connection).get_by_id(1)
        new_name = '_DnD_'
        game.name = new_name
        print(game.name, game.type_game, game.category, game.id)
        GameMapper(connection).update(game)
        game = GameMapper(connection).get_by_id(1)
        self.assertEqual(game.name, new_name)


class TestDeleteTables(TestCase):
    """Класс для тестирования удаления данных из таблицы"""
    def test_delete_gamer(self):
        """Метод класса для тестирования удаления игрока"""
        gamer = GamerMapper(connection).get_by_id(2)
        GamerMapper(connection).delete(gamer)
        self.assertRaises(DbRecNotFoundError, GamerMapper(connection).get_by_id, 2)

    def test_delete_dungeon_master(self):
        """Метод класса для тестирования удаления данжен мастера"""
        dungeon_master = DungeonMasterMapper(connection).get_by_id(2)
        DungeonMasterMapper(connection).delete(dungeon_master)
        self.assertRaises(DbRecNotFoundError, DungeonMasterMapper(connection).get_by_id, 2)

    def test_delete_category(self):
        """Метод класса для тестирования удаления категории"""
        category = CategoryMapper(connection).get_by_id(3)
        CategoryMapper(connection).delete(category)
        self.assertRaises(DbRecNotFoundError, CategoryMapper(connection).get_by_id, 3)

    def test_delete_game(self):
        """Метод класса для тестирования удаления игры"""
        game = GameMapper(connection).get_by_id(3)
        GameMapper(connection).delete(game)
        self.assertRaises(DbRecNotFoundError, GameMapper(connection).get_by_id, 3)


if __name__ == '__main__':
    main()
