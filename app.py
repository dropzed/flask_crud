# app.py
from flask import Flask
from .config import Config  # Импорт конфигурации
from .models import db  # Импорт db из models
from .routes import main_bp  # Импорт маршрутов
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    _app = Flask(__name__)
    _app.config.from_object(Config)  # Загрузка конфига [[10]]

    # Инициализация расширений
    db.init_app(_app)
    login_manager.init_app(_app)
    login_manager.login_view = 'main.login'  # Указание view для авторизации

    # Регистрация Blueprint
    _app.register_blueprint(main_bp)

    # Создание таблиц БД (если не существуют)
    with _app.app_context():
        db.create_all()

    return _app


# Запуск приложения
if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])