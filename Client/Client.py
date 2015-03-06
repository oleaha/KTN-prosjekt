# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

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

        self.message = MessageReceiver.MessageReceiver(self, self.connection)
        self.message.start()

        print 'Welcome to ChatBot 2031x'
        print 'Type "exit" to log out'

        # Handle login
        self.username = raw_input('Please type in your username to log in: ')
        self.login()




    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        message = json.load(message)

        if message['response'] == 'login':
            if 'error' in message:
                print 'Something happend'
                self.login()
            elif self.username == message['username']:
                print 'You are now logged in as: ' + self.username
        else:
            print 'Fuckme right'

    def send_payload(self, data):
        self.connection.sendall(data)

    def login(self):
        request = json.dumps({'request': 'login', 'username': self.username})
        self.send_payload(request)



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
