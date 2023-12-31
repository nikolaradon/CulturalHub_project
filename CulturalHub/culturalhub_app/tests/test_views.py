import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from culturalhub_app.forms import UserProfileForm
from culturalhub_app.models import UserProfile, Category, UserContent


@pytest.mark.django_db
def test_login_view_authenticated_user(client, user):
    client.force_login(user)
    response = client.get(reverse('login'))
    assert response.status_code == 302
    assert response.url == reverse('main-page')


@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'invalidpassword'})
    assert response.status_code == 200
    assert b'Please enter a correct username and password' in response.content


@pytest.mark.django_db
def test_register_view_successful_registration(client, valid_registration_data):
    response = client.post(reverse('register'), valid_registration_data)
    assert response.status_code == 302
    assert response.url == reverse('login')

    user = User.objects.get(username=valid_registration_data['username'])
    assert user is not None

    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_register_view_invalid_registration(client, invalid_registration_data):
    response = client.post(reverse('register'), invalid_registration_data)
    assert response.status_code == 200

    with pytest.raises(ObjectDoesNotExist):
        User.objects.get(username=invalid_registration_data['username'])


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout_view_unauthenticated_user(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_main_page_view_user_info(client, user):
    client.force_login(user)
    response = client.get(reverse('main-page'))
    assert response.status_code == 200
    assert 'user' in response.context
    assert response.context['user'] == user


@pytest.mark.django_db
def test_user_profile_view_user_exists(client, create_user_profile):
    response = client.get(reverse('user', args=[create_user_profile.user.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile_view_user_doesnt_exist(client, create_user_profile, generate_non_existing_user_id):
    non_existing_user_id = generate_non_existing_user_id
    response = client.get(reverse('user', args=[non_existing_user_id]))
    assert response.status_code == 302
    assert response.url == reverse('main-page')


@pytest.mark.django_db
def test_category_content_view(client, create_test_category, create_test_category_with_content):
    category = create_test_category
    content1, content2 = create_test_category_with_content

    response = client.get(reverse('category', kwargs={'category': category}), follow=True)

    assert response.status_code == 200
    assert 'category' in response.context
    assert 'contents' in response.context
    assert response.context['category'] == category
    assert list(response.context['contents']) == [content1, content2]


@pytest.mark.django_db
def test_content_view_existing_content(client, create_test_category, create_test_category_with_content):
    category = create_test_category
    content1, content2 = create_test_category_with_content

    response = client.get(reverse('content-view', kwargs={'content_id': content1.id}), follow=True)

    assert response.status_code == 200
    assert 'content' in response.context
    assert 'category' in response.context
    assert response.context['content'] == content1
    assert response.context['category'] == category


@pytest.mark.django_db
def test_user_profile_edit_view_authenticated_owner(client, create_user_profile):
    user_profile = create_user_profile
    client.force_login(user_profile.user)
    response = client.get(reverse('edit-user', kwargs={'user_id': user_profile.user.id}))

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'user_profile' in response.context
    assert isinstance(response.context['form'], UserProfileForm)
    assert response.context['user_profile'] == user_profile


