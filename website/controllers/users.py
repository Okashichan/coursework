from flask import Blueprint, request, flash, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from ..models import User
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

users = Blueprint('users', __name__)


@users.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(login) < 3:
            flash('Логін має містити 3 і більше символи.', category='error')
        elif len(email) < 3:
            flash('Email-адреса повинна містити 3 і більше символи.', category='error')
        elif check_password_hash(password, current_user.password):
            flash('Паролі не співпадають.', category='error')
        elif len(password2) < 7:
            flash('Для редагування даних введіть пароль два рази.', category='error')
        else:
            current_user.login = login
            current_user.email = email
            current_user.password = generate_password_hash(password2, method='sha256')
            flash('Дані було оновлено!', category='success')
            db.session.commit()
            return render_template('users/home.html', user=current_user)
    return render_template('users/home.html', user=current_user)


@users.route('/users', methods=['GET', 'POST'])
@login_required
def users_list():
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    users = User.query.all()

    return render_template('users/users.html', users=users, user=current_user)


@users.route('/users/<int:usr>/delete')
@login_required
def delete_user(usr):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))
    User.query.filter_by(id=usr).delete()
    db.session.commit()
    flash('Акаунт було видалено.', category='success')
    return redirect(url_for('users.users_list'))


@users.route('/users/<int:usr>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(usr):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))
    user_edit = User.query.filter_by(id=usr).first()
    
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        admin = request.form.getlist('admin')
        admin = True if admin else False

        if login == user_edit.login:
            user_edit.login = login
        elif User.query.filter_by(login=login).first():
            flash('Користувач з таким іменем вже існує!', category='error')
            return redirect(url_for('users.edit_user', usr=usr))
        else:
            user_edit.login = login

        if email == user_edit.email:
            user_edit.email = email
        elif User.query.filter_by(email=email).first():
            flash('Користувач з такою поштою вже існує!', category='error')
            return redirect(url_for('users.edit_user', usr=usr))
        else:
            user_edit.email = email

        if password:
            user_edit.password = generate_password_hash(password, method='sha256')

        user_edit.is_admin = admin
        db.session.commit()
        flash('Акаунт було відредаговано.', category='success')
        return redirect(url_for('users.users_list'))
    return render_template('users/edit.html', user=current_user, user_edit=user_edit)


@users.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('views.index'))
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        admin = request.form.getlist('admin')
        admin = True if admin else False

        if User.query.filter_by(email=email).first():
            flash('Користувач з такою поштою вже існує!', category='error')
            return redirect(url_for('users.add_user'))
        elif User.query.filter_by(login=login).first():
            flash('Користувач з таким іменем вже існує!', category='error')
            return redirect(url_for('users.add_user'))

        new_user = User(login=login, email=email, password=generate_password_hash(password, method='sha256'), is_admin=admin)
        db.session.add(new_user)
        db.session.commit()
        flash('Акаунт було створено!', category='success')

        return redirect(url_for('users.users_list'))
    return render_template('users/edit.html', user=current_user)


@users.route('/user/<login>')
@login_required
def user(login):
    user_page = User.query.filter_by(login=login).first_or_404()

    return render_template('users/user.html', user=current_user, user_page=user_page)