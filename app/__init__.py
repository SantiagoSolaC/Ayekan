from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from os import path
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from .auth.routes import auth
    from .src.routes import views
    from .auth.models import User
    
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists("app/ayekan.db"):
        db.create_all(app = app)