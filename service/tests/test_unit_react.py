from flask import url_for

MOCK_LIKE_OK = {'react': 'like'}
MOCK_DISLIKE_OK = {'react': 'dislike'}
#MOCK_ACCESS_TOKEN = 'csrf_access_token=01573355-85b5-4688-b74c-1efa0e5c08d2'
MOCK_REACT_BADTYPE = {'react': 10}
MOCK_REACT_BADVALUE = {'react': 'laic'}


def test_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.post_story_react(MOCK_LIKE_OK, 1)
    assert reply.status_code == 200
    assert reply.json['message'] == 'Reaction registered'
    
    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1)
    assert reply.status_code == 200
    assert reply.json['message'] == 'Reaction updated'


def test_react_bad_syntax(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.post_story_react({}, 1)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS314'

    reply = reactions.post_story_react(MOCK_REACT_BADTYPE, 1)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS313'

    reply = reactions.post_story_react(MOCK_REACT_BADVALUE, 1)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS313'
    
    
def test_react_twice(app, client, reactions, requests_mock):
    reactions.client = client
    
    reply = reactions.post_story_react(MOCK_LIKE_OK, 1)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_LIKE_OK, 1)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS311'

    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1)
    assert reply.status_code == 200
    
    reply = reactions.post_story_react(MOCK_DISLIKE_OK, 1)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS312'
    
    
    def test_react_wrong_story(app, client, reactions, requests_mock):
        reactions.client = client

    reply = reactions.post_story_react(MOCK_LIKE_OK, 0)
    assert reply.status_code == 404
    assert reply.json['code'] == 'ERS333'

    reply = reactions.post_story_react(MOCK_LIKE_OK, 5)
    assert reply.status_code == 410
    assert reply.json['code'] == 'ERS334'


def test_get_user_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.get_user_react(1)
    assert reply.status_code == 200


#def test_get_user_react_failure(app, client, reactions, requests_mock):
#    reactions.client = client
#
#    reply = reactions.get_user_react(0)
#    assert reply.status_code == 404
#    assert json['code'] == 'ERS322'
#
#
#def test_get_user_bad_syntax(app, client, reactions, requests_mock):
#    reactions.client = client
#
#    reply = reactions.get_user_react('pippo')
#    assert reply.status_code == 400
#    assert json['code'] == 'ERS321'


def test_get_story_react_success(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.get_story_react(1)
    assert reply.status_code == 200
    assert reply.json['dislikes'] == 1


def test_get_story_react_failure(app, client, reactions, requests_mock):
    reactions.client = client

    reply = reactions.get_story_react(0)
    assert reply.status_code == 404
    assert reply.json['code'] == 'ERS333'


def test_get_story_react_bad_syntax(app, client, reactions, requests_mock):
    reactions.client = client
    
    s = 'lafattoriadeglianimali'

    reply = reactions.get_story_react(s)
    assert reply.status_code == 400
    assert reply.json['code'] == 'ERS331'
