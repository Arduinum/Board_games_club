from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """Функция, которая рендерит html шаблоны"""
    env = Environment()  # объект окружения
    env.loader = FileSystemLoader(folder)  # указание папки где лежит шаблон
    template = env.get_template(template_name)  # получение шаблона из окружения
    return template.render(**kwargs)
