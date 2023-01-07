import datetime

import jwt
from flask import current_app
from sqlalchemy.sql.type_api import UserDefinedType

from ..extensions import db, bcrypt
from ..recognition import encode


class CUBE(UserDefinedType):
    def get_col_spec(self, **kw):
        return "CUBE"


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    face_embeddings_low = db.Column(CUBE, unique=True, nullable=False)
    face_embeddings_high = db.Column(CUBE, unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    settings = db.relationship('Settings', backref='user', lazy=True, uselist=False)

    def __init__(self, email, password, image, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

        face_embeddings = encode(image)
        self.face_embeddings_low = ','.join(str(s) for s in face_embeddings[0][0:64])
        self.face_embeddings_high = ','.join(str(s) for s in face_embeddings[0][64:128])

        self.registered_on = datetime.datetime.now()
        self.admin = admin

    @staticmethod
    def get_user(image):
        threshold = 0.6
        face_embeddings = encode(image)

        query = "SELECT * FROM users WHERE sqrt(power(CUBE(array[{}]) <-> face_embeddings_low, 2) + power(CUBE(array[{}]) <-> face_embeddings_high, 2)) <= {} ".format(
            ','.join(str(s) for s in face_embeddings[0][0:64]),
            ','.join(str(s) for s in face_embeddings[0][64:128]),
            threshold,
        ) + "ORDER BY sqrt(power(CUBE(array[{}]) <-> face_embeddings_low, 2) + power(CUBE(array[{}]) <-> face_embeddings_high, 2)) ASC".format(
            ','.join(str(s) for s in face_embeddings[0][0:64]),
            ','.join(str(s) for s in face_embeddings[0][64:128]),
        )

        return User.query.from_statement(db.text(query)).first()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
