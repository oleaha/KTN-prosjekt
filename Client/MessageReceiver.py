# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        #Initialize thread
        Thread.__init__(self)
        # Flag to run thread as a deamon
        self.daemon = True
        self.client = client
        self.connection = connection
        self.status = True



    # Stop it
    def stop(self):
        self.status = False

    # Run it
    def run(self):
        while self.status:
            # Reveice data in json format
            data = self.client.recv(1024)
            # Send data to client
            self.connection.receive_message(data, self.listener)
        pass
