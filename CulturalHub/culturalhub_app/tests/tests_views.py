import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from culturalhub_app.models import UserProfile


@pytest.mark.django_db
def test_login_view_authenticated_user(client, user):
    client.force_login(user)
    response = client.get(reverse('login'))
    assert response.status.code == 302
    assert response.url == reverse('main-page')


@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'invalidpassword'})
    assert response.status_code == 200
    assert 'Invalid login credentials. Please try again.' in response.text


@pytest.mark.django_db
def test_register_view_successful_registration(client, valid_registration_data):
    response = client.post(reverse('register'), valid_registration_data)
    assert response.status_code == 200
    assert 'Profile has been successfully created. Please log in.' in response.text

    user = User.objects.get(username=valid_registration_data['username'])
    assert user is not None

    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_register_view_invalid_registration(client, invalid_registration_data):
    response = client.post(reverse('register'), invalid_registration_data)

    assert response.status_code == 200
    assert 'Please correct the errors below' in response.text
    assert "The two password fields didn't match" in response.text

    with pytest.raises(ObjectDoesNotExist):
        User.objects.get(username=invalid_registration_data['username'])


def test_logout_view(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert not response.wsqi_request.user.is_authenticated


def test_logout_view_unauthenticated_user(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('login')


