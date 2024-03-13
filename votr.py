from flask import (
        Flask, render_template, request, flash, redirect, url_for, session, jsonify
        )
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Topics, Polls, Options, UserPolls
from flask_migrate import Migrate

from flask_admin import Admin
from admin import AdminView, TopicView

import config
from celery import Celery

# blueprints
from api.api import api

votr = Flask(__name__)

votr.register_blueprint(api)

votr.config.from_object('config')

db.init_app(votr)
#with votr.app_context():
#    db.create_all()    # 只在第一次创建模型时使用，以后的模型更改都通过migrate完成

migrate = Migrate(votr, db, render_as_batch=True)

admin = Admin(votr, name='Dashboard', index_view=TopicView(Topics, db.session, url='/admin', endpoint='admin'))
admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Polls, db.session))
admin.add_view(AdminView(Options, db.session))

def make_celery(app):
    celery = Celery(app.import_name, broker=config.CELERY_BROKER)
    celery.conf.update(votr.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with votr.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
# create celery object
celery = make_celery(votr)

@votr.route('/')
def home():
    return render_template('index.html')

@votr.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # get the user details from the form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # hash the password
        password = generate_password_hash(password)

        user = Users(email=email, username=username, password=password)

        db.session.add(user)
        db.session.commit()

        flash('Thanks for signing up please login')

        return redirect(url_for('home'))

    # it's a GET request, just render the template
    return render_template('signup.html')

@votr.route('/login', methods=['POST'])
def login():
    # we don't need to check the request type as flask will raise a bad request
    # error if a request aside from POST is made to this url
    username = request.form['username']
    password = request.form['password']

    # search the database for the User
    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password

        if check_password_hash(password_hash, password):
            # The hash matches the password in the database log the user in
            session['user'] = username

            flash('Login was succesfull')
    else:
        # user wasn't found in the database
        flash('Username or password is incorrect please try again', 'error')

    return redirect(url_for('home'))

@votr.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

        flash('We hope to see you again!')

    return redirect(url_for('home'))

@votr.route('/polls', methods=['GET'])
def polls():

    return render_template('polls.html')

@votr.route('/polls/<poll_name>')
def poll(poll_name):

    return render_template('index.html')

