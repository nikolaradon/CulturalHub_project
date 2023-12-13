import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from culturalhub_app.forms import RegistrationForm


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def login_data():
    return {
        'username': 'testuser',
        'password': 'testpassword'
    }


@pytest.fixture
def login_user(client, user, login_data):
    client.post(reverse('login'), login_data)
    return user


@pytest.fixture
def valid_registration_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'TestPassword123',
        'password2': 'TestPassword123',
        'birth_year': 1990,
    }


@pytest.fixture
def invalid_registration_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'TestPassword123',
        'password2': 'DifferentPassword',
        'birth_year': 2010,
    }


@pytest.fixture
def registration_form_data(valid_registration_data):
    form_data = {
        'username': valid_registration_data['username'],
        'email': valid_registration_data['email'],
        'password1': valid_registration_data['password1'],
        'password2': valid_registration_data['password2'],
        'birth_year': valid_registration_data['birth_year'],
    }
    return RegistrationForm(data=form_data)