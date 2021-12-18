import os
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
from ..models import Gallery
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
            ext = name[1]
            img = random_string()+'.'+ext
            img = os.path.join(current_app.config['UPLOAD_FOLDER'], img)
            file.save(img)

        new_image = Gallery(text=text, img=img, ext=ext, user_id=current_user.id)

        db.session.add(new_image)
        db.session.commit()
        flash('Картинку було успішно додано!', category='success')
        return redirect(url_for('gallery.gallery_add'))  

    return render_template('gallery/gallery_add.html', user=current_user)