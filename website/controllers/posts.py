from flask import Blueprint, request, flash, render_template, jsonify
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect
from ..models import Post, User
from .. import db
from flask_login import login_required, current_user

posts = Blueprint('posts', __name__)


@posts.route('/post-create', methods=['GET', 'POST'])
@login_required
def post_create():

    if request.method == 'POST':
        head = request.form.get('head')
        data = request.form.get('data')

        new_post = Post(head=head, data=data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Пост було успішно додано!', category='success')

    return render_template('posts/create.html', user=current_user)


@posts.route('/news')
def news():
    news_posts = Post.query.all()
    created_by = list()

    for n in news_posts:
        created_by.append(User.query.filter_by(id=n.user_id).first())

    return render_template('posts/news.html', user=current_user,
                                              news_posts=news_posts, 
                                              created_by=created_by)


@posts.route('/post-dashboard')
@login_required
def dashboard():
    news_posts = Post.query.all()
    created_by = list()

    for p in news_posts:
        created_by.append(User.query.filter_by(id=p.user_id).first())

    return render_template('posts/dashboard.html', user=current_user,
                                                    news_posts=news_posts, 
                                                    created_by=created_by)


@posts.route('/posts/<int:id>/delete')
@login_required
def delete_post(id):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Пост було видалено.', category='success')
    return redirect(url_for('posts.dashboard'))


@posts.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))
    post_edit = Post.query.filter_by(id=id).first()

    if request.method == 'POST':
        head = request.form.get('head')
        data = request.form.get('data')

        post_edit.head = head
        post_edit.data = data
        db.session.commit()
        flash('Пост було відредаговано.', category='success')
        return redirect(url_for('posts.dashboard'))

    return render_template('posts/edit.html', user=current_user, post_edit=post_edit)


@posts.route('/news/<int:id>')
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    
    created_by = User.query.filter_by(id=post.user_id).first()

    return render_template('posts/post.html', user=current_user, post=post, created_by=created_by)


q = 5

@posts.route('/post-load')
def post_load():

    posts = Post.query.all()
    posts_json = list()
    for p in posts:
       posts_json.append([p.id, p.head, p.data.split('\n')[0], str(p.date), User.query.filter_by(id=p.user_id).first().id, User.query.filter_by(id=p.user_id).first().login])

    if request.args:

        counter = int(request.args.get('c'))

        if counter == 0:
            res = make_response(jsonify(posts_json[0:q]), 200)
        elif counter == len(posts_json):
            res = make_response(jsonify({}), 200)
        else:
            res = make_response(jsonify(posts_json[counter:counter+q]), 200)

    return res