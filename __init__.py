from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .models import db as _db  # Импортируем db из models

login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    _db.init_app(app)
    login_manager.init_app(app)

    # Регистрация маршрутов
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Создание таблиц при необходимости
    with app.app_context():
        _db.create_all()

    return app


# Для доступа к db из других модулей
db = _db