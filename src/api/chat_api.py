from flask_restful import Resource, reqparse
from db.chat import *
from flask import *
from db.swen344_db_utils import *
from hashlib import sha512
import secrets

#List All Users API
class AllUsers(Resource):
    """This class uses the list_all_users() method to list all of the users in the database."""
    def get(self):
        return json.jsonify(list_all_users())
    
    #Add a user (with all their information). This would be POST. Parameters should be in the BODY
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']
    
        session_key = hashlib.sha512(secrets.token_bytes(32)).hexdigest()

        create_user(username, password, session_key)

        return jsonify(list_all_users())
    
    #Edit a users information. This would be a PUT to do a SQL UPDATE. Again, parameters in the BODY.
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('old_username', type=str, required=True)
        parser.add_argument('new_username', type=str, required=True)
        args = parser.parse_args()

        old_username = args['old_username']
        new_username = args['new_username']

        update_user(old_username, new_username)

        return jsonify(list_all_users())
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='args')
        args = parser.parse_args()

        username_to_delete = args['username']

        delete_user(username_to_delete)

        return jsonify(list_all_users())

#List All Communities and Channels API
class AllCommunitiesAndChannels(Resource):
    """This class uses the list_all_communities_and_channels() method to list all of the communities and channels within the database."""
    def get(self):
        return json.jsonify(list_all_communities_and_channels())
    
#Search for messages API
class MessageSearch(Resource):
    """This class is meant to use the search_message() method to find a message(s) based on a string or start and end date."""
    def get(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('string', type=str, required=True, location='args')
        parser.add_argument('start_date', type=str, required=True, location='args')
        parser.add_argument('end_date', type=str, required=True, location='args')
        args = parser.parse_args()

        search_results = search_messages(args['string'], args['start_date'], args['end_date'])

        return json.jsonify(search_results)

#List all messages in a particular channel API
class MessagesInSpecificChannel(Resource):
    """This class will get all of the messages in a certain channel with the list_all_messages_in_specific_channel()"""
    def get(self,community_name=None, channel_name=None):
        if channel_name:
            messages = list_all_messages_in_specific_channel(community_name,channel_name)
            return json.jsonify(messages)
        
class DirectMessages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('max_messages', type=int, location='args')
        args = parser.parse_args()
        
        return json.jsonify(list_all_direct_messages(args['max_messages']))
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True, location='json')
        parser.add_argument('date', type=str, location='json')
        parser.add_argument('time', type=str, location='json')
        parser.add_argument('sender', type=str, required=True, location='json')
        parser.add_argument('receiver', type=str, required=True, location='json')
        args = parser.parse_args()
        
        date = args.get('date', None)
        time = args.get('time', None)
        
        new_dm = add_direct_message(args['message'], args['sender'], args['receiver'], date, time)
        
        return new_dm   