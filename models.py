"""Models for Blogly."""
from flask import Flask
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


Default_image = 'https://thewanderers.travel/data_content/meet-the-wanderers/blank-user-img.jpg'


class User(db.Model):
    """User Table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    img_url = db.Column(
        db.Text, default=Default_image,
        nullable=False)

    posts = db.relationship('Post', backref='user')

    posts = db.relationship("Post", cascade="all, delete")

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post Table"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True)

    title = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    user = db.relationship('User')

    tags = db.relationship('Tag')


class Tag(db.Model):
    """Tag Table"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


class PostTag(db.Model):
    """Where post and tags intercept"""

    __tablename__ = 'posts_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
