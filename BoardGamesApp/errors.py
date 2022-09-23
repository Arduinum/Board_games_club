class IdItemError(Exception):
    """Класс ошибка категории"""
    def __str__(self):
        return 'CategoryError'


class NameItemError(Exception):
    """Класс ошибка имени"""
    def __str__(self):
        return 'NameError'


if __name__ == '__main__':
    try:
        raise IdItemError
    except IdItemError as err:
        print(err)

    try:
        raise NameItemError
    except NameItemError as err:
        print(err)
