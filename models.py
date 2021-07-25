"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Default_image = 'https://thewanderers.travel/data_content/meet-the-wanderers/blank-user-img.jpg'


class User(db.Model):
    """User Table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    last_name = db.Column(db.String(50),
                          nullable=False)

    img_url = db.Column(
        db.Text, default=Default_image,
        nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


def connect_db(app):
    db.app = app
    db.init_app(app)
