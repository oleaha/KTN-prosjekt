# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time

connected_clients = []
online_usernames = {}

messages = []


# Helper methods #
def login(username):
    if username in online_usernames.values():
        return False
    return True


def get_datetime():
    return str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))


class Bcolors:
    SYSTEM = '\033[91m'
    USER = '\033[92m'
    ENDC = '\033[0m'


class ClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        connected_clients.append(self)
        print 'Client connected! ' + self.ip + ':' + str(self.port)

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if not received_string:
                break
            data = json.loads(received_string)

            if data['request'] == 'login':
                self.handle_login(data)
            elif data['request'] == 'logout':
                self.handle_logout(data)
            elif data['request'] == 'users':
                self.handle_users()
            elif data['request'] == 'message':
                self.handle_message(data)

    # Validate login and send response
    def handle_login(self, data):
        # Make sure that the user is NOT logged in
        if login(data['username']):
            online_usernames[self.port] = data['username']
            self.make_package('login', data['username'])
            time.sleep(0.1)
            self.connection.sendall(json.dumps({'response': 'history', 'message': messages}))
            time.sleep(0.1)
            message = Bcolors.SYSTEM + get_datetime() + ' - system : ' + data['username'] + ' joined the channel' + Bcolors.ENDC
            self.make_package('message', message)
            messages.append(message)

        else:
            self.make_package('error', Bcolors.SYSTEM + '##FAIL: Username already exists ##' + Bcolors.ENDC)

    # Handle logout the correct way
    def handle_logout(self, data):
        # Make sure the client is logged in
        if not login(data['username']):
            # Broadcast logout message
            message = Bcolors.SYSTEM + get_datetime() + ' - system : ' + data['username'] + ' left the channel' + Bcolors.ENDC
            self.make_package('logout', message)
            messages.append(message)
            # Delete client from online users list
            del online_usernames[self.port]
            print 'Client disconnected! ' + self.ip + ':' + str(self.port)
            # Remove client from connected clients to avoid unexpected shutdown
            connected_clients.remove(self)

    # Handle the list of online users
    def handle_users(self):
        users = Bcolors.SYSTEM + get_datetime() + ' - system : online users - '
        for i in online_usernames:
            users += online_usernames[i] + ', '
        users += Bcolors.ENDC
        self.make_package('users', users)

    # Handle incoming messages
    def handle_message(self, data):
        message = get_datetime() + ' - ' + data['username'] + ': ' + data['message']
        self.make_package('message', message)
        messages.append(message)

    def make_package(self, response, message):
        self.broadcast(json.dumps({'response': response, 'message': message}))

    #When a new message is added, send this to all clients
    def broadcast(self, response):
        for client in connected_clients:
            client.request.sendall(response)


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
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
