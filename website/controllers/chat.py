from flask import Blueprint, request, flash, redirect, url_for, render_template
from ..models import Chat, User
from .. import db
from flask_login import login_required, current_user

chat = Blueprint('chat', __name__)


@chat.route('/chat', methods=['GET', 'POST'])
def chat_render():

    chats = Chat.query.all()
    chats.reverse()

    if request.method == 'POST':
        login = request.form.get('login')
        text = request.form.get('text')
        if current_user.is_authenticated:
            if User.query.filter_by(login=login).first() and current_user.login != login:
                flash('Ви не можете використовувати логін іншого існуючого користувача!', category='error')
                return redirect(url_for('chat.chat_render'))
        elif User.query.filter_by(login=login).first():
            flash('Ви не можете використовувати логін існуючого користувача!', category='error')
            return redirect(url_for('chat.chat_render'))
        new_message = Chat(user_id=current_user.id if current_user.is_authenticated else 0, login=login, text=text)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('chat.chat_render'))

    return render_template('chat/chat.html', user=current_user, chats=chats)


@chat.route('/chat-dashboard', methods=['GET', 'POST'])
@login_required
def chat_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    chats = Chat.query.all()

    return render_template('chat/dashboard.html', user=current_user, chats=chats)


@chat.route('/chat/<int:id>/delete')
@login_required
def delete_user(id):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))
    Chat.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Повідомлення було видалено.', category='success')
    return redirect(url_for('chat.chat_dashboard'))