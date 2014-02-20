#encoding: utf8 

from select import select
from socket import socket
from socket import AF_INET,SOCK_STREAM
from packet import RecvPacket
from player import player
from opccode import handlePacket

class TCPClient:

    def __init__(self,host="localhost",port=8888):
        self.connectSocket=socket(AF_INET,SOCK_STREAM)
        self.connectSocket.connect((host,port))
        self.connectSocket.setblocking(0)

        self.sendData=""
        self.recvData=""

    def recvPackets(self):
        reads,_,errors=select([self.connectSocket],[],[],0.0001)
        if self.connectSocket in reads:
            self.read()

    def sendPackets(self):
        _,writes,errors=select([],[self.connectSocket],[],0.0001)
        if self.connectSocket in writes:
            self.write()

    def handlePackets(self):
        for buffer in self.buffers:
            packet=RecvPacket(buffer)
            handlePacket(player,packet)
        self.buffers=[]

    def read(self):
        data=self.recvData+self.connectSocket.recv(1024)
        dataLength=len(data)

        lengthBeginIndex=0
        contentBeginIndex=2

        if dataLength>contentBeginIndex:
            contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
            packetLength=contentLength+contentBeginIndex
            while dataLength>=packetLength:
                content=data[contentBeginIndex:contentBeginIndex+contentLength]

                self.buffers.append(content)

                data=data[contentBeginIndex+contentLength:]
                dataLength=len(data)
                if dataLength>=contentBeginIndex:
                    contentLength=ord(data[lengthBeginIndex])*0x100+ord(data[lengthBeginIndex+1])
                    packetLength=contentLength+contentBeginIndex
                else:
                    break
        self.recvData=data

    def write(self):
        data=self.sendData
        amount=self.connectSocket.send(data)
        self.sendData=data[amount:]


