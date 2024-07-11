import unittest
from src.db import chat
from tests.test_utils import *
from src.db import *
import urllib.parse

class TestDBSchema(unittest.TestCase):

    def setUp(self):
        """Rebuild the tables. This method will always be done before creating any tests."""
        post_rest_call(self, 'http://127.0.0.1:5000/manage/init')
        
        
    def test_db_list_all_users(self):
        #Setup & Invoke
        all_users = get_rest_call(self, 'http://127.0.0.1:5000/users') #Getting all of the tables for every single user.
        expected_users = 6
        
        #Analyze
        self.assertEqual(len(all_users), expected_users) #The length of all_users should be six as there are only six users in our DB.
        
    def test_db_list_all_comms_and_chans(self):
        #Setup & Invoke
        results = chat.list_all_communities_and_channels()
        all_comms_and_chans = get_rest_call(self, 'http://127.0.0.1:5000/communities')
        expected_comms = 2 #There are only two communities in my database Arrakis & Comedy.
        
        #Now we want to get all of the channels within the communities too. There are two per community.
        expected_chans_in_comms = {
            'Arrakis': 2,
            'Comedy': 2
        }
        
        for community in results: #Iterate through the communities in the database of all comms and chans.
            community_name = community['name'] 
            expected_chans = expected_chans_in_comms.get(community_name, 0)
            actual_chans = len(community['channels'].split(','))
            
        #Analyze
            self.assertEqual(actual_chans, expected_chans) #The number of channels within each community, which is two.
        self.assertEqual(len(all_comms_and_chans), expected_comms) #The number of communities in the whole database, which is also two.
        
    def test_db_search_for_message(self):
        #Setup
        search_results = chat.search_messages("Hello", "01-01-1922", "01-01-1992")

        #Invoke
        expected_results = [
            {
                'messageID': 1,
                'message': 'Hello Costello! How are you today?',
                'date': '06-05-1922',
                'time': '2:05 PM',
                'sender': 'Abbott',
                'receiver': 'Costello',
                'comm_name': 'Comedy',
                'chan_name': '#Dialogs'
            },
            {
                'messageID': 2,
                'message': 'Hello Abbott. Long time, no see.',
                'date': '06-05-1922',
                'time': '2:33 PM',
                'sender': 'Costello',
                'receiver': 'Abbott',
                'comm_name': 'Comedy',
                'chan_name': '#Dialogs'
            }
        ]

        #Analyze
        self.assertEqual(search_results, expected_results)

            
    def test_db_list_messages_in_channel(self):
        #Setup
        community_name = 'Comedy'
        channel_name = '#Dialogs'
        expected_messages = [
            {'messageID': 1, 'message': 'Hello Costello! How are you today?', 'date': '06-05-1922', 'time': '2:05 PM', 'sender': 'Abbott',
             'receiver': 'Costello', 'comm_name': 'Comedy', 'chan_name': '#Dialogs'},
            {'messageID': 2, 'message': 'Hello Abbott. Long time, no see.', 'date': '06-05-1922','time': '2:33 PM', 'sender': 'Costello',
             'receiver': 'Abbott', 'comm_name': 'Comedy', 'chan_name': '#Dialogs'},
        ]
        
        #Invoke
        result = chat.list_all_messages_in_specific_channel(community_name, channel_name)
        
        #Analyze
        self.assertEqual(result, expected_messages)

    def test_db_list_messages_in_empty_channel(self):
        #Setup
        community_name = 'Comedy'
        channel_name = '#Zaire'
        
        expected_messages = []
        
        #Invoke
        result = chat.list_all_messages_in_specific_channel(community_name, channel_name)
        
        #Analyze
        self.assertEqual(result, expected_messages)
        
