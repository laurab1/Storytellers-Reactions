MOCK_LIKE_OK = {'react': 'like'}
MOCK_DISLIKE_OK = {'react': 'dislike'}
MOCK_ACCESS_TOKEN = 'csrf_access_token=01573355-85b5-4688-b74c-1efa0e5c08d2'
MOCK_REACT_BADTYPE = {'react': 10}
MOCK_REACT_BADVALUE = {'react': 'laic'}


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
    assert reply.get_json().code == 'E314'

    reply = reactions.post_story_react(MOCK_REACT_BADTYPE)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E313'

    reply = reactions.post_story_react(MOCK_REACT_BADVALUE)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E313'
    
    
def test_react_twice(app, client, reactions, requests_mock):
    reply = reactions.post_story_react(MOCK_LIKE_OK)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_LIKE_OK)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E311'

    reply = reactions.post_story_react(MOCK_DISLIKE_OK)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_DISLIKE_OK)
    assert reply.status_code == 400
    assert reply.get_json().code == 'E312'


def test_get_user_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/1/get_react',
                      status_code=200)

    reply = reactions.get_user_react(1)
    assert reply.status_code == 200


def test_get_user_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/0/get_react',
                      status_code=404)

    reply = reactions.get_user_react(0)
    assert reply.status_code == 404
    assert reply.get_json().code == 'E322'


def test_get_user_bad_syntax(app, client, reactions, requests_mock):
   reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/users/pippo/get_react',
                      status_code=404)

    reply = reactions.get_user_react('pippo')
    assert reply.status_code == 404
    assert reply.get_json().code == 'E321'


def test_get_story_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/stories/1/get_react',
                      status_code=200)

    reply = reactions.get_story_react(1)
    assert reply.status_code == 200


def test_get_story_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/stories/0/get_react',
                      status_code=200)

    reply = reactions.get_story_react(0)
    assert reply.status_code == 404
    assert reply.get_json().code == 'E333'


def test_get_story_react_bad_syntax(app, client, reactions, requests_mock):
    reactions.client = client

    requests_mock.get(f'{app.config["USERS_ENDPOINT"]}/api/stories/lafattoriadeglianimali/get_react',
                      status_code=200)

    reply = reactions.get_story_react('lafattoriadeglianimali')
    assert reply.status_code == 404
    assert reply.get_json().code == 'E331'
