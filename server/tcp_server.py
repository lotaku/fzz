#encoding: utf8 

from select import select
from socket import socket
from socket import AF_INET,SOCK_STREAM
from socket import SOL_SOCKET,SO_REUSEADDR 
from packet import RecvPacket

from opccode import handlePacket
from player import Player
from player_manager import playerManager

class TCPServer:

    def __init__(self,host="localhost",port=8888):
        self.listenSocket=socket(AF_INET,SOCK_STREAM)
        self.listenSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.listenSocket.setblocking(0)

        self.remoteSockets=[]
        self.remoteData={}
        self.buffers={}

    def listen(self): 
        self.listenSocket.bind(("localhost",8888))
        self.listenSocket.listen(11)

    @trace
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
        #if self.buffers:
        #    import pdb; pdb.set_trace()
        for remote,buffers in self.buffers.items():
            player=playerManager.get(remote)
            for buffer in buffers:
                packet=RecvPacket(buffer)
                handlePacket(player,packet)
        self.buffers={}

    @trace
    def acceptConnection(self):
        remote,address=self.listenSocket.accept()
        player=Player(remote)
        player.sendData=""
        playerManager.add(player)
        self.remoteSockets.append(remote)

    def readRemoteData(self,readSocket): 
        #packet = length(2 byte) + content(length byte)
        data=self.remoteData.get(readSocket,"")+readSocket.recv(1024)
        dataLength=len(data)
        
        print "recv"
        for char in data:
            print "\t",ord(char)

        lengthBeginIndex=0
        contentBeginIndex=2

        if dataLength>contentBeginIndex:
            contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
            packetLength=contentLength+contentBeginIndex
            while dataLength>=packetLength:
                content=data[contentBeginIndex:contentBeginIndex+contentLength]

                self.buffers.setdefault(readSocket,[]).append(content)

                data=data[contentBeginIndex+contentLength:]
                dataLength=len(data)
                if dataLength>=contentBeginIndex:
                    contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
                    packetLength=contentLength+contentBeginIndex
                else:
                    break
        self.remoteData[readSocket]=data

        print self.buffers

    def writeRemote(self,writeSocket):
        player=playerManager.get(writeSocket)
        data=player.sendData
        amount=writeSocket.send(data)
        player.sendData=data[amount:]


#import ptrace; ptrace.traceModule()
