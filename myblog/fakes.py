from myblog.models import Admin,Category,Post,Comment,Link
from myblog.extensions import db
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random

fake=Faker()

def fake_admin():
    admin=Admin(
        username='admin',
        blog_title='Bluelog',
        blog_sub_title="No, i am the real thing",
        name='Mima kirigoe',
        about='u, i...'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):
    category=Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category=Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post=Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1,Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_links():
    twitter=Link(name="Twitter",url="#")
    fackbook=Link(name="Fackbook",url="#")
    linkedin=Link(name="Linkedin",url="#")
    google=Link(name="Google+",url="#")
    db.session.add_all([twitter,fackbook,linkedin,google])
    db.session.commit()