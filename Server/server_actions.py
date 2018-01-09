import logging
from client import *
import json
from db import *

class ServerActions:
    def __init__(self):

        self.messageTypes = {
            
            'connect': self.processCreate,
            
            'validate': self.processStatus
        }

        self.db = DataBase('/home/daniela/Documents/RFID/RDID-knockin/rfid.db')

    def handleRequest(self, s, request, client):
        """Handle a request from a client socket.
        """
        try:

            logging.info("HANDLING message from %s: %s" %
                         (client, str(request)))

            try:
                req = json.loads(request)
            except:
                logging.exception("Invalid message from client")
                client.sendResult({"error": "wrong message format"})
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

        if not set({'knock', 'rfid', 'door'}).issubset(set(data.keys())):
            logging.error( "Badly formated \"status\" message: " +
                json.dumps(data))
            client.sendResult({"error": "wrong message format", "seq": data["seq"]})
        
        knock = data['knock']

        knock = knock[:-1] # vem com uma virgula a mais

        uid = None

        if not len(str(data["rfid"])) == 14:
            uid = "0"*(14-len(str(data['rfid']))) + str(data["rfid"])
        else:
            uid = str(data["rfid"])
        door_data = data["door"]
        print('\n\n')
        print knock
        print uid

        self.db.c.execute('select _id from doors where location =? and num= ?', (door_data[1], door_data[0]) )
        client.id = self.db.c.fetchone()[0]
        #boolean

        response = self.db.validate(list_knock= knock , _pass= uid, door_id=client.id, b = door_data[2])
        if response[0] :
            client.sendResult({"type": 'validate',"result": "True", "seq": data["seq"]})
        else:
            client.sendResult({"type": 'validate', "result": response[1], "seq": data["seq"]})

