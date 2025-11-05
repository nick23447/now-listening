from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from musicblog.config import Config
from flask_migrate import Migrate
from flask_mail import Mail

db: SQLAlchemy= SQLAlchemy()
migrate: Migrate = Migrate()
bcrypt: Bcrypt = Bcrypt()
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'users.login'
mail: Mail = Mail()

def create_app(config_class: type[Config] = Config) -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from musicblog.users.routes import users
    from musicblog.posts.routes import posts
    from musicblog.main.routes import main
    from musicblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

