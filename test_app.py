from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class TestFlask(TestCase):

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="Test", img_url='')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            u = {'first_name': 'Test', 'last_name': 'Name', 'img_url': ''}
            resp = client.post('/users/new', data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">Test Name</a></li>', html)

    # def test_post(self):
    #     with app.test_client() as client:
    #         post = {'title': 'Example',
    #                 'content': 'This is an example post', 'user_id': '1'}
    #         resp = client.post('/users/1/posts/new',
    #                            data=post, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertIn('<h3>Example</h3>', html)
