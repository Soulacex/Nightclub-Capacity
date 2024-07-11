import unittest
from tests.test_utils import *
from src.db.chat import *
import json
from hashlib import sha512

class TestChat(unittest.TestCase):
    def setUp(self):
        """Initialize DB using API call"""
        post_rest_call(self, 'http://127.0.0.1:5000/manage/init')
        print("DB Should be reset now")
    
    def test_api_list_all_users(self):
        #Setup & Invoke
        expected_users = 6
        actual_users = get_rest_call(self, 'http://127.0.0.1:5000/users')
        
        #Analyze
        self.assertEqual(expected_users, len(actual_users))
        print(actual_users)
    
    def test_api_list_all_comms_and_chans(self):
        #Setup & Invoke
        expected_comms = 2
        actual_comms = get_rest_call(self, 'http://127.0.0.1:5000/communities')
        
        #Analyze
        self.assertEqual(expected_comms, len(actual_comms))
        print(actual_comms)
        
    def test_api_search_messages_with_hello(self):
        #Setup
        expected_messages = [
            {'messageID': 1, 'message': 'Hello Costello! How are you today?', 'date': '06-05-1922', 'time': '2:05 PM', 'sender': 'Abbott', 'receiver': 'Costello', 'comm_name': 'Comedy', 'chan_name': '#Dialogs'},
            {'messageID': 2, 'message': 'Hello Abbott. Long time, no see.', 'date': '06-05-1922', 'time': '2:33 PM', 'sender': 'Costello', 'receiver': 'Abbott', 'comm_name': 'Comedy', 'chan_name': '#Dialogs'},
        ]
        
        #Invoke
        actual_messages = get_rest_call(self, 
        'http://127.0.0.1:5000/messages/search?string=Hello&start_date=01-01-1922&end_date=01-01-1992')
        
        #Analyze
        self.assertEqual(expected_messages, actual_messages)
        print(actual_messages)
        
    def test_api_list_messages_in_channel(self):
        #Setup
        expected_messages = [
            (1, 'Hello Costello! How are you today?', '06-05-1922', '2:05 PM', 'Abbott', 'Costello', 'Comedy', '#Dialogs'),
            (2, 'Hello Abbott. Long time, no see.', '06-05-1922', '2:33 PM', 'Costello', 'Abbott', 'Comedy', '#Dialogs'),
        ]
    
        #Invoke
        actual_messages = get_rest_call(self, 'http://127.0.0.1:5000/channels/messages/Comedy/%23Dialogs')
        
        #Analyze
        self.assertEqual(len(actual_messages), len(expected_messages))
        print(actual_messages)
    
    def test_api_list_messages_in_empty_channel(self):
        #Setup
        expected_messages = []
        
        #Invoke
        actual_messages = get_rest_call(self, 'http://127.0.0.1:5000/channels/messages/Comedy/%23Zaire')
        
        #Analyze
        self.assertEqual(actual_messages, expected_messages)
        print(actual_messages)  
        
    """Rest 2 Tests"""
    #You can add a new user with a password and any other user information
    def test_api_add_user(self):
        # Setup 
        new_user_data = {'username': 'MonseuirParis', 'password': 'royalewithcheese'}
        header = {'content-type': 'application/json'}
        post_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(new_user_data), header)

        #Invoke
        actual_users = get_rest_call(self, 'http://127.0.0.1:5000/users')

        #Analyze
        expected_users_count = 7  
        self.assertEqual(expected_users_count, len(actual_users))
        print(actual_users)
        
    def test_api_user_already_exists(self):
        #Setup
        new_user_data = {'username': 'MonseuirParis', 'password': 'royalewithcheese'}
        header = {'content-type': 'application/json'}
        post_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(new_user_data), header)
        
        #Invoke
        already_response = post_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(new_user_data), header)
        
        #Analyze
        usernames = [user['username'] for user in already_response]
        self.assertEqual(1, usernames.count('MonseuirParis')) #There should only be one occurence of the user 'MonseuirParis'.

        
    def test_api_login_and_logout(self):
        #Setup
        user_data = {'username': 'MonseuirParis', 'password': 'royalewithcheese'}
        header = {'content-type': 'application/json'}
        
        #Invoke & Analyze
        post_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(user_data), header) #Creating the user MonseuirParis.
        login_data = post_rest_call(self, 'http://127.0.0.1:5000/login', json.dumps(user_data), header)
        self.assertIn('session_key', login_data) # The session key should be in the post rest call, which means the login was successful.
        session_key = login_data['session_key']
        print(login_data)

        logout_data = post_rest_call(self, 'http://127.0.0.1:5000/logout', json.dumps({'session_key': session_key}), header) # The session key should now be invalid since the logout was succesful.
        self.assertEqual(logout_data['message'], 'Logout successful') # If the message 'Logout successful' appears in the headers, the logout was succesful.
        print(logout_data)
        
    def test_api_login_wrong_password(self):
        #Setup
        user_data = {'username': 'MonseuirParis', 'password': 'royalewithcheese'}
        header = {'content-type': 'application/json'}
        post_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(user_data), header)
        wrong_data = {'username': 'MonseuirParis', 'password': 'whatsaboutburgerking?'}
        
        # Invoke
        wrong_login = post_rest_call(self, 'http://127.0.0.1:5000/login', json.dumps(wrong_data), header, expected_code=401)
        
        #Analyze
        self.assertEqual(wrong_login['message'], 'Incorrect password')
        print(wrong_login)
    
    #You can edit a users information; if you try to edit a non-existent user, the API fails
    def test_api_edit_user_username(self):
        # Setup
        old_username = 'Abbott'
        new_username = 'NewAbbott'
        edit_user_data = {'old_username': old_username, 'new_username': new_username}
        header = {'content-type': 'application/json'}

        # Invoke
        put_rest_call(self, 'http://127.0.0.1:5000/users', json.dumps(edit_user_data), header)

        # Analyze
        updated_users = get_rest_call(self, 'http://127.0.0.1:5000/users')
        self.assertTrue(any(user['username'] == new_username for user in updated_users))
        self.assertFalse(any(user['username'] == old_username for user in updated_users))
        print(updated_users)
    
    #You can list DMs
    def test_api_list_all_direct_messages(self):
        # Setup & Invoke
        expected_dms = 7
        actual_dms = get_rest_call(self, 'http://127.0.0.1:5000/messages')

        # Analyze
        self.assertEqual(expected_dms, len(actual_dms))
        print(actual_dms)
    
    #And specify a maximum number to return
    def test_api_list_5_direct_messages(self):
        # Setup
        expected_dms = 5
        
        # Invoke
        actual_dms = get_rest_call(self, 'http://127.0.0.1:5000/messages?max_messages=5')
        
        # Analyze
        self.assertEqual(expected_dms, len(actual_dms))
        print(actual_dms)
    
    #You can add a new DM
    def test_api_add_direct_message(self):
        # Setup
        new_dm_data = {
            'message': 'Dear friend. Over yonder, awaits that great big shining city.',
            'sender': 'Nikola Tesla',
            'receiver': 'Richard Feynman',
            'date': '03-15-1955',
            'time': '08:32 AM'
        }
        header = {'content-type': 'application/json'}
        
        # Invoke
        post_rest_call(self, 'http://127.0.0.1:5000/messages', json.dumps(new_dm_data), header)
        
        # Analyze
        actual_dms = get_rest_call(self, 'http://127.0.0.1:5000/messages')
        self.assertTrue(any(dm['message'] == new_dm_data['message'] for dm in actual_dms))
        print(actual_dms)