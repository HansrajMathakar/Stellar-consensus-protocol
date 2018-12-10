
import json
import socket
import sys
import time
from database import Database
import threading
from utils import *
import uuid
from algorithms import FBABallot
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

neighbouring_nodes = [3000,3001,3002,3003]

# Number of quorums required for consensus
HOST = '127.0.0.1'



LIMIT = 2



class FBATransaction:
    INIT = "init"
    COMMIT = "commit"
    VOTE = "vote"

    def __init__(self, id, key, value, type=None):
        self.id = id
        self.key = key
        self.value = value
        self.type = type




class FBAServer(DatagramProtocol):
    def __init__(self, port):
        self.port = int(port)

        #self.quorum = QUORUMS[self.port]
        self.db = Database(name="assignment3_{}.db".format(self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', self.port)
        self.history = list()
        self.init_vote = dict()
        self.ballot = FBABallot()

    def startProtocol(self):
        print("Server {} started".format(self.port))

    def _send_msg(self, c_port, s_json):
       # self.transport.connect(HOST, c_port)
        data = json.dumps(s_json).encode()
        self.transport.write(data, (HOST, c_port))

    def send_msg(self, c_port, s_json):
        t = threading.Thread(target=self._send_msg, args=(c_port, s_json,))
        t.start()

    def mainloop(self):
        reactor.listenUDP(self.port, self)

    def broadcast(self, s_json):
        for port in neighbouring_nodes:
            if(port!=self.port):
                self._send_msg(int(port), s_json)

    def datagramReceived(self, data, host):

        print("received %r from %s" % (data, host))
        message = json.loads(data)
        if message in self.history:
            return

        self.history.append(message)
        
        if message['type'] == 'init' and self.port==3000:
            
            self.broadcast(message)

        if message['key'] not in self.init_vote:
            self.init_vote[message['key']] = message['value']
            t = FBATransaction(str(uuid.uuid1()), message['key'], message['value'], FBAStates.Initial_Voting)
            self.broadcast(t.__dict__)

        elif message['value'] != self.init_vote[message['key']]:
            self.init_vote[message['key']] = message['value']
            st = FBATransaction(str(uuid.uuid1()), message['key'], message['value'], FBAStates.Initial_Voting)
            self.broadcast(st.__dict__)

        elif message['type'] == FBAStates.Initial_Voting:

            self.ballot.append(message['key'], message['value'])

            if len(self.ballot.get(message['key'])) >= LIMIT:
                val = self.db.get(message['key'])
                #print(val)
                most_often = self.ballot.most_often(message['key'])
                #print(most_often)

                if val!=False:
                    amt = int(val[1:])+ int(most_often[1:])
                    updated_amount = '$'+str(amt)
                    #print(updated_amount)
                # Commit the msgs to the database
                    self.db.set(message['key'], updated_amount)
                else:
                    self.db.set(message['key'], most_often)
                

                print("Server: {} database snapshot: {}".format(self.port, str(self.db.snapshot())))
                
                if(self.port==3000):
                    self._send_msg(3005, "Transaction accepted")
                self.db.dump()
                self.ballot = FBABallot()

if __name__ == '__main__':

    
    s = FBAServer(sys.argv[1])
    s.mainloop()

    reactor.run()
