import copy
import socket
import sys
import uuid

from layernode import ntwrk, custom
from layernode import tools
from layernode.client_db import ClientDB
from layernode.ntwrk import Message
from layernode.service import Service, threaded, sync


class PeerListenService(Service):
    def __init__(self, engine):
        Service.__init__(self, 'peer_receive')
        self.engine = engine
        self.db = None
        self.blockchain = None
        self.clientdb = None
        self.node_id = None

    def on_register(self):
        self.db = self.engine.db
        self.blockchain = self.engine.blockchain
        self.clientdb = self.engine.clientdb

        if not self.db.exists('node_id'):
            node_id = self.engine.get_new_node_id()
            self.db.put('node_id', node_id)
            self.clientdb.put('node_id', node_id)

        self.node_id = self.db.get('node_id')

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.settimeout(2)
            self.s.bind(('0.0.0.0', self.engine.config['port']['peers']))
            self.s.listen(10)
            print("Started Peer Listen on 0.0.0.0:{}".format(
                self.engine.config['port']['peers']))
            return True
        except Exception as e:
            tools.log("Could not start Peer Receive socket!")
            tools.log(e)
            sys.stderr.write(str(e)+'\n')
            return False

    def on_close(self):
        try:
            self.s.close()
        except:
            pass

    @threaded
    def listen(self):
        try:
            client_sock, address = self.s.accept()
            response, leftover = ntwrk.receive(client_sock)
            if response.getFlag():
                message = Message.from_yaml(response.getData())
                request = message.get_body()
                try:
                    if hasattr(self, request['action']) \
                            and request['version'] == custom.version \
                            and message.get_header("node_id") != self.node_id:
                        kwargs = copy.deepcopy(request)
                        if request['action'] == 'greetings':
                            kwargs['__remote_ip__'] = client_sock.getpeername()
                        elif request['action'] == 'push_score':
                            kwargs['node_id'] = message.get_header("node_id")
                        elif request['action'] == 'push_identity':
                            kwargs['node_id'] = message.get_header("node_id")
                        del kwargs['action']
                        del kwargs['version']
                        result = getattr(self, request['action'])(**kwargs)
                    else:
                        result = 'Received action is not valid'
                except:
                    result = 'Something went wrong while evaluating.\n'
                    tools.log(sys.exc_info())
                response = Message(headers={'ack': message.get_header('id'),
                                            'node_id': self.node_id},
                                   body=result)
                ntwrk.send(response, client_sock)
                client_sock.close()
        except Exception as e:
            import time
            time.sleep(0.1)

    @sync
    def greetings(self, node_id, port, length, identity_length, request_length, __remote_ip__):
        """
        Called when a peer starts communicating with us.
        'Greetings' type peer addition.

        :param node_id: Node id of remote host
        :param port: At which port they are listening to peers.
        :param __remote_ip__: IP address of remote as seen from this network.
        :return: Our own greetings message
        """
        peer = copy.deepcopy(ClientDB.default_peer)
        peer.update(
            node_id=node_id,
            ip=__remote_ip__[0],
            port=port,
            length=length,
            identity_length=identity_length,
            request_length=request_length,
            rank=0.75
        )
        if length > self.clientdb.get('known_length'):
            self.clientdb.put('known_length', length)
        if identity_length > self.clientdb.get('known_identity_length'):
            self.clientdb.put('known_identity_length', identity_length)
        if request_length > self.clientdb.get('known_request_length'):
            self.clientdb.put('known_request_length', request_length)
        self.clientdb.add_peer(peer, 'greetings')
        return {
            'node_id': self.node_id,
            'port': self.engine.config['port']['peers'],
            'length': self.db.get('length'),
            'identity_length': self.db.get('identity_length'),
            'request_length': self.db.get('request_length')
        }

    @sync
    def receive_peer(self, peer):
        """
        'Friend of mine' type peer addition.
        :param peer: a peer dict, sent by another peer we are communicating with.
        :return: None
        """
        peer.update(rank=1)  # We do not care about earlier rank.
        self.clientdb.add_peer(peer, 'friend_of_mine')

    @sync
    def score_count(self):
        length = self.db.get('length')
        # d = '0'
        # if length >= 0:
        #     d = self.db.get('identity_length')
        return {'length': length}

    @sync
    def identity_count(self):
        identity_length = self.db.get('identity_length')
        # d = '0'
        # if length >= 0:
        #     d = self.db.get('identity_length')
        return {'identity_length': identity_length}

    @sync
    def request_count(self):
        request_count = self.db.get('request_count')
        # d = '0'
        # if length >= 0:
        #     d = self.db.get('identity_length')
        return {'request_count': request_count}

    @sync
    def range_request(self, range):
        out = []
        counter = 0
        while range[0] + counter <= range[1]:
            score = self.blockchain.get_score(range[0] + counter)
            if score and 'length' in score:
                out.append(score)
            counter += 1
        return out

    @sync
    def identity_range_request(self, range):
        out = []
        counter = 0
        while range[0] + counter <= range[1]:
            identity = self.blockchain.get_identity(range[0] + counter)
            if identity and 'identity_length' in identity:
                out.append(identity)
            counter += 1
        return out

    @sync
    def request_range_request(self, range):
        out = []
        counter = 0
        while range[0] + counter <= range[1]:
            _request = self.blockchain.get_request(range[0] + counter)
            if _request and 'request_length' in _request:
                out.append(_request)
            counter += 1
        return out

    @sync
    def peers(self):
        return self.clientdb.get_peers()

    @sync
    def push_score(self, scores, node_id):
        self.blockchain.scores_queue.put((scores, node_id))
        return 'success'

    @sync
    def push_identity(self, identities, node_id):
        self.blockchain.identities_queue.put((identities, node_id))
        return 'success'

    @sync
    def push_request(self, _requests, node_id):
        self.blockchain.requests_queue.put((_requests, node_id))
        return 'success'
