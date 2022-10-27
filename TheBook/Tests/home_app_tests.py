import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from home_app.models import Post, Comment
from login_app.models import CustomUser


@pytest.mark.django_db
def test_home_view_1(client):
    url = reverse('home-view')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_home_view_2(client, user):
    url = reverse('home-view')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_create_1(client, user):
    url = reverse('create-post')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_create_2(client, user):
    url = reverse('create-post')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_create_3(client, user):
    url = reverse('create-post')
    client.force_login(user)
    data = {
        'title': 'created',
        'body': 'test_body',
        'status': 'draft',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    Post.objects.get(title='created')


@pytest.mark.django_db
def test_post_create_4(client, user):
    url = reverse('create-post')
    client.force_login(user)
    data = {
        'title': 'created',
        'body': 'test_body',
        'status': 'draft',
    }
    client.post(url, data)
    Post.objects.get(title='created')


@pytest.mark.django_db
def test_post_update_view(client, user, post):
    url = reverse('post-view', kwargs={'pk': post.id})
    response = client.get(url)
    assert response.status_code == 302
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    update_data = {
        'title': 'test_update',
        'body': 'test_body_update',
        'status': 'published',
    }
    response = client.post(url, update_data)
    assert response.status_code == 302
    Post.objects.get(**update_data)


@pytest.mark.django_db
def test_post_delete(client, user, post):
    url = reverse('post-delete', kwargs={'pk': post.id})
    response = client.get(url)
    assert response.status_code == 302
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_like(client, user, post):
    client.force_login(user)
    url = reverse('post-like', kwargs={'pk': post.id})
    response = client.post(url)
    assert response.status_code == 302
    assert Post.objects.get(id=post.id).total_likes() == 1
    assert CustomUser.objects.get(id=user.id).liked_posts.get(id=post.id) == post


@pytest.mark.django_db
def test_add_comment(client, user, post):
    client.force_login(user)
    url = reverse('add-comment', kwargs={'pk': post.id})
    response = client.get(url)
    assert response.status_code == 200
    data = {
        'body': 'test_comment_body',
    }
    response = client.post(url, data)
    assert response.status_code == 302
