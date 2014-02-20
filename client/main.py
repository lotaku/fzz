#encoding: utf8 

from tcpclient import TCPClient

class Client:

    def __init__(self):
        self.net=TCPClient()

    def loop(self):
        while True:
            self.net.recvPackets()
            self.net.handlePackets()
            self.handleEvents() 
            self.render()
            self.net.sendPackets()

    def handleEvents(self):
        pass

    def render(self):
        pass

client=Client()
client.mainLoop()