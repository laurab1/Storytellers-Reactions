import functools

from flask import jsonify, request

'''
Constant value representing the endpoint. This has to be written with two
uppercase letter, eg. API Gateway -> AG)
'''
EP_CODE = 'AR' # Reactions service identifier

'''
Dictionary with all errors related to this service and the
corresponding error messages and status_code
'''
EP_DICT = {
    # Reactions errors
    '010': (400, 'You\'ve already liked this story'),
    '011': (400, 'You\'ve already disliked this story'),
    '012': (400, 'Reaction value must be \'like\' or \'dislike\''),
    '013': (400, 'Reaction message must not be empty'),
    '014': (400, 'The story identifier must be an integer'),
    '015': (403, 'The requested story is a draft'),
    '016': (404, 'The requested story does not exist'),
    '017': (410, 'The requested story was deleted')
    '018': (400, 'The user identifier must be an integer'),
    '019': (404, 'You must provide an identifier associated to a registered user'),
    '020': (400, 'The user identifier must be an integer'),
    '021': (404, 'You must provide an identifier associated to a registered user'),
    '030': (400, 'The story identifier must be an integer'),
    '031': (403, 'The requested story is a draft'),
    '032': (404, 'The requested story does not exist'),
    '033': (410, 'The requested story was deleted')
}


def response(code):
    '''
    Standard for the error response.

    The code must be written as a three number code, call it xyz, as follows:
        x -> the number of the current blueprint
        y -> the number of the route of the current blueprint
        z -> the number of the error within the current route

    Returns:
        A json response ready to be sent via a Flask view
    '''
    status_code, message = EP_DICT[code]
    return jsonify({
        'code': f'E{EP_CODE}{code}',
        'message': message
    }), status_code

