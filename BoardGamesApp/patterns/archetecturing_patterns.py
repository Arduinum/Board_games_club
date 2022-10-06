from threading import local


class UnitOfWork:
    """Класс архитектурный системный паттерн"""
    current_thread = local()  # текущий поток

    def __init__(self):
        self.mapper_registry = None
        self.new_object_list = list()
        self.dirty_object_list = list()
        self.deleted_object_list = list()

    def set_mapper_registry(self, mapper_registry):
        """Метод класса чтоб назначить маппер для регистрации"""
        self.mapper_registry = mapper_registry

    def register_obj_new(self, obj):
        """Метод класса для добавления в список регистрации нового объекта"""
        self.new_object_list.append(obj)

    def register_obj_dirty(self, obj):
        """Метод класса для добавления в список объекта для изменения"""
        self.dirty_object_list.append(obj)

    def register_obj_del(self, obj):
        """Метод класса для добавления в список на удаление"""
        self.deleted_object_list.append(obj)

    def insert_data(self):
        """Метод класса выполняет команду создание новых данных из списка в таблицах бд"""
        for obj in self.new_object_list:
            self.mapper_registry.get_mapper(obj).insert(obj)

    def update_data(self):
        """Метод класса выполняет команду обновление данных из списка в таблицах бд"""
        for obj in self.dirty_object_list:
            self.mapper_registry.get_mapper(obj).update(obj)

    def delete_data(self):
        """Метод класса выполняет команду удаление данных из списка в таблицах бд"""
        for obj in self.deleted_object_list:
            self.mapper_registry.get_mapper(obj).delete(obj)

    def commit(self):
        """Метод класса для сохранения изменений в бд"""
        self.insert_data()
        self.update_data()
        self.delete_data()

        # очищение списков
        self.new_object_list.clear()
        self.dirty_object_list.clear()
        self.deleted_object_list.clear()

    @classmethod
    def set_current(cls, unit_of_work):
        """Метод класса для создания нового потока"""
        cls.current_thread.unit_of_work = unit_of_work

    @classmethod
    def new_current(cls):
        """Метод класса вызывает метод для создания нового потока"""
        cls.set_current(UnitOfWork())

    @classmethod
    def get_current(cls):
        return cls.current_thread.unit_of_work


class DomainObject:
    """Класс domain object"""

    def mark_new(self):
        """Метод класса для вызова метода класса на отправку в список создания объектов"""
        UnitOfWork.get_current().register_obj_new(self)

    def mark_dirty(self):
        """Метод класса для вызова метода класса на отправку список изменения объектов"""
        UnitOfWork.get_current().register_obj_dirty(self)

    def mark_removed(self):
        """Метод класса для вызова метода класса на отправку список удаления объектов"""
        UnitOfWork.get_current().register_obj_del(self)
