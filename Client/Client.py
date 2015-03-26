# -*- coding: utf-8 -*-
import socket
import time
from MessageReceiver import *


class Client:

    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.message = None
        self.username = None

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):

        # Initialize connection to server. If for some reason the client cant connect, show appropiate error message.
        try:
            self.connection.connect((self.host, self.server_port))
        except socket.error, e:
            print 'Could not connect to server. Error: ' + str(e)

        self.message = MessageReceiver(self, self.connection)

        print 'Welcome to ChatBot 2031x'
        print 'Type help for help'

        # Handle login
        self.login()
        self.message.start()
        while True:
            input = raw_input('').strip()
            if input == 'logout':
                self.logout()
            elif input == 'help':
                print """Following commands are available:\n- help\n- logout\n- users [lists active users]\n- msg [start message with msg]"""

            elif input == 'users':
                self.users()
            elif input[:3] == 'msg':
                self.send_message(input[3:])

    def receive_message(self, message):

        if not message:
            print 'Invalid response'
            return

        try:
            message = json.loads(message)
        except ValueError, e:
            print e

        if message['response'] == 'login':
            if 'error' in message:
                print 'Something happend'
                self.login()
            elif self.username == message['message']:
                print 'You are now logged in as: ' + self.username
        elif message['response'] == 'message':
            print message['message']
        elif message['response'] == 'users':
            print message['message']
        elif message['response'] == 'error':
            print message['message']
            self.login()
        elif message['response'] == 'logout':
            print message['message']
        elif message['response'] == 'history':
            for i, val in enumerate(message['message']):
                print val
        else:
            print 'Something something'

    def send_payload(self, data):
        self.connection.send(data)

    def login(self):
        self.username = raw_input('Please type in your username to log in: ')
        request = json.dumps({'request': 'login', 'username': self.username})
        self.send_payload(request)

    def logout(self):
        request = json.dumps({'request': 'logout', 'username': self.username})
        self.send_payload(request)

    def users(self):
        request = json.dumps({'request': 'users', 'username': self.username})
        self.send_payload(request)

    def send_message(self, input):
        request = json.dumps({'request': 'message', 'username': self.username, 'message': input})
        self.send_payload(request)


if __name__ == '__main__':
    """52987
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
