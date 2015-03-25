# -*- coding: utf-8 -*-
from threading import Thread
import json

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

        # Flag to run thread as a deamon
        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection
        self.status = True

    # Run it
    def run(self):
        while self.status:
            data = self.connection.recv(4096)
            if data:
                self.client.receive_message(data)

    # Stop it
    def stop(self):
        self.status = False


