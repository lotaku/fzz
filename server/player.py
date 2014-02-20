#encoding: utf8

from packet import SendPacket

class Player:

    def __init__(self,socket):
        self.socket=socket

    def create(self,name):
        self.name=name
        self.x=1
        self.y=1

    def enterWorld(self):
        self.gs2cEnterWorld()

    def gs2cEnterWorld(self):
        packet=SendPacket(1)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.send(self)

    def move(self,newX,newY):
        self.x=newX
        self.y=newY
        self.gs2cPlayerMove()

    def gs2cPlayerMove(self):
        packet=SendPacket(1)
        packet.packInt(self.x)
        packet.packInt(self.y)
        packet.send(self) #TODO 

def c2gsEnterWorld(player,packet):
    name=packet.unpackString()
    player.create(name)
    player.enterWorld()

def c2gsPlayerMove(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.move(x,y)

import ptrace; ptrace.traceModule()
