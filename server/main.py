#encoding: utf8

import sys
sys.path.append("../common")

from tcp_server import TCPServer

import ptrace

tcpServer=TCPServer()
tcpServer.listen()
tcpServer.run()

