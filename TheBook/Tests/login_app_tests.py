import pytest

# @pytest.mark.django_db
# def test_check_settings():
#     assert True
from django.urls import reverse

from login_app.models import CustomUser, Relations


@pytest.mark.django_db
def test_login_view(client):
    url = reverse('login-view')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_user_exists(client, user):
    # User does exist!
    CustomUser.objects.get(username='testowy')
    url = reverse('register-view')
    response = client.get(url)
    assert response.status_code == 200
    data = {
        'name': 'testowy',
        'password': '1234',
        'password2': '1234',
        'email': 'jacek@gmail.com',
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view(client, user):
    url = reverse('register-view')
    data = {
        'name': 'NIE_testowy',
        'password': '1234',
        'password2': '1234',
        'email': 'jacek@gmail.com',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    #Checking for user in database
    CustomUser.objects.get(username='NIE_testowy')


@pytest.mark.django_db
def test_logout_view(client):
    url = reverse('logout-view')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_view_1(client, user):
    url = reverse('profile-view', args=[user.id])
    response = client.get(url)
    url_redirect_nologin = reverse('login-view')
    #Checks if user, that is not logged in is redirected to login page
    assert response.url.startswith(url_redirect_nologin)
    assert response.status_code == 302



@pytest.mark.django_db
def test_profile_view_2(client, user):
    url = reverse('profile-view', args=[user.id])
    client.force_login(user)
    response = client.get(url)
    CustomUser.objects.get(username='testowy', email='jacek@gmail.com', image='default.jpg')
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view_3(client, user):
    url = reverse('profile-view', args=[user.id])
    client.force_login(user)
    data = {
        'name': 'testowy_updated',
        'email': 'email_updated@gmail.com',
        'profile_pic': 'updated.png',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    CustomUser.objects.get(username='testowy_updated', email='email_updated@gmail.com', image='profile_pics/updated.png')

@pytest.mark.django_db
def test_follow_view(client, user, user2):
    client.force_login(user)
    url = reverse('follow-view', args=[user2.id])
    response = client.post(url)
    assert response.status_code == 302
    Relations.objects.get(initiator=user, receiver=user2)


@pytest.mark.django_db
def test_unfollow_view(client, user, user2):
    client.force_login(user)
    url = reverse('unfollow-view', args=[user2.id])
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_send_message_get(client, user, user2):
    client.force_login(user)
    url = reverse('send-message', args=[user2.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_send_message_post(client, user, user2):
    client.force_login(user)
    url = reverse('send-message', args=[user2.id])
    data = {'body': 'this is a test message body'}
    response = client.post(url, data)
    assert response.status_code == 302
    user.send_messages.get(body="this is a test message body")


@pytest.mark.django_db
def test_message_get(client, user, relation):
    client.force_login(user)
    url = reverse('messages-view')
    response = client.get(url)
    assert response.status_code == 200