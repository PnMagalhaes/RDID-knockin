import serial, utils

class chameleon:
    
    RESPONSE_OK_TEXT = 101
    RESPONSE_OK = 0
    RESPONSE_WAITING = 1
    RESPONSE_ERROR = 2
    RESPONSES = {RESPONSE_OK : [100,RESPONSE_OK_TEXT] , RESPONSE_WAITING : [110] , RESPONSE_ERROR : [200,201,202] }

    def __init__(self):
        self.PORT = None
        self.SERIAL = None

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
        except Exception,e:
			print "Error: Cannot open serial port: %s" % e
			return None
        return self.SERIAL

    def writing(self, command="GETUID"):
        self.SERIAL.write ( command + '\r' )
        retval = ''
        retcode = self.SERIAL.readline()
        if int(retcode.split(':')[0]) == self.RESPONSE_OK_TEXT:
            retval = self.SERIAL.readline()
        return (retcode.strip(),retval.strip())

    def read(self):
        pass

    def close(self):
        try:
            self.SERIAL.close()
        except:
            pass


if __name__ == '__main__':
    ch = chameleon()
    ch.connect()
    print(ch.writing())