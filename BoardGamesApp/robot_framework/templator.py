from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """Функция, которая рендерит html шаблоны"""
    path_file = f'{folder}/{template_name}'

    with open(path_file, encoding='utf-8') as file:
        template = Template(file.read())
    return template.render(**kwargs)


if __name__ == "__main__":
    test_render = render('events.html', '../templates', date='2022-09-08')
    print(test_render)
