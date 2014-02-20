

from packet import RecvPacket
from packet import SendPacket

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
