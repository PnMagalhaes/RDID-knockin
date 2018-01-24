#!/usr/bin/python

import sys
from socket import *
HOST = "192.168.43.6"   # All available interfaces
PORT = 8080  # The server port
import json
s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket


s.connect((HOST, PORT)) # connect to server on the port
uid = 'uid'
knock = 'knock'
obj = '{"door": [4, "DETI", 3300], "knock": [808, 758, 0], "rfid": "040cbe82ba4881", "type": "validate", "seq": 1}'
#obj = {"type": "validate" , "rfid": uid, "knock": knock, "door": [1 ,'det8'] , "seq": 1}
#s.send(json.dumps(obj) + "\n\n" )               # send the data
s.send(obj + "\n\n" )               # send the data
print('send--> ' + str(obj))                                  
data = s.recv(64 * 1024)                 # receive up to 1K bytes
print 'recv--> ' + data


# #!/usr/bin/python{"type": "validate" , "rfid": "4090909090909" , "knock": [50,351,702,401,100,0] , "door": [4 ,103] , "seq": 1}

# #
# #  secure shell pipe module
# #

# import os
# import sys
# from socket import *


# localPortNo=8000
# maxTries=10
# blockSize=65536*16

# def createTCPSocketSSH (remoteHostname, remotePort=22, localPort=-1):
#     global localPortNo
#     if localPort == -1:
#         localPort = localPortNo
#         localPortNo = localPortNo+1
#     tryNo = 1
#     while 1:
#         command = "ssh -f -g -A -X -N -T -L%d:localhost:%d %s\n" \
#                   % (localPort, remotePort, remoteHostname)
#         result = os.system(command)
#         if result == 0:
#             break
#         localPort = localPort+1
#         tryNo = tryNo + 1
#         if tryNo == maxTries:
#             os.exit(1)


#     # create a TCP socket which connects to our ssh pipe
#     s = socket(AF_INET, SOCK_STREAM)
#     s.connect(("localhost", localPort))
#     return s

# s = createTCPSocketSSH('localhost')
# s.send('Hello world')               # send the data
# print('send--> Hello world')                                 
# data = s.recv(1024)                 # receive up to 1K bytes
# print data
