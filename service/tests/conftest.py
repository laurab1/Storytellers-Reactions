import json
import pytest

from service.app import create_app


@pytest.fixture
def app():
    app = create_app(config='tests/config_test.py')

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

        def post_story_react(self, data, storyid):
            assert self.client is not None
            return self.client.post(f'/stories/{storyid}/react',
                                    data=json.dumps(data),   
                                    content_type='application/json')
    return ReactionsActions()
