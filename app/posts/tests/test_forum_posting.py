import pytest


@pytest.mark.django_db
def make_post_by_superuser(client, create_superuser, post_context2):
    client.login(username=create_superuser['username'], password=create_superuser['password'])
    post = post_context2
    post['id'] = create_superuser['id]']
    response = client.post('/post/forum/', post)
    assert response.status_code == 200