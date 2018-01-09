#!/usr/bin/env python2.7
# encoding: utf-8

from socket import *
from select import *
import json
import sys
import time
import logging

from client import *

from server_actions import *
print('[INFO] ip: ',str(sys.argv[1]).split('/')[0])
# Server address
HOST = str(sys.argv[1]).split('/')[0]   # All available interfaces
PORT = 8080  # The server port

BUFSIZE = 512 * 1024
TERMINATOR = "\n\n"
MAX_BUFSIZE = 64 * 1024



class Server:

    def __init__(self, host, port):
        self.ss = socket(AF_INET, SOCK_STREAM)  # the server socket (IP \ TCP)
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ss.bind((host, port))
        self.ss.listen(10)
        logging.info("Secure IM server listening on %s" %
            str(self.ss.getsockname()))

        
        self.server_actions = ServerActions()

        # clients to manage (indexed by socket and by name):
        self.clients = {}       # clients (key is socket)

    def stop(self):
        """ Stops the server closing all sockets
        """
        logging.info("Stopping Server")
        try:
            self.ss.close()
        except:
            logging.exception("Server.stop")

        for csock in self.clients:
            try:
                self.clients[csock].close()  # Client.close!
            except:
                # this should not happen since close is protected...
                logging.exception("clients[csock].close")

        # If we delClient instead, the following would be unnecessary...
        self.clients.clear()

    def addClient(self, csock, addr):
        """Add a client connecting in csock."""
        if csock in self.clients:
            logging.error("Client NOT Added: %s already exists" %
                self.clients[csock])
            return

        client = Client(csock, addr)
        self.clients[client.socket] = client
        logging.debug("Client added: %s" % client)

    def delClient(self, csock):
        """Delete a client connected in csock."""
        if csock not in self.clients:
            logging.error("Client NOT deleted: %s not found" %
                self.clients[csock])
            return

        client = self.clients[csock]

        del self.clients[client.socket]
        client.close()
        logging.debug("Client deleted: %s" % client)

    def accept(self):
        """Accept a new connection.
        """
        try:
            csock, addr = self.ss.accept()
            self.addClient(csock, addr)
        except:
            logging.exception("Could not accept client")

    def flushin(self, s):
        """Read a chunk of data from this client.
        Enqueue any complete requests.
        Leave incomplete requests in buffer.
        This is called whenever data is available from client socket.
        """
        client = self.clients[s]
        data = None
        try:
            data = s.recv(BUFSIZE)
            logging.debug("Received data from %s. Message:\n%r" % (client, data))

        except Exception as e:
            logging.exception("flushin: recv(%s)" % client)
            self.delClient(s)
        else:
            if len(data) > 0:
                logging.debug( "Handle Resquest .. %d" % len(data))
                reqs = client.parseReqs(data)
                logging.debug("Handle Resquest .. %d" % len(reqs))
                for req in reqs:
                    logging.debug( "Handle Resquest")
                    self.server_actions.handleRequest(s, req, self.clients[s])
            else:
                self.delClient(s)

    def flushout(self, s):
        """Write a chunk of data to client.
        This is called whenever client socket is ready to transmit data."""
        if s not in self.clients:
            return

        client = self.clients[s]
        try:
            sent = client.socket.send(client.bufout[:BUFSIZE])
            logging.debug( "Sent %d bytes to %s. Message:\n%r" %
                (sent, client, client.bufout[:sent]))
            # leave remaining to be sent later
            client.bufout = client.bufout[sent:]
        except:
            logging.exception("flushout: send(%s)", client)
            # logging.error("Cannot write to client %s. Closing", client)
            self.delClient(client.socket)

    def loop(self):
        while True:
            # sockets to select for reading: (the server socket + every open
            # client connection)
            rlist = [self.ss] + self.clients.keys()

            # sockets to select for writing: (those that have something in
            # bufout)
            wlist = [sock for sock in self.clients if len(
                self.clients[sock].bufout) > 0]

            (rl, wl, xl) = select(rlist, wlist, rlist)

            # Deal with incoming data:
            for s in rl:
                if s is self.ss:
                    self.accept()
                elif s in self.clients:
                    self.flushin(s)
                else:
                    logging.error(
                        "Incoming, but %s not in clients anymore" % s)

            # Deal with outgoing data:
            for s in wl:
                if s in self.clients:
                    self.flushout(s)
                else:
                    logging.error(
                        "Outgoing, but %s not in clients anymore" % s)

            for s in xl:
                logging.error( "EXCEPTION in %s. Closing" % s)
                self.delClient(s)




if __name__ == "__main__":
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, formatter=logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))

    serv = None
    while True:
        try:
            logging.info( "Starting Secure IM Server v1.0")
            serv = Server(HOST, PORT)
            serv.loop()
        except KeyboardInterrupt:
            serv.stop()
            try:
                logging.info("Press CTRL-C again within 2 sec to quit")
                time.sleep(2)
            except KeyboardInterrupt:
                logging.info( "CTRL-C pressed twice: Quitting!")
                break
        except:
            logging.exception("Server ERROR")
            if serv is not (None):
                serv.stop()
            time.sleep(10)
