# -*- coding: utf-8 -*

'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''

import SocketServer
import json
import threading
from datetime import datetime

'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''

clients = []
#tanken bak å ha dict her er at vi har nøkkel som ip eller port og verdi brukernavn. Slik at vi senere i clienthandler vet hvilken bruker som sender de forskjellige beskjedene
#og kan ha med det i chatten som blir sendt tilbake til clientene
usernames = {} # liste over unike brukernavn som er pålogget

def broadcast_message(data):
    for client in clients:
        client.request.sendall(data.encode('utf-8'))

#lage liste over connections.
class CLientHandler(SocketServer.BaseRequestHandler):

    def check_login(self, username):
        if username in usernames.values():
            return True
        else:
            return False

    def handle(self):
        # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]

        clients.append(self)

        print 'Client connected @' + self.ip + ':' + str(self.port)


        while True:

            #Wait for data from the clients
            data = self.connection.recv(1024).strip()


            # Check if the data exists
            if not data:
                break

            data = json.loads(data)

            if (data['request']=='login'):

                for i in data['username']:
                    if not ((i>47 and i<58) or (i>64 and i<91) or (i>96 and i<122) or i==95): # Denne sjekken bør bakes inn i en funksjon. Da kan vi sjekke den med en if-setning og sende melding tilbake til klient umiddelbart uten å sjekke de senere if-setningene.
                        message='Invalid username!'
                        response = {'response': 'login', 'error': message}
                        break
                if self.check_login(data['username']):
                    message='Name already taken!'
                    response = {'response': 'login', 'error': message}


                elif self.check_login(data['username'])==False: #Sjekker om brukernavnet er tatt 
                    usernames[self.port] = (data['username'])
                    response = {'response': 'login', 'username': data['username']}

            if (data['request']=='message'):
                print(str(self.port))
                print datetime.now().strftime("%Y-%m-%d %H:%M") + ' '+ usernames[self.port] + ':  ' + data['message']
                response = {'response': 'message', 'username': usernames[self.port], 'message': data['message'], }

            #send en melding til klienten om at meldingen ble mottatt.
            data = json.dumps(response)
            #self.request.sendall(data.encode('utf-8'))

            broadcast_message(data)


            

'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9977


    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), CLientHandler)
    print("Server successfully started. Waiting for clients to connect")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
