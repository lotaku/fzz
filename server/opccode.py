#encoding: utf8

import player

handler={
    1:player.c2gsEnterWorld,
    2:player.c2gsPlayerMove,
}

def handlePacket(player,packet):
    handler[packet.id](player,packet)

