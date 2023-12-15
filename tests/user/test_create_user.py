import pytest

from conftest import client


@pytest.mark.parametrize('username, email, password', [
    ('string', 'user@example.com', 'string'),
    ('anotheruser', 'anotheruser@example.com', 'password123'),
    ('testuser', 'testuser@example.com', 'test123'),
])
def test_create_user(username, email, password):
    response = client.post(
        '/users/sign-up/',
        json={
            'username': username,
            'email': email,
            'password': password,
        },
    )
    assert response.status_code == 201
