from flask import Blueprint, request, flash, redirect, url_for, render_template
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')       
        password = request.form.get('password')

        user = User.query.filter_by(login=login).first() if User.query.filter_by(login=login).first() else User.query.filter_by(email=login).first() 
        if user:
            if check_password_hash(user.password, password):
                flash('Ви успішно авторизувались!', category='succsess')
                login_user(user, remember=True)
                return redirect(url_for('users.home'))
            else:
                flash('Щось пішло не так. Попробуйте знову.', category='error')
        else:
            flash('Такого користувача не існує.', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Користувач з такою поштою вже існує.', category='error')
        elif len(login) < 3:
            flash('Логін має містити 3 і більше символи.', category='error')
        elif len(email) < 3:
            flash('Email-адреса повинна містити 3 і більше символи.', category='error')
        elif password != password2:
            flash('Паролі не співпадають.', category='error')
        elif len(password) < 7:
            flash('Пароль повинен містити 7 і більше символів.', category='error')
        else:
            new_user = User(login=login, email=email, password=generate_password_hash(password, method='sha256'), is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            #login_user(user)
            flash('Акаунт було створено!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signUp.html', user=current_user)