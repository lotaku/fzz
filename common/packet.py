#encoding: utf8

class RecvPacket:

    def __init__(self,buffer):
        self.buffer=buffer
        self.currentIndex=0

    def unpackInt(self):
        index=self.currentIndex
        value=ord(self.buffer[index])*0x100+ord(self.buffer[index+1])
        self.currentIndex+=2
        return value

    def unpackString(self):
        length=self.unpackInt()
        string=self.buffer[self.currentIndex:self.currentIndex+length]
        self.currentIndex+=length
        return string

class SendPacket:

    def __init__(self):
        self.buffer=""

    def packInt(self,value):
        self.buffer+=chr(value/0x100)+chr(value%0x100)

    def packString(self,text):
        self.packInt(len(text))
        self.buffer+=text

x=SendPacket()
x.packInt(100)
x.packInt(12120)
x.packString("cjt")
x.packInt(65535)
x.packString("caijietao")

y=RecvPacket(x.buffer)
print y.unpackInt()
print y.unpackInt()
print y.unpackString()
print y.unpackInt()
print y.unpackString()
