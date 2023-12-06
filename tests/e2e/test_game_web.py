from flask import session
import pytest
from games.app import create_app
from utils import get_project_root


TEST_DATA_PATH = get_project_root() / "tests" / "data" / "games.csv"

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='abcd', password='Qwer1234'):
        return self.__client.post(
            '/authentication/register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='abcd', password='Qwer1234'):
        self.register(user_name, password)
        return self.__client.post(
            '/authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'bugn212', 'password': 'Qwer1234'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('ab', '', b'Your user name is too short'),
        ('abcd', '', b'Your password is required'),
        ('abcd', 'abcd', b'Your password must have at least 8 characters, contain an upper case letter,\
            a lower case letter and a digit.'),
))

def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    response = auth.login()
    assert response.headers['Location'] == '/profile?user_name=abcd'

    with client:
        client.get('/')
        assert session['user_name'] == 'abcd'


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235 Game Library' in response.data


def test_login_required_to_add_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == '/authentication/login'


def test_review(client, auth):
    auth.login()

    # Check that we can retrieve the comment page.

    response = client.get('/review?game_id=435790')
    assert response.status_code == 200


    response = client.post(
        '/review?game_id=435790',
        data={'rating': 5, 'review': 'Good game', 'game_id': 435790, 'submit': 'Submit'}
    )
    assert response.headers['Location'] == '/game/435790'

