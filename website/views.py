from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('main.html', user=current_user)


@views.route('/gallery')
def gallery():
    return render_template('gallery.html', user=current_user)


@views.route('/news')
def news():
    return render_template('news.html', user=current_user)