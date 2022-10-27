import pytest

from home_app.models import Post
from login_app.models import CustomUser, Relations


@pytest.fixture
def user():
    return CustomUser.objects.create(username='testowy', password='1234', email='jacek@gmail.com', image='default.jpg')


@pytest.fixture
def user2():
    return CustomUser.objects.create(username='testowy2', password='1234', email='jacek@gmail.com', image='default.jpg')


@pytest.fixture
def post(user):
    data = {
        'title': 'test',
        'body': 'test_body',
        'status': 'draft',
        'author_id': user.id,
    }
    return Post.objects.create(**data)

@pytest.fixture
def relation(user, user2):
    return Relations.objects.create(initiator=user, receiver=user2)
