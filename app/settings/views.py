import requests
from flask import Blueprint, current_app, request, make_response, jsonify
from flask.views import MethodView

from .models import Settings
from ..extensions import db
from ..models import User

settings = Blueprint('settings', __name__)


class SettingsAPI(MethodView):
    """
    Settings Resource
    """

    @staticmethod
    def post():
        # get the post data
        post_data = request.get_json()
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user_settings = Settings.query.filter_by(user_id=resp).first()
                try:
                    if not user_settings:
                        user_settings = Settings(
                            user_id=resp,
                            driver_seat_tilt=post_data.get('driverSeatTilt'),
                            passenger_seat_tilt=post_data.get('passengerSeatTilt'),
                            driver_mirror_tilt_X=post_data.get('driverMirrorTiltX'),
                            driver_mirror_tilt_Y=post_data.get('driverMirrorTiltY'),
                            passenger_mirror_tilt_X=post_data.get('passengerMirrorTiltX'),
                            passenger_mirror_tilt_Y=post_data.get('passengerMirrorTiltY'),
                        )
                        # insert the user
                        db.session.add(user_settings)
                        db.session.commit()
                    else:
                        user_settings.driver_seat_tilt = post_data.get('driverSeatTilt')
                        user_settings.passenger_seat_tilt = post_data.get('passengerSeatTilt')
                        user_settings.driver_mirror_tilt_X = post_data.get('driverMirrorTiltX')
                        user_settings.driver_mirror_tilt_Y = post_data.get('driverMirrorTiltY')
                        user_settings.passenger_mirror_tilt_X = post_data.get('passengerMirrorTiltX')
                        user_settings.passenger_mirror_tilt_Y = post_data.get('passengerMirrorTiltY')
                        db.session.commit()
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': 'Some error occurred: ' + str(e)
                    }
                    return make_response(jsonify(response_object)), 401

                if current_app.config.get('CAR_MODEL_API_ENABLED'):
                    api_response = requests.post(
                        current_app.config.get('CAR_MODEL_API_URL'),
                        json={
                            'driverSeatTilt': user_settings.driver_seat_tilt,
                            'passengerSeatTilt': user_settings.passenger_seat_tilt,
                            'driverMirrorTiltX': user_settings.driver_mirror_tilt_X,
                            'driverMirrorTiltY': user_settings.driver_mirror_tilt_Y,
                            'passengerMirrorTiltX': user_settings.passenger_mirror_tilt_X,
                            'passengerMirrorTiltY': user_settings.passenger_mirror_tilt_Y
                        }
                    )

                    if not api_response.ok or api_response.json().get('status') != 'ok':
                        response_object = {
                            'status': 'fail',
                            'message': 'Some error with the model occurred: ' + api_response
                        }
                        return make_response(jsonify(response_object)), 401

                response_object = {
                    'status': 'success',
                    'data': {
                        'driverSeatTilt': user_settings.driver_seat_tilt,
                        'passengerSeatTilt': user_settings.passenger_seat_tilt,
                        'driverMirrorTiltX': user_settings.driver_mirror_tilt_X,
                        'driverMirrorTiltY': user_settings.driver_mirror_tilt_Y,
                        'passengerMirrorTiltX': user_settings.passenger_mirror_tilt_X,
                        'passengerMirrorTiltY': user_settings.passenger_mirror_tilt_Y
                    }
                }
                return make_response(jsonify(response_object)), 201
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
            return make_response(jsonify(response_object)), 401

    @staticmethod
    def get():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user_settings = Settings.query.filter_by(user_id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'driverSeatTilt': user_settings.driver_seat_tilt,
                        'passengerSeatTilt': user_settings.passenger_seat_tilt,
                        'driverMirrorTiltX': user_settings.driver_mirror_tilt_X,
                        'driverMirrorTiltY': user_settings.driver_mirror_tilt_Y,
                        'passengerMirrorTiltX': user_settings.passenger_mirror_tilt_X,
                        'passengerMirrorTiltY': user_settings.passenger_mirror_tilt_Y
                    }
                }
                return make_response(jsonify(response_object)), 200
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
            return make_response(jsonify(response_object)), 401


# define the API resources
settings_view = SettingsAPI.as_view('settings_api')

# add Rules for API Endpoints
settings.add_url_rule(
    '/settings',
    view_func=settings_view,
    methods=['GET', 'POST']
)
