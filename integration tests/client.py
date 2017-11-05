import random, utils

class Client:
    def __init__(self):
        self.id = ''.join([str(random.randint(0, 9)) for i in range(4)])
        self.name = 'Unknown'
        self.pin = []

    def setpin(self):
        self.pin = utils.timmeKeys()
