# -*- coding: utf-8 -*-
import socket
import MessageReceiver

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.message = ''
        self.run()

        # TODO: Finish init process with necessary code

    def run(self):

         # Connect to the server
        try:
            self.connection.connect((self.host, self.server_port))
        except socket.error, e:
            print 'Caught exception socket.error: %s' % e

        self.message = MessageReceiver.MessageReceiver(self.connection, self)
        self.message.run()

        print 'Welcome to Chat Client 9998. Type exit to exit.'

    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9997)
