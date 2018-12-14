import json
import socket
import sys
import threading

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

HOST = '127.0.0.1'


class FBA_Message:
    

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



class FBAClient(DatagramProtocol):
    def __init__(self, port):
        self.port = port
        
        self.history = list()
        self.id = 0

    def send_next(self, port):
        print('Message sent to server')
        if self.id >= len(transactions):
            return


        m = transactions[self.id]

        key, value = m.split(':')
        
        t = FBA_Message(key, value, type='init')
        data = t.__dict__

        self.id += 1
        self.start_messagethread(port, data)

    def start_messagethread(self, port, json_msg):
        t = threading.Thread(target=self.sending_msg, args=(port, json_msg,))
        t.start()

    def sending_msg(self, port, json_msg):
       # self.transport.connect(HOST, port)
        data = json.dumps(json_msg).encode()
        self.transport.write(data, (HOST, port))

    def listen(self):
        reactor.listenUDP(self.port, self)

    def startProtocol(self):
        print("Client {} started".format(self.port))

    def datagramReceived(self, data, host):
        print("received %r from %s" % (data, host))
        self.send_next(port=3000)

if __name__ == '__main__':
    client = FBAClient(port=3005) 
    client.listen()

    client.send_next(3000)
    reactor.run()
    
