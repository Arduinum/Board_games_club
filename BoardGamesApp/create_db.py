from sqlite3 import connect


def create_db(name_db, name_sql):
    """Функция для создания базы данных"""
    connection = connect(name_db)
    cursor_now = connection.cursor()

    with open(name_sql, 'r') as f:
        text = f.read()

    cursor_now.executescript(text)
    cursor_now.close()
    connection.close()


if __name__ == '__main__':
    create_db('patterns.sqlite', 'create_db.sql')
