#encoding: utf8 

import sys
sys.path.append("../common")

from tcp_client import tcpClient
from player import player

class Client:

    def __init__(self):
        tcpClient.connect()
        player.create("fzz")
        player.c2gsEnterWorld()
        player.c2gsEnterWorld()

    def loop(self):
        while True:
            tcpClient.recvPackets()
            tcpClient.handlePackets()
            self.handleEvents() 
            self.render()
            tcpClient.sendPackets()

    def handleEvents(self):
        pass

    def render(self):
        pass

client=Client()
client.loop()
