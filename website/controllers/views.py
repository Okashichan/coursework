from flask import Blueprint, render_template
from flask_login import current_user
#from werkzeug.security import generate_password_hash
#from .. import db
#from website.models import Post, User
#import lorem

views = Blueprint('views', __name__)


@views.route('/')
def index():
    #admin = User(login='okashi', email='okashichandesu@gmail.com', password=generate_password_hash('12345678', method='sha256'), is_admin=True)
    #db.session.add(admin)
    #for p in range(25):
    #    post = Post(head=lorem.sentence(), data=lorem.text()+'\n'+lorem.text(), user_id=1)
    #    db.session.add(post)
    #db.session.commit()
    return render_template('main.html', user=current_user)
