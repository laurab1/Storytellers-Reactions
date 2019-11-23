import json
import pytest
import flask_jwt_extended as jwt

from service.app import create_app


@pytest.fixture
def app():
    app = create_app(config='config_test.py')

    return app


@pytest.fixture
def client_factory(app):

    class ClientFactory:

        def __init__(self, app):
            self._app = app

        def get(self):
            return self._app.test_client()

    return ClientFactory(app)


@pytest.fixture
def client(app, client_factory):
    return client_factory.get()


@pytest.fixture
def reactions():

    class ReactionsActions:

        def __init__(self):
            self.client = None

        def get_user_react(self, userid):
            assert self.client is not None
            return self.client.get(f'/users/{userid}/get_react')

        def get_story_react(self, storyid):
            assert self.client is not None
            return self.client.get(f'/stories/{storyid}/get_react')

        def post_story_react(self, data, storyid, token):
            assert self.client is not None
            if token is not None:
                self.client.set_cookie(
                    'localhost', 'access_token_cookie', token)
            return self.client.post(f'/stories/{storyid}/react',
                                    data=json.dumps(data),   
                                    content_type='application/json')
    return ReactionsActions()


@pytest.fixture()
def jwt_token(app):

    class JWTActions():

        def create_token(self, identity, refresh=False, max_age=None):
            with app.app_context():
                if refresh:
                    return jwt.create_refresh_token(identity,
                                                    expires_delta=max_age)
                return jwt.create_access_token(identity,
                                               expires_delta=max_age)

        def set_token(self, response, token, refresh=False):
            with app.app_context():
                if refresh:
                    jwt.set_refresh_cookies(response, token)
                else:
                    jwt.set_access_cookies(response, token)

        def token_headers(self, identity, refresh=False, max_age=None):
            with app.app_context():
                token = self.create_token(identity, max_age=max_age)
                res = jsonify({})
                self.set_token(res, token)
                if refresh:
                    token = self.create_token(
                        identity, refresh=True, max_age=max_age)
                    self.set_token(res, token, refresh=True)
                return res.headers['Set-Cookie']

    return JWTActions()