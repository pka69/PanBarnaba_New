import pytest

from django.test import Client
from django.contrib.auth.models import User, Permission


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_user():
    user_data = {"username": "ananymus", "password": "1qaz2wsx3edc"}
    user = User.objects.create_user(**user_data)
    user.save()
    user_data['id]'] = user.id
    return user_data


@pytest.fixture
def create_moderator():
    user_data = {"username": "ananymus", "password": "1qaz2wsx3edc"}
    user = User.objects.create_user(**user_data)
    permission = Permission.objects.get(name='Can moderate posts')
    user.user_permissions.add(permission)
    user.save()
    user_data['id]'] = user.id
    return user_data


@pytest.fixture
def create_superuser():
    user_data = {"username": "super", "password": "1qaz2wsx3edc"}
    user = User.objects.create_superuser(**user_data)
    user.save()
    user_data['id]'] = user.id
    return user_data


# @pytest.fixture
# def post_context2():
#     my_post = {
#         'group': 0,
#         'content': 'lewjskdjvnasd,mvnakjdnawo',
#         'stage': 0,
#         'external_link': 'external_link',
#         'pictureType': '1',
#         'picture': 'picture',
#     }
#     return my_post

@pytest.fixture
def post_context():
    my_post = {
        'group': 0,
        'content': 'lewjskdjvnasd,mvnakjdnawo',
        'stage': 0,
        'external_link': 'external_link',
        'pictureType': '1',
        # 'picture': 'picture',
    }
    return my_post
