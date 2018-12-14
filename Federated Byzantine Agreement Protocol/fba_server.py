
import json
import socket
import sys
import time
from database import Database
import threading



from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

quorum = [3000,3001,3002,3003]

# Minimum number of nodes required for consensus
count = 2


# IP address 
HOST = '127.0.0.1'






# Structure of a fba message
class FBA_Message:

    def __init__(self, key, value, type=None):
        
        self.key = key
        self.value = value
        self.type = type

# States of a FBA nodes
class FBAStates:
    Initial_Voting = "Initial voting"
    Acceptance = "Acceptance"
    Ratification = "Ratification"
    Confirmation_messages = "Confirmation messages"


class Ballot:
    def __init__(self):
        self.transactions = dict()

    def append(self, key, value):
        if key not in self.transactions:
            self.transactions[key] = list()
        
        self.transactions[key].append(value)

    def most_often(self, key):
        if key in self.transactions:
            return self.most_common(self.transactions[key])
        else:
            raise Exception("Key not in transactions")
    
    def get(self, key):
        return self.transactions[key]

    # most common from a list. Only works when only one value is most common. 
    def most_common(self,L):
        return max(set(L), key=L.count)


class FBAServer(DatagramProtocol):
    def __init__(self, port):
        self.port = int(port)

        # Create a database file
        self.db = Database(name="assignment3_{}.db".format(self.port))
        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to an address
        self.server_address = ('localhost', self.port)

        self.message_history = list()
        self.msgs = dict()
        self.ballot = Ballot()

    def startProtocol(self):
        print("Server {} started".format(self.port))
    
    def sending_message(self, port, json_msg):
       
        data = json.dumps(json_msg).encode()
        self.transport.write(data, (HOST, port))

    def start_messageThread(self, port, json_msg):
        t = threading.Thread(target=self.sending_message, args=(port, json_msg,))
        t.start()

    def listen(self):
        reactor.listenUDP(self.port, self)

    # Broadcase to other nodes in the quorum
    def broadcast(self, json_msg):
        for port in quorum:
            if(port!=self.port):
                self.sending_message(int(port), json_msg)

    # Receive the messages
    def datagramReceived(self, data, host):

        print("received %r from %s" % (data, host))
        message = json.loads(data)


        # If message is already in the history and message type is other than init and initial voting. return
        if message  in self.message_history and message['type'] == FBAStates.Confirmation_messages or message['type'] == FBAStates.Acceptance :
            return

        # Add to the history
        self.message_history.append(message)
        
        # If message is received from client and 3000 is the primary node. Broadcase
        if message['type'] == 'init' and self.port==3000:
            
            self.broadcast(message)

        # if new message received. Add to the dictionary and initiate voting to other nodes
        if message['key'] not in self.msgs:
            self.msgs[message['key']] = message['value']
            # Broadcast initial voting message to other nodes in the quorum
            t = FBA_Message(message['key'], message['value'], FBAStates.Initial_Voting)
            self.broadcast(t.__dict__)

        # if new message with same key but different value is received. Add to the dictionary and initiate voting to other nodes
        elif message['value'] != self.msgs[message['key']] and message['type'] == 'init':
            self.msgs[message['key']] = message['value']
            # Broadcast initial voting message to other nodes in the quorum
            st = FBA_Message(message['key'], message['value'], FBAStates.Initial_Voting)
            self.broadcast(st.__dict__)

        # If received message is in Initial voting state
        elif message['type'] == FBAStates.Initial_Voting:
            # Add to a dict of list
            '''
            {'foo':[$10,$10,$10]}
            '''
            self.ballot.append(message['key'], message['value'])

            # when a node receives the msg from rest of the live nodes in the quorum
            if len(self.ballot.get(message['key'])) >= count:
                
                val = self.db.get(message['key'])
                
                most_often = self.ballot.most_often(message['key'])
                #s = FBA_Message(message['key'], message['value'], FBAStates.Acceptance)
                #self.broadcast(s.__dict__)
                
                # To update the amount for the same key
                if val!=False:
                    amt = int(val[1:])+ int(most_often[1:])
                    updated_amount = '$'+str(amt)
                    
                # Commit the msgs to the database
                    self.db.set(message['key'], updated_amount)
                else:
                    self.db.set(message['key'], most_often)
                
                #s = FBA_Message(message['key'], message['value'], FBAStates.Confirmation_messages)
                #self.broadcast(s.__dict__)
                
                print("Server: {} database snapshot: {}".format(self.port, str(self.db.snapshot())))
                
                # Server 3000 replies to the client after the databasde is updated
                if(self.port==3000):
                    self.sending_message(3005, "Transaction accepted")
                self.db.dump()
                # To create a new dict for every transaction
                self.ballot = Ballot()

            
if __name__ == '__main__':

    
    s = FBAServer(sys.argv[1])
    s.listen()

    reactor.run()
