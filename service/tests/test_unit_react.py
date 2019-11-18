MOCK_LIKE_OK = {'react': 'like'}
MOCK_DISLIKE_OK = {'react': 'dislike'}
MOCK_ACCESS_TOKEN = 'csrf_access_token=01573355-85b5-4688-b74c-1efa0e5c08d2'
MOCK_REACT_BADTYPE = {'react': 10}
MOCK_REACT_BADVALUE = {'react': 'laic'}

MOCK_GET_USER_REACT = {'user_id': 'testuserid'}
MOCK_GET_STORY_REACT = {'story_id': 'teststoryid'}


def test_react_success(app, client, reactions, requests_mock):
    auth.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/stories/1/react',
                      status_code=200
                      headers={'Set-Cookie': [MOCK_ACCESS_TOKEN, MOCK_REFRESH_TOKEN]})

    reply = reactions.post_story_react(MOCK_LIKE_OK)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_DISLIKE_OK)
    assert reply.status_code == 200


def test_react_bad_syntax(app, client, reactions, requests_mock):
    auth.client = client

    reply = reactions.post_story_react({}})
    assert reply.status_code == 400
    assert reply.get_json().code == 'E0'

    reply = reactions.post_story_react(MOCK_REACT_BADTYPE)
    assert reply.status_code == 400
    assert reply.get_json().message == 'invalid type'

    reply = reactions.post_story_react(MOCK_REACT_BADVALUE)
    assert reply.status_code == 400
    assert reply.get_json().message == 'invalid value'
    
    
def test_react_twice(app, client):
    reply = reactions.post_story_react(MOCK_LIKE_OK)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_LIKE_OK)
    assert reply.status_code == 400
    assert reply.get_json().message == 'you\'ve already liked this story!'

    reply = reactions.post_story_react(MOCK_DISLIKE_OK)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_DISLIKE_OK)
    assert reply.status_code == 400
    assert reply.get_json().message == 'you\'ve already disliked this story!'


def test_get_user_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    data = MOCK_GET_USER_REACT.copy()
    data_user_id = data['user_id']

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/{data_user_id}/get_react',
                      status_code=200)

    reply = reactions.get_user_react(MOCK_GET_USER_REACT)
    assert reply.status_code == 200

def test_get_user_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    data = MOCK_GET_USER_REACT.copy()
    data_user_id = data['user_id']

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/{data_user_id}/get_react',
                      status_code=404)

    reply = reactions.get_user_react(MOCK_GET_USER_REACT)
    assert reply.status_code == 404
    assert reply.get_json().code == 'E112' #unregistered user

def test_get_story_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    data = MOCK_STORY_REACT.copy()
    data_story_id = data['story_id']

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/{data_story_id}/get_react',
                      status_code=200)

    reply = reactions.get_story_react(MOCK_STORY_REACT)
    assert reply.status_code == 200

def test_get_story_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    data = MOCK_STORY_REACT.copy()
    data_story_id = data['story_id']

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/{data_story_id}/get_react',
                      status_code=404)

    reply = reactions.get_story_react(MOCK_STORY_REACT)
    assert reply.status_code == 404
    assert reply.get_json().code == 'unregistered story' #to add the error case in errors.py
