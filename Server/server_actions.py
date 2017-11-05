import logging
from client import *
import json
from db import *

class ServerActions:
    def __init__(self):

        self.messageTypes = {
            
            'connect': self.processCreate,
            
            'status': self.processStatus
        }

        self.db = DataBase()

    def handleRequest(self, s, request, client):
        """Handle a request from a client socket.
        """
        try:
            logging.info("HANDLING message from %s: %r" %
                         (client, repr(request)))

            try:
                req = json.loads(request)
            except:
                logging.exception("Invalid message from client")
                return

            if not isinstance(req, dict):
                logging.error( "Invalid message format from client")
                return

            if 'type' not in req:
                logging.error( "Message has no TYPE field")
                return

            if req['type'] in self.messageTypes:
                self.messageTypes[req['type']](req, client)
            else:
                logging.error( "Invalid message type: " +
                    str(req['type']) + " Should be one of: " + str(self.messageTypes.keys()))
                client.sendResult({"error": "unknown request", "seq": data["seq"]})

        except Exception, e:
            logging.exception("Could not handle request")

    def processCreate(self, data, client):
        logging.debug( "RECEIVED :%s" % json.dumps(data))

        if 'uuid' not in data.keys():
            logging.error( "No \"uuid\" field in \"create\" message: " +
                json.dumps(data))
            client.sendResult({"error": "wrong message format", "seq": data["seq"]})
            return

        client.sendResult({"result": True, "seq": data["seq"]})

    

    def processStatus(self, data, client):
        logging.debug( "%s" % json.dumps(data))

        if not set({'knock', 'rfid'}).issubset(set(data.keys())):
            logging.error( "Badly formated \"status\" message: " +
                json.dumps(data))
            client.sendResult({"error": "wrong message format", "seq": data["seq"]})
        
        knock = data['knock']
        
        rfid = data["rfid"]

        
        #boolean
        response = self.db.validate(knock, rfid)
        client.sendResult({"result": response, "seq": data["seq"]})

