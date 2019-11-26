from flask import url_for

from service.models import db

MOCK_LIKE_OK = {'react': 'like'}
MOCK_DISLIKE_OK = {'react': 'dislike'}
MOCK_REACT_BADTYPE = {'react': 10}
MOCK_REACT_BADVALUE = {'react': 'laic'}
MOCK_TOKEN_IDENTITY_1 = {'id': 1,
                         'username': 'testusername', 'password': 'hash'}


def test_react_success(app, client, reactions, requests_mock, jwt_token):

    reactions.client = client

    token = jwt_token.create_token(MOCK_TOKEN_IDENTITY_1)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=200)

    reply = reactions.post_story_react(MOCK_LIKE_OK, 1, token)
    assert reply.status_code == 200
    assert reply.json['message'] == 'Reaction registered'

    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1, token)
    assert reply.status_code == 200
    assert reply.json['message'] == 'Reaction updated'


def test_react_bad_syntax(app, client, reactions, requests_mock, jwt_token):
    reactions.client = client

    token = jwt_token.create_token(MOCK_TOKEN_IDENTITY_1)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=200)

    reply = reactions.post_story_react({}, 1, token)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR314'

    reply = reactions.post_story_react(MOCK_REACT_BADTYPE, 1, token)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR313'

    reply = reactions.post_story_react(MOCK_REACT_BADVALUE, 1, token)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR313'


def test_react_twice(app, client, reactions, requests_mock, jwt_token):
    reactions.client = client

    token = jwt_token.create_token(MOCK_TOKEN_IDENTITY_1)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=200)

    reply = reactions.post_story_react(MOCK_LIKE_OK, 1, token)
    assert reply.status_code == 200

    reply = reactions.post_story_react(MOCK_LIKE_OK, 1, token)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR311'

    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1, token)
    assert reply.status_code == 200

    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1, token)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR312'


def test_react_wrong_story(app, client, reactions, requests_mock, jwt_token):
    reactions.client = client

    token = jwt_token.create_token(MOCK_TOKEN_IDENTITY_1)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/0',
                      status_code=404)

    reply = reactions.post_story_react(MOCK_LIKE_OK, 0, token)
    assert reply.status_code == 404
    #assert reply.json['code'] == 'EAR333'

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/5',
                      status_code=410)

    reply = reactions.post_story_react(MOCK_LIKE_OK, 5, token)
    assert reply.status_code == 410
    #assert reply.json['code'] == 'EAR334'


def test_get_user_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/user/1',
                      status_code=200,
                      json={"username": "exampleu_name", "password": "example_pwd", "id": '1'})

    reply = reactions.get_user_react(1)
    assert reply.status_code == 200


def test_get_user_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/user/0',
                      status_code=404)

    reply = reactions.get_user_react(0)
    assert reply.status_code == 404
    #assert reply.json['code'] == 'EAR322'


def test_get_user_bad_syntax(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.get_user_react('pippo')
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR321'


def test_get_story_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=200)

    reply = reactions.get_story_react(1)
    assert reply.status_code == 200
    assert reply.json['dislikes'] == 1


def test_get_draft_story(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=403)

    reply = reactions.get_story_react(1)
    assert reply.status_code == 403


def test_get_deleted_story(app, client, reactions, requests_mock, jwt_token):
    reactions.client = client

    token = jwt_token.create_token(MOCK_TOKEN_IDENTITY_1)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=200)

    reactions.post_story_react(1, MOCK_LIKE_OK, token)

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/1',
                      status_code=410)

    reply = reactions.get_story_react(1)
    assert reply.status_code == 410


def test_get_story_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["STORIES_ENDPOINT"]}/stories/0',
                      status_code=404)

    reply = reactions.get_story_react(0)
    assert reply.status_code == 404
    #assert reply.json['code'] == 'EAR333'


def test_get_story_react_bad_syntax(app, client, reactions, requests_mock):
    reactions.client = client

    s = 'lafattoriadeglianimali'

    reply = reactions.get_story_react(s)
    assert reply.status_code == 400
    #assert reply.json['code'] == 'EAR331'
