import pytest


@pytest.mark.django_db
def test_access_for_superuser_to_moderateView(client, create_superuser, post_context):
    client.login(username=create_superuser['username'], password=create_superuser['password'])
    response = client.get('/moderate/2/')
    assert response.status_code == 200
    response = client.post('/moderate/2/', post_context)
    assert response.status_code == 200
    response = client.get('/moderate/quiz/')
    assert response.status_code == 200



@pytest.mark.django_db
def test_access_for_moderator_to_moderateView(client, create_moderator, post_context):
    client.login(username=create_moderator['username'], password=create_moderator['password'])
    response = client.get('/moderate/2/')
    assert response.status_code == 200
    response = client.post('/moderate/2/', post_context)
    assert response.status_code == 200
    response = client.get('/moderate/quiz/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_access_for_user_to_moderateView(client, create_user, post_context):
    client.login(username=create_user['username'], password=create_user['password'])
    response = client.get('/moderate/2')
    assert response.status_code != 200
    response = client.post('/moderate/2/', post_context)
    assert response.status_code != 200
    response = client.get('/moderate/quiz/')
    assert response.status_code != 200