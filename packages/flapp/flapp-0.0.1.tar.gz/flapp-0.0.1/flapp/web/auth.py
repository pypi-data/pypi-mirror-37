from functools import wraps

from flask import jsonify, g, request

def authorized(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        error = False
        if not auth_header:
            error = True

        user_id = None
        if not error and auth_header.startswith('Bearer '):
            user_id = extract_user_id(auth_header[len('Bearer '):])

        if not user_id:
            error = True

        if error:
            response = jsonify({ 'error': 'Not authorized' })
            response.status_code = 401
            return response

        request.user_id = user_id

        return f(*args, **kwargs)

    return wrapper


def make_auth_token(user_id):
    return str(user_id)


def extract_user_id(token):
    return int(token)
