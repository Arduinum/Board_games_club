from wsgiref.simple_server import make_server
from robot_framework.main import RobotFramework
from urls import fronts
from views import routes


app = RobotFramework(routes, fronts)
port = 8080

with make_server('', port, app) as http:
    print(f'Старт запуска сервера на порту {port}...')
    http.serve_forever()


# uwsgi --http :8000 --wsgi-file run_app.py
