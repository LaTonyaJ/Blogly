from models import User, Post, db, Tag
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

tonya = User(first_name='LaTonya', last_name='Johnson',
             img_url='https://st2.depositphotos.com/1445595/11009/v/600/depositphotos_110090198-stock-illustration-african-hair-dreadlocks-hairstyle-wig.jpg')


elvis = User(first_name='Elvis', last_name='Presley',
             img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqidAAsRjQLsAcqcsayDaEQpKJSBXdbxY6Vg&usqp=CAU')


jordan = User(first_name='Jordan',
              last_name='White', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8LYDvK-85DMDWCOpU8gUjI96nDk0jbWWh3Q&usqp=CAU')

paul = User(first_name='Paul', last_name='Smith')

today = Post(title='Burgers',
             content='Grilled Burgers are the best burgers.', user_id=1)

king = Post(title='King?',
            content='Who is the king? I\'m all shook up!', user_id=2)

motivate = Post(title='Captain',
                content='Steer your ship with positivity :)', user_id=4)

food_tag = Tag(name='food')
motivation = Tag(name='motivation')

db.session.add(tonya)
db.session.add(elvis)
db.session.add(jordan)
db.session.add(paul)
db.session.add(today)
db.session.add(king)
db.session.add(motivate)
db.session.add(food_tag)
db.session.add(motivation)

db.session.commit()
