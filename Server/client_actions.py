import logging

import datetime
import json


ST_NONE = 0
ST_CONNECTED = 1
ST_CONNECTING = 2

class ClientActions:
    def __init__(self):

        self.messageTypes = {
            'connect': self.processCreate,
            'status': self.processStatus
        }

        

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
                logging.error("Invalid message format from client")
                return

            if 'result' not in req :
                if 'error' not in req:
                    logging.error( "Message has no result field")
                    return
                else:
                    logging.error(" Error message !")
                    return
            if 'seq' not in  req:
                logging.error( "Message has no sequence identifier field")
                return 

            in_seq_id = False

            for key in client.seq_id:
               
                if req['seq'] in  client.seq_id[key]:
                    self.messageTypes[key](req, client)
                    in_seq_id = True
                    break
            if(in_seq_id == False):
                logging.error("Invalid message : " + str(req['seq']) + " Should be a response to one of the messages sent!" )
                print(req)

        except Exception, e:
            logging.exception("Could not handle request")

    def processCreate(self, data, client):

        logging.debug("%s" % json.dumps(data))

        _id = data['result']
        if not isinstance(_id, int):
            logging.error( "No valid \"_id\" field in \"connect\" message: " +
                json.dumps(data))
            _seq = data['seq']
            client.seq_id["connect"].remove(_seq)
            #client.sendResult({"error": "wrong message format"})
            return

        
        _seq = data['seq']
        client.seq_id["connect"].remove(_seq)

        #_sec = data['sec']

        client.id = _id
        client.state = ST_CONNECTED
        logging.info(' Internal Id : ' + str(_id))
        
    
    def processStatus(self, data, client):
        print "System Status "
        result = data['result']
        _seq = data['seq']
        client.seq_id["status"].remove(_seq)

        print("result: ", result )

##------------------------------------------------------------------------------------------
##--------------------------------------------HANDLE OPTIONS -------------------------------
##------------------------------------------------------------------------------------------
    def handleOption(self, op, client):
        logging.debug("Handle option : "+ op +"..")
        if(op == '1'):
            logging.debug("create option..")
            self.create(client)
            logging.debug("created...")
        if op == '2' :
            logging.debug("Handle option...")
            self.status(client)

        else:
            print("BAD Option!")

        client.menu()

        
    def create(self, client):
        client.state = ST_CONNECTING                                                          
        seq  = 1
        #client.uuid = 1234
        client.seq_id["connect"] = client.seq_id["connect"] + [seq]
        message = {"type": "connect", "uuid": client.uuid, "sec": None, "seq": seq }
        client.send(message)


    ##
    ## @brief      STATUS
    ## option 8 : List messages sent and receipts
    ##
    def status(self, client):
        try:
            seq = 8
   
            message = {"type": "status", "rfid": '123456789', "knock": [1,2,4], "seq": seq }
            client.seq_id["status"] = client.seq_id["status"] + [seq]
            client.send(message)
        except Exception, e:
            print("BAD id! ")
            pass