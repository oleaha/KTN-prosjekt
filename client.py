# -*- coding: utf-8 -*
'''
KTN-project 2013 / 2014
'''
import socket
import json
import sys
from threading import Thread
import MessageWorker
from datetime import datetime


class Client(object):

    def __init__(self):
        #instansierer en socket
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        #test om vi får kobla oss til server.
        try:
            self.connection.connect((host, port))
        #kaster exception dersom vi ikke får kobla til serveren, og avslutter programmet
        except:
            print "ERROR: Could not connect to server. Please try again later."
            sys.exit(0)

        #message variabel blir en instans av MW sin RMW
        self.message = MessageWorker.ReceiveMessageWorker(self.connection, self)
        #kjører start metoden som ligger i Thread fra før. Dette starterden nye tråden.
        self.message.start()
        print("Welcome to the server. To exit type 'exit'")
        
        loggetInn=False
        self.login()

        while True:
            message = raw_input('')

             # Lukk tilkoblingen hvis brukeren skriver "exit"
            if message == 'exit':
                self.send(json.dumps({'username': self.username, 'message': 'I\'m leaving. Goodbye!'}))
                self.connection.close()
                break

            # Konstruer et JSON objekt som som skal
            # sendes til serveren
            data = {'request': 'message', 'message': message}

            # Lag en streng av JSON-objektet
            data = json.dumps(data)
            # Send meldingen til serveren
            self.send(data.encode('utf-8'))

        self.connection.close()

    def message_received(self, message, connection):
        message = json.loads(message.decode("utf-8"))
        #print datetime.now().strftime("%Y-%m-%d %H:%M") + ' '+ message['username'] + ':  ' + message['message']
        #Håndterer hva den gjør med informasjonen som kommer tilbake fra server.
        if message['response'] =='login':
            if 'error' in message:
                    if message['error']=='Invalid username!':
                        print message['username'] + "er ikke et gyldig brukernavn. Prøv igjen."
                        #prøver et nytt brukernavn.
                        self.login()

                    elif message['error']=='Name already taken!':
                        print("Brukernavnet er allerede tatt. Prøv igjen. ")
                        #Prøver ett nytt brukernavn
                        self.login()
            elif self.username == message["username"]:
                #self.username = message['username']
                print "Bruker er logget inn. "
                loggetInn = True
                #print datetime.now().strftime("%Y-%m-%d %H:%M") + ' '+ message['username'] + ':  ' + message['message']
        elif message['response'] =='message':
            if 'error' in message: 
                #Skal bare sendes til brukeren som prøver å sende meld.
                print "du er ikke logget inn. Vi fikk denne feilmeldingen. " +message['error']
            else: 
                #Skal sendes til alle.
                print datetime.now().strftime("%Y-%m-%d %H:%M") + ' '+ message['username'] + ':  ' + message['message']
        elif message['response']=='logout':
            if 'error' in message:
                #Bruker ikke logget inn skal kun sendes til brukeren som prøver å
                #logge ut. 
                print"Du er ikke logget inn. "+ self.username
            else: 
                #Gjøre noe for å logge personen ut. 
                print "Bruker logget ut. "
                loggetInn = False
                self.logout()

    def connection_closed(self, connection):
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        pass

    def logout(self):
        request = {'request':'logout'}
        request = json.dumps(request).encode('utf-8')
        self.send(request)
        self.connection.close()

    def login(self):
        #Spør etter brukernavn
        self.username = raw_input("Please enter your desired username: ")
        #Lager json objekt. 
        request = {'request': 'login', 'username': self.username}
        request = json.dumps(request)
        #Sender til server. 
        self.send(request.encode('utf-8'))



if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9977)

