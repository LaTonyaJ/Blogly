"""Blogly application."""

from datetime import datetime
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from logging import debug
from flask import Flask, redirect, request
from models import Default_image, db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


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

    user = User(first_name=first, last_name=last, img_url=Default_image)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show User Profile"""

    user = User.query.get_or_404(user_id)
    post = Post.query.filter_by(user_id=user.id)
    return render_template('user_profile.html', user=user, post=post)


@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Display Edit User Form"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Update/Edit user"""

    user = User.query.get(user_id)

    if request.form['first'] and request.form['first'] != '':
        user.first_name = request.form['first']
    if request.form['last'] and request.form['last'] != '':
        user.last_name = request.form['last']
    if request.form['url'] and request.form['url'] != '':
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


"""****************************POSTS ROUTES**************************"""


@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Add Post Form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle post form and update post table, redirect to detail page"""

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['post_text']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content,
                user_id=user.id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Post Details page"""

    post = Post.query.get(post_id)

    return render_template('posts.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_editpost_form(post_id):
    """Display Edit Post Form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit_posts.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Update/Edit post"""

    post = Post.query.get(post_id)
    if request.form['title'] and request.form['title'] != '':
        post.title = request.form['title']
    if request.form['content'] and request.form['content'] != '':
        post.content = request.form['post_text']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete user from list and db"""

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/')


"""**********************************TAG ROUTES******************************************"""


@app.route('/tags')
def show_tags_list():

    tags = Tag.query.all()

    return render_template('tags_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag.html', tag=tag, tag_id=tag_id)


@app.route('/tags/new')
def add_tag():

    return render_template('add_tag.html')


@app.route('/tags/new', methods=['POST'])
def handle_add():

    name = request.form['name']

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_tag_edit(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    name = request.form['name']

    tag.name = name
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def handle_delete(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
