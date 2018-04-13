from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Wish, Movie


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()


def wishes(count=100):
    user_count = User.query.count()
    movie_count = Movie.query.count()
    with db.session.no_autoflush:
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            m = Movie.query.offset(randint(0, movie_count - 1)).first()
            w = Wish(movietosee=m, seer=u)
            if Wish.query.filter_by(movietosee=m, seer=u).count() == 0:
                db.session.add(w)

        db.session.commit()
