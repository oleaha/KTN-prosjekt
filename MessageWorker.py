# -*- coding: utf-8 -*
'''
KTN-project 2013 / 2014
Python daemon thread class for listening for events on
a socket and notifying a listener of new messages or
if the connection breaks.

A python thread object is started by calling the start()
method on the class. in order to make the thread do any
useful work, you have to override the run() method from
the Thread superclass. NB! DO NOT call the run() method
directly, this will cause the thread to block and suspend the
entire calling process' stack until the run() is finished.
it is the start() method that is responsible for actually
executing the run() method in a new thread.
'''
from threading import Thread
import json
import client


class ReceiveMessageWorker(Thread):
    #listener er serveren vi lytter til. Type socket.socket(socket.AF_INET, socket.SOCK_STREAM) fra client
    #connection er en instans av client
    def __init__(self, listener, connection):
        #Sier at tråden er av typen som stopper ved shutdown
        self.daemeon = True
        #gir globale verdier slik av de kan brukes i de andre metodene
        self.listener = listener
        self.connection = connection
        #siden subklassen vår av Thread overrider konstruktøren må vi kalle denne
        Thread.__init__(self)
        #Lager en ny global verdi som settes til True når programmet initialiseres
        self.running = True

    def stop(self):
        #dersom metoden kalles blir variabelen False
        self.running = False

    def run(self):
        #løkka kjører til stop metoden evt. blir kalt
        while (self.running):

            #r_d tar i mot det serveren sender ut. Dette er på json format. json.dumps er brukt
            received_data = self.listener.recv(1024)

            #kaller metoden fra client. self.connection gir inn instansen av client, r_d er data på laods format, listener er serveren
            self.connection.message_received(received_data, self.listener)