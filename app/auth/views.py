from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from ..extensions import bcrypt, db
from ..models import User, BlacklistToken

auth = Blueprint('auth', __name__)


class RegisterImageAPI(MethodView):
    """
    User Registration via Image Resource
    """

    @staticmethod
    def post():
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    image=post_data.get('image')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()

                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(response_object)), 201
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response_object)), 202


class LoginImageAPI(MethodView):
    """
    User Login via Image Resource
    """

    @staticmethod
    def post():
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.get_user(image=post_data.get('image'))
            if user:
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    @staticmethod
    def post():
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and bcrypt.check_password_hash(
                    user.password, post_data.get('password')
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    @staticmethod
    def post():
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403


# define the API resources
registration_image_view = RegisterImageAPI.as_view('register_image_api')
login_image_view = LoginImageAPI.as_view('login_image_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth.add_url_rule(
    '/auth/register',
    view_func=registration_image_view,
    methods=['POST']
)
auth.add_url_rule(
    '/auth/login',
    view_func=login_image_view,
    methods=['POST']
)
auth.add_url_rule(
    '/auth/login/basic',
    view_func=login_view,
    methods=['POST']
)
auth.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
