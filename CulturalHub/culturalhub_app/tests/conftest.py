import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')
