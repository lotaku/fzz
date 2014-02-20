#encoding: utf8

import sys
sys.path.append("../common")

from server import TCPServer

tcpServer=TCPServer()
tcpServer.listen()
tcpServer.run()

