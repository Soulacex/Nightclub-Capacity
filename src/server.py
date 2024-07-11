from flask import Flask
from flask_restful import Resource, Api
from api.management import *
from api.chat_api import *
from api.authentication import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB

api.add_resource(Version, '/manage/version') #Management API for checking DB version

api.add_resource(AllUsers, '/users') #Management API for listing all users.
api.add_resource(AllCommunitiesAndChannels, '/communities') #Management API for listing all communities and channels.
api.add_resource(MessageSearch, '/messages/search') #Management API to search for a message with a specific string, start and end date.
api.add_resource(MessagesInSpecificChannel, '/channels/messages/<community_name>/<channel_name>') #Management API to list all messages in a specific channel in a community.
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(DirectMessages, '/messages')


if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)