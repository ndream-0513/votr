from flask import (
  Flask, render_template, request, flash, redirect, url_for, session
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users

votr = Flask(__name__)

votr.config.from_object('config')

db.init_app(votr)
with votr.app_context():
    db.create_all()

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

@votr.route('/polls')
def polls():

    return render_template('polls.html')

if __name__ == '__main__':
    votr.run(host='0.0.0.0')
