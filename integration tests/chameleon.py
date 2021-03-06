import sys, serial, utils, socket, time

class chameleon:
    
    RESPONSE_OK_TEXT = 101
    RESPONSE_OK = 0
    RESPONSE_WAITING = 1
    RESPONSE_ERROR = 2
    RESPONSES = {RESPONSE_OK : [100,RESPONSE_OK_TEXT] , RESPONSE_WAITING : [110] , RESPONSE_ERROR : [200,201,202] }

    def __init__(self):
        self.PORT = None
        self.SERIAL = None
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ss.bind(("", 5005))
        self.ss.settimeout(4)
        
    def setPort(self):
        '''
        :return: serial port path of the device, None if not connected
        '''
        self.PORT = utils.serial_ports()

    def connect(self):
        if self.PORT == None:
            self.setPort()
        try:
            self.SERIAL = serial.Serial(self.PORT)
        except Exception as e:
            print ("Error: Cannot open serial port: %s" % e)
            return None
        return self.SERIAL

    def writing(self,addr, command="getuid"):
        self.SERIAL.write ( command + '\r' )
        retval = ''
        retcode = self.SERIAL.readline()
        print retcode
        if int(retcode.split(':')[0]) == self.RESPONSE_OK_TEXT:
            retval = self.SERIAL.readline()
        print (retcode, retval)
        self.ss.sendto(retval.strip(), addr)
        return (retcode.strip(),retval.strip())

    def close(self):
        try:
            self.SERIAL.close()
        except:
            pass

    def loop(self):
        while True:
            data, addr = self.ss.recvfrom(1024)
            print(data)
            if "True" in data:
                print 'in'
                self.writing( addr)

    def stop(self):
        try:
            self.ss.shutdown()
            self.ss.close()
        except:
            pass

if __name__ == '__main__':
    ch = chameleon()
    while True:
        try:
            ch.connect()
            ch.loop()
        except KeyboardInterrupt:
            ch.stop()
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                break
        except:
            if ch is not (None):
                ch.stop()
        time.sleep(10)


        
'''
ch = chameleon()
ch.connect()
print(ch.writing())
'''