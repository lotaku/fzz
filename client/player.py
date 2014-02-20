#encoding: utf8

from packet import SendPacket

class Player:

    def __init__(self):
        pass

    def create(self,name):
        self.name=name
        self.x=1
        self.y=1

    def enterWorld(self,x,y):
        self.x=x
        self.y=y

    def move(self,x,y):
        self.x=x
        self.y=y

    def c2gsEnterWorld(self):
        packet=SendPacket(1)
        packet.packString(self.name)
        packet.send()

    def c2gsPlayerMove(self,x,y):
        packet=SendPacket(2)
        packet.packInt(x,1)
        packet.packInt(y,1)
        packet.send()

player=Player()

def gs2cEnterWorld(player,packet):
    x=packet.unpackInt()
    y=packet.unpackInt()
    player.enterWorld(x,y)

def gs2cPlayerMove(player,packet):
    x=packet.unpackInt(1)
    y=packet.unpackInt(1)
    player.move(x,y)

