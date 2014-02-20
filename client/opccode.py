#encoding: utf8


import player

handler={
    1:player.gs2cEnterWorld,
    2:player.gs2cPlayerMove, 
}

def handlePacket(packet):
    handler[packet.id](player.player,packet)

