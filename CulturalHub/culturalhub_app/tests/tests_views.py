import pytest
from django.urls import reverse


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
    assert b"Invalid login credentials. Please try again." in response.content