class PageError404:
    """Класс, отвечающий за информацию о не найденой странице"""
    def __call__(self, request):
        return '404 ERROR', '404 Page Not Found'


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


class NameFormError(Exception):
    """Класс ошибка имени в форме"""
    def __str__(self):
        return 'NameFormError'


class AddDungeonMasterError(Exception):
    """Класс ошибка добавления данжен мастера на игру"""
    def __str__(self):
        return 'AddDungeonMasterError'


if __name__ == '__main__':
    try:
        raise IdItemError
    except IdItemError as err:
        print(err)

    try:
        raise NameItemError
    except NameItemError as err:
        print(err)
