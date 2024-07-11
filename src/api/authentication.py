from flask_restful import Resource, reqparse
import hashlib
import secrets
from db.swen344_db_utils import *
from db.chat import *
from flask import *


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        args = parser.parse_args()
        
        username = args['username']
        password = args['password']

        result, status_code = login_user(username, password)
        
        return result, status_code
        
class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_key', type=str, required=True, location='json')
        args = parser.parse_args()
        
        session_key = args['session_key']

        result, status_code = logout_user(session_key)
        
        return result, status_code

