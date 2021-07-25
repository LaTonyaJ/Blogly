"""Blogly application."""

from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from logging import debug
from flask import Flask, redirect, request
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = 'Letsgetblogging!!!!'
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def users():
    """Display list of users and add user button"""

    users = User.query.all()
    return render_template('users_list.html', users=users)


@app.route('/users/new')
def new_user():
    return render_template('add_user_form.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """Get user info from form and save to db then display list of users"""
    first = request.form['first_name']
    last = request.form['last_name']
    url = request.form['url']

    user = User(first_name=first, last_name=last, img_url=url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show User Profile"""

    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Display Edit User Form"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Update/Edit user"""

    user = User.query.get(user_id)

    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.img_url = request.form['url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from list and db"""

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
