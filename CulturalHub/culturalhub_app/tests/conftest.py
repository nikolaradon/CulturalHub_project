import random

import pytest
from django.test import Client
from django.contrib.auth.models import User
from culturalhub_app.forms import RegistrationForm
from culturalhub_app.models import UserProfile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def create_user_profile(user):
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'country': 'US', 'birth_year': 1990, 'about': 'Test about'}
    )
    if not created:
        return user_profile

    return UserProfile.objects.get(user=user)


@pytest.fixture()
def generate_non_existing_user_id():
    while True:
        user_id = random.randint(1, 1000000)
        if not User.objects.filter(id=user_id).exists():
            return user_id


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
