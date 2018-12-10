import json
import socket
import sys
import threading

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

HOST = '127.0.0.1'


class FBATransaction:
    INIT = "init"
    COMMIT = "commit"
    VOTE = "vote"

    def __init__(self, key, value, type=None):
        #self.id = id
        self.key = key
        self.value = value
        self.type = type


CLIENT_PORT = 3005

transactions = [
    "foo:$10",
    "bar:$30",
    "foo:$20",
    "bar:$20",
    "foo:$30",
    "bar:$10"

    ]



class FBAClientV1(DatagramProtocol):
    def __init__(self, port):
        self.port = port
        
        self.history = list()
        self.id = 0

    def send_next(self, c_port):
        print('Message sent to server')
        if self.id >= len(transactions):
            return


        m = transactions[self.id]

        key, value = m.split(':')
        
        t = FBATransaction(key, value, type='init')
        data = t.__dict__

        self.id += 1
        self.send_msg(c_port, data)

    def send_msg(self, c_port, s_json):
        t = threading.Thread(target=self._send_msg, args=(c_port, s_json,))
        t.start()

    def _send_msg(self, c_port, s_json):
       # self.transport.connect(HOST, c_port)
        data = json.dumps(s_json).encode()
        self.transport.write(data, (HOST, c_port))

    def mainloop(self):
        reactor.listenUDP(self.port, self)

    def startProtocol(self):
        print("Client {} started".format(self.port))

    def datagramReceived(self, data, host):
        print("received %r from %s" % (data, host))
        self.send_next(c_port=3000)

if __name__ == '__main__':
    c = FBAClientV1(port=3005) 
    c.mainloop()

    c.send_next(3000)
    reactor.run()
    
