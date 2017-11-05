#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import logging
import json
import sys
from client_actions import * 
import uuid
from select import *

BUFSIZE = 512 * 1024
TERMINATOR = "\n\n"
MAX_BUFSIZE = 64 * 1024

sys.tracebacklimit = 30

HOST = ""   # All available interfaces
PORT = 8080  # The server port
             # 
ST_NONE = 0
ST_CONNECTED = 1
ST_CONNECTING = 2

class Client:
    count = 0

    def __init__(self, socket, addr):
        self.socket = socket
        self.bufin = ""
        self.bufout = ""
        self.addr = addr
        self.id = None
        self.sa_data = None

        self.actions = ClientActions()
        self.state = 0

        self.seq_id = {"connect": [] , "status": [] }
        self.uuid = 12345 #TODO

    def __str__(self):
        """ Converts object into string.
        """
        return "Client(id=%r uuid:%s)" % (self.id, str(self.uuid))

    def asDict(self):
        return {'id': self.id}

    def __str__(self):
        """ Converts object into string.
        """
        return "Client(id=%r  )" % (self.id)

    ##
    ## @brief      unique identifier for sequence id on messages
    ## @return     uuid
    ##
    def uuid(self):
        return uuid.uuid4()

    def close(self):
        """Shuts down and closes this client's socket.
        Will log error if called on a client with closed socket.
        Never fails.
        """
        logging.info( "Client.close(%s)" % self)
        try:
            self.socket.close()
        except:
            logging.exception("Client.close(%s)" % self)

    def parseReqs(self, data):
        """Parse a chunk of data from this client.
        Return any complete requests in a list.
        Leave incomplete requests in the buffer.
        This is called whenever data is available from client socket."""

        if len(self.bufin) + len(data) > MAX_BUFSIZE:
            logging.error( "Client (%s) buffer exceeds MAX BUFSIZE. %d > %d" %
                (self, len(self.bufin) + len(data), MAX_BUFSIZE))
            self.bufin = ""

        self.bufin += data
        reqs = self.bufin.split(TERMINATOR)
        print reqs
        self.bufin = reqs[-1]
        return reqs[:-1]

    def sendResult(self, obj):
        """Send an object to this client.
        """
        try:
            self.bufout += json.dumps(obj) + TERMINATOR
        except:
            # It should never happen! And not be reported to the client!
            logging.exception("Client.send(%s)" % self)

        
    def menu(self):
        print('Choose an option:')
        print('[ 1 ] Connect to server')
        print('[ 2 ] Validate User')
        
        


    def loop(self):
        while True:
            # sockets to select for reading: (the server socket + every open
            # client connection)
            rlist = [self.socket , sys.stdin, ]

            # sockets to select for writing: (those that have something in bufout)
            if len(self.bufout)>0:
                wlist = [ self.socket , ]
            else:
                wlist = []


            (rl, wl, xl) = select(rlist, wlist, rlist)

            # Deal with incoming data:
            for s in rl:
                if s is self.socket:
                    self.flushin()
                elif s == sys.stdin :
                    # Informação recebida do teclado
                    data = sys.stdin.readline()

                    self.actions.handleOption( data[0], self) #udp_s.sendto(data, server_addr)
                    
                else: #nunca vai acontecer pois o cliente ja morreu
                    log(logging.ERROR,
                        "Incoming, but %s not in clients anymore" % s)

            # Deal with outgoing data:
            for s in wl:
                #if s in self.clients:
                self.flushout()
                #else:
                #    log(logging.ERROR,
                #        "Outgoing, but %s not in clients anymore" % s)

            # for s in xl:
            #     log(logging.ERROR, "EXCEPTION in %s. Closing" % s)
            #     self.delClient(s)


    

    def send(self, obj):
        """Send an object to the server.
        """
        try:
            self.bufout += json.dumps(obj) + TERMINATOR
        except:
            # It should never happen! And not be reported to the client!
            logging.exception("Client.send(%s)" % self)

    def flushin(self):
        """Read a chunk of data from this client.
        Enqueue any complete requests.
        Leave incomplete requests in buffer.
        This is called whenever data is available from client socket.
        """
        
        data = None
        try:
            data = self.socket.recv(BUFSIZE)
            logging.debug(
                "Received data from server. Message:\n%r" % data)
        except:
            logging.exception("flushin: recv()" )
            logging.error("Received invalid data from server. Closing")
            
        else:
            if len(data) > 0:
                reqs = self.parseReqs(data)
                for req in reqs:
                    self.actions.handleRequest(self.socket, req, self)
            else:
                #self.delClient(s)
                pass

    def flushout(self):
        """Write a chunk of data to server.
        This is called whenever client socket is ready to transmit data."""
        # if not in a state of sending messages:
        #     return

        
        try:
           
            sent = self.socket.send(self.bufout[:BUFSIZE])
            logging.debug("Sent " + str(sent) + " bytes to server. Message:\n"+ str(self.bufout[:sent]) )
            # leave remaining to be sent later
            self.bufout = self.bufout[sent:]
        except:
            logging.exception("flushout: send()")
            logging.error("Cannot write to server. Closing")
            
