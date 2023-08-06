import time
import uuid

from layernode import blockchain
from layernode import ntwrk
from layernode import tools
from layernode.service import Service, threaded, sync


class PeerCheckService(Service):
    def __init__(self, engine, new_peers):
        # This logic might change. Here we add new peers while initializing the service
        Service.__init__(self, 'peers_check')
        self.engine = engine
        self.new_peers = []
        self.new_peers = new_peers
        self.db = None
        self.blockchain = None
        self.clientdb = None
        self.node_id = None
        # self.old_peers = []

    def on_register(self):
        self.db = self.engine.db
        self.blockchain = self.engine.blockchain
        self.clientdb = self.engine.clientdb
        for peer in self.new_peers:
            self.clientdb.add_peer(peer, 'friend_of_mine')
        self.node_id = self.db.get('node_id')
        return True

    @threaded
    def listen(self):
        """
        Pseudorandomly select a peer to check.
        If blockchain is synchronizing, don't check anyone.
        :return:
        """
        if self.blockchain.get_chain_state() == blockchain.BlockchainService.SYNCING:
            time.sleep(0.1)
            return

        peers = self.clientdb.get_peers()
        # print('peer check listen peers', peers)
        if len(peers) > 0:
            i = tools.exponential_random(3.0 / 4) % len(peers)
            peer = peers[i]
            t1 = time.time()
            peer_result = self.peer_check(peer)
            t2 = time.time()

            peer['rank'] *= 0.8
            if peer_result == 1:  # We give them blocks. They do not contribute much information
                peer['rank'] += 0.4 * (t2 - t1)
            elif peer_result == 2:  # We are at the same level. Treat them equal
                peer['rank'] += 0.2 * (t2 - t1)
            elif peer_result == 3:
                # They give us blocks. Increase their rank.
                # If blocks are faulty, they will get punished severely.
                peer['rank'] += 0.1 * (t2 - t1)
            else:
                peer['rank'] += 0.2 * 30

            self.clientdb.update_peer(peer)

        time.sleep(0.1)

    @sync
    def peer_check(self, peer):
        peer_ip_port = (peer['ip'], peer['port'])
        greeted = ntwrk.command(peer_ip_port,
                                {
                                    'action': 'greetings',
                                    'node_id': self.node_id,
                                    'port': self.engine.config['port']['peers'],
                                    'length': self.db.get('length'),
                                    'identity_length': self.db.get('identity_length'),
                                    'request_length': self.db.get('request_length')
                                },
                                self.node_id)

        if not isinstance(greeted, dict):
            return None
        if 'error' in greeted.keys():
            return None

        peer['request_length'] = greeted['request_length']
        peer['identity_length'] = greeted['identity_length']
        peer['length'] = greeted['length']
        self.clientdb.update_peer(peer)

        known_length = self.clientdb.get('known_length')
        if greeted['length'] > known_length:
            self.clientdb.put('known_length', greeted['length'])

        known_identity_length = self.clientdb.get('known_identity_length')
        if greeted['identity_length'] > known_identity_length:
            self.clientdb.put('known_identity_length',
                              greeted['identity_length'])

        known_request_length = self.clientdb.get('known_request_length')
        if greeted['request_length'] > known_request_length:
            self.clientdb.put('known_request_length',
                              greeted['request_length'])

        length = self.db.get('length')
        identity_length = self.db.get('identity_length')
        request_length = self.db.get('request_length')
        # This is the most important peer operation part
        # We are deciding what to do with this peer. We can either
        # send them blocks, share txs or download blocks.

        # Only transfer peers at every minute.
        peer_history = self.clientdb.get_peer_history(peer['node_id'])
        if time.time() - peer_history['peer_transfer'] > 60:
            my_peers = self.clientdb.get_peers()
            their_peers = ntwrk.command(
                peer_ip_port, {'action': 'peers'}, self.node_id)
            if type(their_peers) == list:
                for p in their_peers:
                    self.clientdb.add_peer(p, 'friend_of_mine')
                for p in my_peers:
                    ntwrk.command(
                        peer_ip_port, {'action': 'receive_peer', 'peer': p}, self.node_id)

            peer_history['peer_transfer'] = time.time()
            self.clientdb.set_peer_history(peer['node_id'], peer_history)

        # if greeted['identity_length'] < identity_length:
        #     self.give_identity(peer_ip_port, greeted['identity_length'])
        #     return 1
        # elif greeted['identity_length'] == identity_length:
        #     # self.ask_for_txs(peer_ip_port)
        #     if greeted['length'] < length:
        #         self.give_score(peer_ip_port, greeted['length'])
        #         return 1
        #     elif greeted['length'] == length:
        #         return 2
        #     else:
        #         self.download_scores(
        #             peer_ip_port, greeted['length'], length, peer['node_id'])
        #         return 3
        #     # return 2
        # else:
        #     self.download_identities(
        #         peer_ip_port, greeted['identity_length'], identity_length, peer['node_id'])
        #     return 3

        if greeted['identity_length'] < identity_length:
            self.give_identity(peer_ip_port, greeted['identity_length'])
            return 1
        elif greeted['identity_length'] == identity_length:
            # self.ask_for_txs(peer_ip_port)
            if greeted['length'] < length:
                self.give_score(peer_ip_port, greeted['length'])
                return 1
            elif greeted['length'] == length:
                if greeted['request_length'] < request_length:
                    self.give_request(peer_ip_port, greeted['request_length'])
                    return 1
                elif greeted['request_length'] == request_length:
                    return 2
                else:
                    self.download_requests(
                        peer_ip_port, greeted['request_length'], request_length, peer['node_id'])
                    return 3
            else:
                self.download_scores(
                    peer_ip_port, greeted['length'], length, peer['node_id'])
                return 3
            # return 2
        else:
            self.download_identities(
                peer_ip_port, greeted['identity_length'], identity_length, peer['node_id'])
            return 3

    def download_scores(self, peer_ip_port, score_count_peer, length, node_id):
        b = [max(0, length - 10), min(score_count_peer,
                                      length + self.engine.config['peers']['download_limit'])]
        scores = ntwrk.command(
            peer_ip_port, {'action': 'range_request', 'range': b}, self.node_id)
        if isinstance(scores, list):
            self.blockchain.scores_queue.put((scores, node_id))

    def download_identities(self, peer_ip_port, identity_count_peer, identity_length, node_id):
        b = [max(0, identity_length - 10), min(identity_count_peer,
                                               identity_length + self.engine.config['peers']['download_limit'])]
        identities = ntwrk.command(
            peer_ip_port, {'action': 'identity_range_request', 'range': b}, self.node_id)
        if isinstance(identities, list):
            self.blockchain.identities_queue.put((identities, node_id))

    def download_requests(self, peer_ip_port, request_count_peer, request_length, node_id):
        b = [max(0, request_length - 10), min(request_count_peer,
                                               request_length + self.engine.config['peers']['download_limit'])]
        _requests = ntwrk.command(
            peer_ip_port, {'action': 'request_range_request', 'range': b}, self.node_id)
        if isinstance(_requests, list):
            self.blockchain.requests_queue.put((_requests, node_id))

    def give_score(self, peer_ip_port, score_count_peer):
        scores = []
        b = [max(score_count_peer - 5, 0), min(self.db.get('length'),
                                               score_count_peer + self.engine.config['peers']['download_limit'])]
        for i in range(b[0], b[1]):
            scores.append(self.blockchain.get_score(i))
        ntwrk.command(
            peer_ip_port, {'action': 'push_score', 'scores': scores}, self.node_id)
        return 0

    def give_identity(self, peer_ip_port, identity_count_peer):
        identities = []
        b = [max(identity_count_peer - 5, 0), min(self.db.get('identity_length'),
                                                  identity_count_peer + self.engine.config['peers']['download_limit'])]
        for i in range(b[0], b[1]):
            identities.append(self.blockchain.get_identity(i))
        ntwrk.command(
            peer_ip_port, {'action': 'push_identity', 'identities': identities}, self.node_id)
        return 0

    def give_request(self, peer_ip_port, request_count_peer):
        _requests = []
        b = [max(request_count_peer - 5, 0), min(self.db.get('request_length'),
                                                  request_count_peer + self.engine.config['peers']['download_limit'])]
        for i in range(b[0], b[1]):
            _requests.append(self.blockchain.get_request(i))
        ntwrk.command(
            peer_ip_port, {'action': 'push_request', 'requests': _requests}, self.node_id)
        return 0
