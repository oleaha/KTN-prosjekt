# -*- coding: utf-8 -*-
import socket
import SocketServer
import json
import sys

users = []
online_users = []


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print('Client connected! IP: ' + str(self.ip) + ' Port: ' + str(self.port))

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            if received_string:
                print(received_string)

                json_object = json.loads(received_string)

                if json_object.get('request') == 'login':
                    if self in users:
                        respone = {
                            'response': 'error',
                            'message': 'Du må logge ut før du kan logge inn igjen!'
                        }

                        self.send(json.dumps(respone))
                    else:
                        response, user = self.login(json_object)

    def login(self, object):
        username = object.get('username')


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9997
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
