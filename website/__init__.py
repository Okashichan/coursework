from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from datetime import datetime

db = SQLAlchemy()
DB_NAME = 'database.db'
UPLOAD_FOLDER = 'website/static/gallery/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5YNpad34DOdWprjXWeTzbujT2rqSHSYx'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from website.controllers.views import views
    from website.controllers.auth import auth
    from website.controllers.users import users
    from website.controllers.posts import posts
    from website.controllers.gallery import gallery

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Ви повинні авторизуватись щоб отримати доступ до цієї сторінки!'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user=current_user), 404

    @app.before_request
    def before_request():
        if current_user:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created!')