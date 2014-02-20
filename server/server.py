#encoding: utf8 

from select import select
from socket import socket
from socket import AF_INET,SOCK_STREAM

from packet import RecvPacket

from opccode import handlePacket
from player import Player
from player_manager import playerManager

class TCPServer:

    def __init__(self,host="localhost",port=8888):
        self.listenSocket=socket(AF_INET,SOCK_STREAM)
        self.listenSocket.setblocking(0)

        self.remoteSockets=[]
        self.remoteData={}
        self.buffers={}

    def listen(self): 
        self.listenSocket.bind(("localhost",8888))
        self.listenSocket.listen(11)

    def run(self): 
        while True:
            reads,writes,errors=select([self.listenSocket]+self.remoteSockets,self.remoteSockets,[],0.0001)

            for read in reads: 
                if read is self.listenSocket:
                    self.acceptConnection() 
                else: 
                    self.readRemoteData(read) 
            self.handlePackets()

            for write in writes:
                self.writeRemote(write)

    def handlePackets(self):
        for remote,buffers in self.buffers:
            player=remote.player
            for buffer in buffers:
                packet=RecvPacket(buffer)
                handlePacket(player,packet)
        self.buffers=[]

    def acceptConnection(self):
        remote,address=self.listenSocket.accept()
        player=Player(remote)
        playerManager.add(player)
        remote.player=player
        remote.sendPackets=[]
        self.remoteSockets.append(remote)

    def readRemoteData(self,readSocket): 
        #packet = length(2 byte) + content(length byte)
        data=self.remoteData.get(readSocket,"")+readSocket.recv(1024)
        dataLength=len(data)

        lengthBeginIndex=0
        contentBeginIndex=2

        if dataLength>contentBeginIndex:
            contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
            packetLength=contentLength+contentBeginIndex
            while dataLength>=packetLength:
                content=data[contentBeginIndex:contentBeginIndex+contentLength]

                self.buffers.get(readSocket,[]).append(content)

                data=data[contentBeginIndex+contentLength:]
                dataLength=len(data)
                if dataLength>=contentBeginIndex:
                    contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
                    packetLength=contentLength+contentBeginIndex
                else:
                    break
        self.remoteData[readSocket]=data

    def writeRemote(self,writeSocket):
        data=writeSocket.sendData
        amount=writeSocket.write(data)
        writeSocket.sendData=data[amount:]


#import ptrace; ptrace.traceModule()
