class IdItemError(Exception):
    """Класс ошибка категории"""
    def __str__(self):
        return 'CategoryError'


class NameItemError(Exception):
    """Класс ошибка имени"""
    def __str__(self):
        return 'NameError'


class DbCommitError(Exception):
    """Класс ошибка внесения изменений в бд"""
    def __init__(self, mess):
        self.mess = mess

    def __str__(self):
        return f'DbCommitError: {self.mess}'


class DbUpdateError(Exception):
    """Класс ошибка обновления данных в бд"""
    def __init__(self, mess):
        self.mess = mess

    def __str__(self):
        return f'DbUpdateError: {self.mess}'


class DbDeleteError(Exception):
    """Класс ошибка удаления данных из бд"""
    def __init__(self, mess):
        self.mess = mess

    def __str__(self):
        return f'DbDeleteError: {self.mess}'


class DbRecNotFoundError(Exception):
    """Класс ошибка не найдена запись в бд"""
    def __init__(self, mess):
        self.mess = mess

    def __str__(self):
        return f'DbRecNotFoundError: {self.mess}'


if __name__ == '__main__':
    try:
        raise IdItemError
    except IdItemError as err:
        print(err)

    try:
        raise NameItemError
    except NameItemError as err:
        print(err)
