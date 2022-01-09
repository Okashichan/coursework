import os
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
from ..models import Gallery, User
from .. import db, ALLOWED_EXTENSIONS
from flask_login import login_required, current_user
import random  
import string  

gallery = Blueprint('gallery', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def random_string(len=8):
    return ''.join((random.choice(string.ascii_lowercase + string.ascii_uppercase) for x in range(len)))


@gallery.route('/gallery')
def gallery_render():
    gallery = Gallery().query.all()
    for g in gallery:
        print(g.img)
    return render_template('gallery/gallery.html', user=current_user, gal=gallery)


@gallery.route('/gallery-add', methods=['GET', 'POST'])
@login_required
def gallery_add():

    if request.method == 'POST':
        file = request.files['gal']
        text = request.form.get('text')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name = filename.split('.')
            img_name = random_string()
            ext = name[1]
            img_name = img_name+'.'+ext
            img = os.path.join(current_app.config['UPLOAD_FOLDER'], img_name)
            file.save(img)
        else:
            flash('Підримуються лише наступні формати файлів: jpg, jpeg, gif!', category='error')
            return redirect(url_for('gallery.gallery_add'))

        new_image = Gallery(text=text, img=img_name, ext=ext, user_id=current_user.id)

        db.session.add(new_image)
        db.session.commit()
        flash('Картинку було успішно додано!', category='success')
        return redirect(url_for('gallery.gallery_add'))  

    return render_template('gallery/gallery_add.html', user=current_user)


@gallery.route('/gallery-dashboard', methods=['GET', 'POST'])
@login_required
def gallery_dashboard():
    gallery = Gallery().query.all()
    created_by = list()

    for g in gallery:
        created_by.append(User.query.filter_by(id=g.user_id).first())

    return render_template('gallery/dashboard.html', user=current_user,
                                                     gal=gallery, 
                                                     created_by=created_by)


@gallery.route('/gallery/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def gallery_delete(id):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    img = Gallery.query.filter_by(id=id).first()
    img_remove = os.path.join(current_app.config['UPLOAD_FOLDER'], img.img)
    if os.path.isfile(img_remove):
        Gallery.query.filter_by(id=id).delete()
        os.remove(img_remove)
    else:
        flash('Такої картинки не існує.', category='success')
        return redirect(url_for('gallery.gallery_dashboard'))
    db.session.commit()
    flash('Картинку було видалено.', category='success')

    return redirect(url_for('gallery.gallery_dashboard'))


@gallery.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def gallery_edit(id):
    if not current_user.is_admin:
        return redirect(url_for('views.index'))

    img = Gallery.query.filter_by(id=id).first()
    img_remove = os.path.join(current_app.config['UPLOAD_FOLDER'], img.img)
    old_img_name = img.img

    if request.method == 'POST':
        file = request.files['gal']
        text = request.form.get('text')
        if not allowed_file(file.filename):
            flash('Підримуються лише наступні формати файлів: jpg, jpeg, gif!', category='error')
            return redirect(url_for('gallery.gallery_edit', id=id))

        if os.path.isfile(img_remove):
            if file:
                os.remove(img_remove)
                new_img = os.path.join(current_app.config['UPLOAD_FOLDER'], old_img_name)
                file.save(new_img)

            img.text = text
            db.session.commit()
            flash('Дані було відредаговано.', category='success')
            return redirect(url_for('gallery.gallery_dashboard'))      

    return render_template('gallery/gallery_edit.html', user=current_user, img=img)