from conftest import client


def test_create_user():
    response = client.post(
        '/users/sign-up/',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == 201
