from datetime import datetime
import os
import secrets
from .swen344_db_utils import *
from flask import *
import hashlib


def rebuild_tables():
    exec_sql_file('src/db/chat.sql')

#List All Users
def list_all_users():
    """
    This method lists all of the users within the user_table in the sql system.
    Parameters:
        None
    Returned:
        All of the rows in the user table. Essentially, all of the users in the system.
    """
    users = exec_get_all("""SELECT * FROM user_table""")
        
    all_users = []
    for user in users:
        a_user = {
            'ID': user[0],
            'username': user[1],
            'password': user[2],
            'session_key': user[3]
        }
        all_users.append(a_user)
    return all_users

#List All Communities and Channels
def list_all_communities_and_channels():
    """
    This method lists all of the communities and channels within the database.
    Parameters:
        None.
    Returned:
        All of the related data to all the communities and channels.
    """
    comms_and_chans = exec_get_all("""SELECT * FROM community_table""")
    
    all_coms_and_chans = []
    for comm_and_chan in comms_and_chans:
        a_comm_and_a_chan = {
            'name': comm_and_chan[0],
            'users': comm_and_chan[1],
            'channels': comm_and_chan[2]
        }
        all_coms_and_chans.append(a_comm_and_a_chan)
    return all_coms_and_chans

#Search for messages
def search_messages(string, start_date, end_date):
    """
    Arguments:
        string (string): The specific string I want to find in the messages.
        start_date (string): The start date of the when the message, which contains the string, was posted.
        end_date (string): The end date of the when the message, which contains the string, was posted.
    Returned:
        The message(s) that match the search criteria.
    """
    start_date = datetime.strptime(start_date, '%m-%d-%Y')
    end_date = datetime.strptime(end_date, '%m-%d-%Y')

    messages = exec_get_all("""SELECT * FROM message_table WHERE message LIKE %s 
                            AND TO_DATE(date, 'MM-DD-YYYY') BETWEEN %s AND %s""",
                            (f'%{string}%', start_date, end_date))    
    all_messages = []
    for message in messages:
        a_message = {
            'messageID': message[0],
            'message': message[1],
            'date': message[2],
            'time': message[3],
            'sender': message[4],
            'receiver': message[5],
            'comm_name': message[6],
            'chan_name': message[7]
        }
        all_messages.append(a_message)
    
    return all_messages

#List all messages in a particular channel
def list_all_messages_in_specific_channel(community_name, channel_name):
    """
    This method is meant to list all of the messages in a specific channel in our communities.
    Argument:
        channel_name (string): The name of the specific channel, which would be its identifier..
    Returned:
        All of the messages in that specific channel.
    """
    messages_in_specific_chan = exec_get_all("""SELECT * FROM message_table 
                        WHERE comm_name = %s AND chan_name = %s;""", (community_name, channel_name))
    
    all_messages_in_specific_chan = []
    for message in messages_in_specific_chan:
        a_message = {
            'messageID': message[0],
            'message': message[1],
            'date': message[2],
            'time': message[3],
            'sender': message[4],
            'receiver': message[5],
            'comm_name': message[6],
            'chan_name': message[7]
        }
        all_messages_in_specific_chan.append(a_message)
    return all_messages_in_specific_chan

def create_user(username, password, session_key):
    """
    This method creates a new user.
    Arguments:
        username : The new username for the user
        password : The new password for the user
        session_key : The secure session key for the user
    Returns:
        None
    """
    conn = connect()
    cur = conn.cursor()
    
    existing_user = exec_get_all("SELECT * FROM user_table WHERE username = %s", (username,))
    if existing_user:
            return {'message': 'User Already Exists'}, 400

    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    cur.execute("INSERT INTO user_table(username, password, session_key) VALUES (%s, %s, %s);",
                (username, hashed_password, session_key))

    conn.commit()
    conn.close()
    
def update_user(old_username, new_username):  
    """
    This method updates the user's name.
    Argument:
        old_username (string): The original name of the user.
        new_username (string): The new name of the user.
    Returned:
        Nothing. The name of the user is just updated.
    """
    existing_user = exec_get_all("SELECT * FROM user_table WHERE username = %s", (old_username,))
    if not existing_user:
        return

    exec_commit("UPDATE user_table SET username = %s WHERE username = %s", (new_username, old_username))
    

def delete_user(username):
    """
    This method deletes a user from the database.
    Argument:
        username (string): The name of user to be deleted.
    Returned:
        Nothing. The user is deleted via SQL.
    """
    existing_user = exec_get_all("SELECT * FROM user_table WHERE username = %s", (username,))
    if not existing_user:
        return 

    exec_commit("DELETE FROM user_table WHERE username = %s", (username,))

    
def format_messages(messages):
    """
    This method helps to format messages into a more readable format.
    Argument:
        messages (string): The messages to be formatted.
    Returned:
        The formatted message(s).
    """
    formatted_messages = []
    for message in messages:
        formatted_message = {
            'message': message[0],
            'date': message[1],
            'time': message[2],
            'sender': message[3],
            'receiver': message[4]
        }
        formatted_messages.append(formatted_message)

    return formatted_messages     
    
def list_all_direct_messages(max_messages=None):
    """
    This method lists all direct messages from the dm_table.
    Argument:
        max_messages: Maximum number of messages to return
    Returned: 
        DMs with max number.
    """
    if max_messages is not None:
        messages = exec_get_all(f"SELECT * FROM dm_table LIMIT {max_messages}")
    else:
        messages = exec_get_all("SELECT * FROM dm_table")

    return format_messages(messages)


def add_direct_message(message, sender, receiver, date=None, time=None):
    """
    This method adds a new direct message to the dm_table.
    Arguments:
        message (string): The message to be added to the database.
        sender (string): The sender of the message.
        receiver (string): The receipent of the message.
        date (string): The date (MM-DD-YEAR) of the sent message.
        time (string): The time (H:M AM/PM) of sent message.
    """
    conn = connect()
    cur = conn.cursor()
    
    if date is None:
            date = datetime.date.today().strftime('%m-%d-%Y')  
    if time is None:
            time = datetime.datetime.now().strftime('%I:%M %p') 

    cur.execute("""
        INSERT INTO dm_table(message, date, time, sender, receiver)
        VALUES (%s, %s, %s, %s, %s);
    """, (message, date, time, sender, receiver))
    
    conn.commit()
    conn.close()

def login_user(username, password):
    """
    This method helps login a user.
    Arguments:
        username (string): Name of the user.
        password (string): Password of the user.
    Returned:
        The message of the http request and its status code (assuming the login was successful).
    """
    hashed_password = hashlib.sha512(password.encode()).hexdigest()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT password FROM user_table WHERE username = %s", (username,))
    stored_password = cur.fetchone()[0]
    
    if stored_password != hashed_password:
        return {'message': 'Incorrect password'}, 401

    session_key = hashlib.sha512(secrets.token_bytes(32)).hexdigest()

    cur.execute("UPDATE user_table SET session_key = %s WHERE username = %s", (session_key, username))
    
    conn.commit()
    conn.close()

    return {'session_key': session_key}, 200

def logout_user(session_key):
    """
    This method helps logout a user.
    Argument:
       session_key (string): The session key of the user
    Returned:
        The message of the http request and its status code (assuming the logout was successful).
    """
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("UPDATE user_table SET session_key = NULL WHERE session_key = %s", (session_key,))
    
    conn.commit()
    conn.close()

    return {'message': 'Logout successful'}, 200
