import datetime as dt

MOCK_SIGNUP_USER = {
    'username': 'testusername',
    'password': 'testpassword',
    'email': 'test@example.com',
    'firstname': 'Firstname',
    'lastname': 'Lastname',
    'dateofbirth': str(dt.datetime.now().date())
}
MOCK_LOGIN_USER = {'username': 'testusername', 'password': 'testpassword'}
MOCK_ACCESS_TOKEN = 'csrf_access_token=01573355-85b5-4688-b74c-1efa0e5c08d2'
MOCK_DELETED_ACCESS_TOKEN = 'csrf_access_token=deleted'
MOCK_REFRESH_TOKEN = 'csrf_refresh_token=28b2b10a-50c0-4c7d-afb7-b8ad7b8cfcae'


def test_signup_success(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/signup',
                      status_code=200)

    reply = auth.signup(MOCK_SIGNUP_USER)
    assert reply.status_code == 200


def test_signup_bad_syntax(app, client, auth, requests_mock):
    auth.client = client

    data = MOCK_SIGNUP_USER.copy()
    del data['username']
    reply = auth.signup(data)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E011'

    data = MOCK_SIGNUP_USER.copy()
    del data['password']
    reply = auth.signup(data)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E012'

    data = MOCK_SIGNUP_USER.copy()
    del data['email']
    reply = auth.signup(data)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E013'

    reply = auth.signup({})
    assert reply.status_code == 400
    assert reply.get_json().code == 'E018'


def test_signup_validation_error(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/signup/',
                      status_code=400)
    reply = auth.signup(MOCK_SIGNUP_USER)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E014'


def test_login_success(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(
        f'{app.config["AUTH_ENDPOINT"]}/api/login',
        status_code=200,
        headers={'Set-Cookie': [MOCK_ACCESS_TOKEN, MOCK_REFRESH_TOKEN]})
    reply = auth.signup(MOCK_LOGIN_USER)
    assert reply.status_code == 200
    cookies = reply.headers.getlist('Set-Cookie', type=str)
    assert len(cookies) == 2
    assert cookies[0] == MOCK_ACCESS_TOKEN
    assert cookies[1] == MOCK_REFRESH_TOKEN


def test_login_bad_syntax(app, client, auth, requests_mock):
    auth.client = client

    data = MOCK_LOGIN_USER.copy()
    del data['username']
    reply = auth.signup(data)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E021'

    data = MOCK_LOGIN_USER.copy()
    del data['password']
    reply = auth.signup(data)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E022'

    reply = auth.signup({})
    assert reply.status_code == 400
    assert reply.get_json().code == 'E028'


def test_login_invalid(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(
        f'{app.config["AUTH_ENDPOINT"]}/api/login',
        status_code=401)
    reply = auth.signup(MOCK_LOGIN_USER)
    assert reply.status_code == 403
    assert reply.get_json().error == 'E023'


def test_logout_success(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(
        f'{app.config["AUTH_ENDPOINT"]}/api/logout',
        status_code=200,
        headers={'Set-Cookie': MOCK_DELETED_ACCESS_TOKEN})
    reply = auth.logout(MOCK_ACCESS_TOKEN)
    assert reply.status_code == 200
    cookies = reply.headers.get('Set-Cookie', type=str)
    assert cookies == MOCK_DELETED_ACCESS_TOKEN


def test_logout_missing_token(app, client, auth, requests_mock):
    auth.client = client

    reply = auth.logout()
    assert reply.status_code == 401
    assert reply.get_json().error == 'E031'


def test_logout_invalid_token(app, client, auth, requests_mock):
    auth.client = client

    requests_mock.get(
        f'{app.config["AUTH_ENDPOINT"]}/api/logout',
        status_code=401)
    reply = auth.logout(MOCK_ACCESS_TOKEN)
    assert reply.status_code == 401
    assert reply.get_json().code == 'E032'
