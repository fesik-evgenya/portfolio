from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from .config import Config

from .main_routes import main_bp
from .admin.routes import admin_bp


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # Регистрация blueprints
    from .main_routes import main_bp
    from .admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/panel')

    # Создание администратора по умолчанию
    with app.app_context():
        # Импорт моделей необходим для create_all
        from . import models
        db.create_all()
        from .models import Admin
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('Tdutif_85')
            db.session.add(admin)
            db.session.commit()

    return app