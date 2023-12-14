import random

import pytest
from django.test import Client
from django.contrib.auth.models import User
from culturalhub_app.forms import RegistrationForm
from culturalhub_app.models import UserProfile, Category, UserContent


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


@pytest.fixture
def create_test_category():
    return Category.objects.create(name='Test')


@pytest.fixture
def create_test_category_with_content(create_user_profile, create_test_category):
    user_profile = create_user_profile
    category = create_test_category
    content1 = UserContent.objects.create(title='content1', category=category, author=user_profile)
    content2 = UserContent.objects.create(title='content2', category=category, author=user_profile)

    return content1, content2
