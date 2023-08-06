import copy
import threading
import time
from cdecimal import Decimal

from layernode import custom, api
from layernode import tools
from layernode.ntwrk import Response
from layernode.service import Service, threaded, sync, NoExceptionQueue, lockit
from layernode.models import Layernode, Provider, Score, Identity, User
from layernode.models import *
from layernode import layer_core


class BlockchainService(Service):
    """
    tx_types are allowed transactions in coinami platform.
    spend: Send coins from one address to another
    mint: Traditional mining coinbase
    reward: Reward coins sent from an authority to an address
    auth_reg: Authority register. Includes a certificate that proves this authority is approved by root.
    job_dump: Announcing jobs that are prepared and ready to be downloaded
    job_request: Entering a pool for a job request.
    """
    IDLE = 1
    SYNCING = 2

    def __init__(self, engine):
        Service.__init__(self, name='blockchain')
        self.engine = engine
        self.scores_queue = NoExceptionQueue(3)
        self.identities_queue = NoExceptionQueue(3)
        self.requests_queue = NoExceptionQueue(3)
        # self.tx_queue = NoExceptionQueue(100)
        self.db = None
        self.statedb = None
        self.clientdb = None
        self.__state = BlockchainService.IDLE
        self.addLock = threading.RLock()

    def on_register(self):
        self.db = self.engine.db
        self.statedb = self.engine.statedb
        self.clientdb = self.engine.clientdb
        print("Started Blockchain")
        return True

    @threaded
    @lockit('write_kvstore')
    def blockchain_process(self):
        """
        In this thread we check blocks queue for possible additions to blockchain.
        Following type is expected to come out of the queue. Any other type will be rejected.
        ([candidate_blocks in order], peer_node_id)
        Only 3 services actually put stuff in queue: peer_listen, peer_check
        PeerListen and PeerCheck obeys the expected style.
        :return:
        """
        try:
            candidate = self.scores_queue.get(timeout=0.1)
            self.set_chain_state(BlockchainService.SYNCING)
            try:
                if isinstance(candidate, tuple):
                    scores = candidate[0]
                    node_id = candidate[1]
                    total_number_of_scores_added = 0

                    for score in scores:
                        intchk = self.score_integrity_check(score)
                        if intchk > 0:
                            self.peer_reported_false_scores(node_id)
                            return

                    try:
                        for score in scores:
                            add_score_result = self.add_score(score)
                            # A score that is ahead of us could not be added. No need to proceed.
                            if add_score_result == 0:
                                total_number_of_scores_added += 1
                                api.new_score()
                    except Exception as e:
                        tools.log(e)

                    if total_number_of_scores_added == 0:
                        self.peer_reported_false_scores(node_id)
            except Exception as e:
                pass
                # print('blockchain_process error', e)
                # tools.log(e)
            self.scores_queue.task_done()
        except Exception as e:
            pass
            # tools.log(e)

        # identity queue
        try:
            candidate = self.identities_queue.get(timeout=0.1)
            self.set_chain_state(BlockchainService.SYNCING)
            try:
                if isinstance(candidate, tuple):
                    identities = candidate[0]
                    node_id = candidate[1]
                    total_number_of_identities_added = 0

                    for identity in identities:
                        if self.identity_integrity_check(identity) > 0:
                            self.peer_reported_false_identities(node_id)
                            return

                    try:
                        for identity in identities:
                            add_identity_result = self.add_identity(identity)
                            # A identity that is ahead of us could not be added. No need to proceed.
                            if add_identity_result == 0:
                                total_number_of_identities_added += 1
                                api.new_identity()
                    except Exception as e:
                        tools.log(e)

                    if total_number_of_identities_added == 0:
                        self.peer_reported_false_identities(node_id)
            except Exception as e:
                pass
                # tools.log(e)
            self.identities_queue.task_done()
        except Exception as e:
            pass
            # tools.log(e)

        # requests queue
        try:
            candidate = self.requests_queue.get(timeout=0.1)
            self.set_chain_state(BlockchainService.SYNCING)
            try:
                if isinstance(candidate, tuple):
                    _requests = candidate[0]
                    node_id = candidate[1]
                    total_number_of_requests_added = 0

                    for _request in _requests:
                        intchk = self.request_integrity_check(_request)
                        if intchk > 0:
                            self.peer_reported_false_requests(node_id)
                            return

                    try:
                        for _request in _requests:
                            add_request_result = self.add_request(_request)
                            # A request that is ahead of us could not be added. No need to proceed.
                            if add_request_result == 0:
                                total_number_of_requests_added += 1
                                api.new_request()
                    except Exception as e:
                        tools.log(e)

                    if total_number_of_requests_added == 0:
                        self.peer_reported_false_requests(node_id)
            except Exception as e:
                pass
                # tools.log(e)
            self.requests_queue.task_done()
        except Exception as e:
            pass
            # tools.log(e)

        self.set_chain_state(BlockchainService.IDLE)

    @sync
    def set_chain_state(self, new_state):
        self.__state = new_state

    @sync
    def get_chain_state(self):
        return self.__state

    @lockit('kvstore')
    def get_score(self, length):
        return layer_core.get_score(length)

    @lockit('kvstore')
    def get_identity(self, identity_length):
        return layer_core.get_identity(identity_length)

    @lockit('kvstore')
    def get_request(self, request_length):
        return layer_core.get_request(request_length)

    def score_integrity_check(self, score):
        try:
            # validation
            if not isinstance(score, dict) or not score['hash'] or not score['address'] or not score['keyHash'] or not score['score'] or not score['category'] or not score['provider_sig'] or not score['signer_sig']:
                # {'status': 400, 'msg': 'containing empty field'}
                return 5

            db_session = session()
            # address/provider check
            provider_row = db_session.query(Provider).filter(
                Provider.address == score['address']).first()
            if provider_row is None:
                # {'status': 400, 'msg': 'invalid provider address'}
                return 1

            # # identity_hash check
            # identity_row = Identity.query.filter_by(
            #     hash=score['hash']).first()
            # if identity_row is None:
            #     # {'status': 400, 'msg': 'invalid identity hash'}
            #     return 6

            # verify score signature
            sigs_verify_code = self.engine.layernode_sdk.verify_score_signature(
                hash=score['hash'], address=score['address'], keyHash=score['keyHash'], score=score['score'], category=score['category'], provider_sig=score['provider_sig'], signer_sig=score['signer_sig'])
            if sigs_verify_code > 0:
                # {'status': 400, 'msg': 'signature_verify failed'}
                # return 2
                """
                sigs_verify_code = 0 => success
                sigs_verify_code = 1 => provider_sig is not verified
                sigs_verify_code = 2 => signer_sig is not verified
                sigs_verify_code = 3 => key_hash is not valid
                """
                return 200+sigs_verify_code

            return 0
        except Exception as e:
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4

    def identity_integrity_check(self, identity):
        try:
            # validation
            if not isinstance(identity, dict) or not identity['hash'] or not identity['address'] or not identity['keyHash'] or not identity['provider_sig'] or not identity['signer_sig']:
                # {'status': 400, 'msg': 'containing empty field'}
                return 5

            db_session = session()
            # address/provider check
            provider_row = db_session.query(Provider).filter(
                Provider.address == identity['address']).first()
            if provider_row is None:
                # {'status': 400, 'msg': 'invalid provider address'}
                return 1

            # verify identity signature
            sigs_verify_code = self.engine.layernode_sdk.verify_identity_signature(
                hash=identity['hash'], address=identity['address'], keyHash=identity['keyHash'], provider_sig=identity['provider_sig'], signer_sig=identity['signer_sig'])
            if sigs_verify_code > 0:
                # {'status': 400, 'msg': 'signature_verify failed'}
                # return 2
                """
                sigs_verify_code = 0 => success
                sigs_verify_code = 1 => provider_sig is not verified
                sigs_verify_code = 2 => signer_sig is not verified
                sigs_verify_code = 3 => key_hash is not valid
                """
                return 200+sigs_verify_code

            return 0
        except Exception as e:
            print(str(e))
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4

    def request_integrity_check(self, _request):
        try:
            # validation
            if not isinstance(_request, dict) or not _request['hash'] or not _request['address'] or not _request['timestamp'] or not _request['provider_sig']:
                # {'status': 400, 'msg': 'containing empty field'}
                return 5

            hash = _request['hash']
            address = _request['address']
            timestamp = _request['timestamp']
            provider_sig = _request['provider_sig']

            db_session = session()

            # address/provider check
            provider_row = db_session.query(Provider).filter(
                Provider.address == address).first()
            if provider_row is None:
                # {'status': 400, 'msg': 'invalid provider address'}
                return 1

            # balance and requests count check
            req_count = layer_core.get_request_count_by_provider(address)
            if req_count >= provider_row.balance:
                # {'status': 400, 'msg': 'provider balance is not enough'}
                return 6

            # verify sign
            provider_request = {'hash': hash,
                                'address': address, 'timestamp': timestamp}
            sigs_verify_code = self.engine.layernode_sdk.verify_provider_signature(
                provider_request, provider_sig, address)
            if sigs_verify_code > 0:
                """
                sigs_verify_code = 0 => success
                sigs_verify_code = 1 => provider_sig is not verified
                """
                return 200+sigs_verify_code

            return 0
        except Exception as e:
            # print(e)
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4

    def peer_reported_false_scores(self, node_id):
        peer = self.clientdb.get_peer(node_id)
        if peer is not None:
            peer['rank'] *= 0.8
            peer['rank'] += 0.2 * 30
            self.clientdb.update_peer(peer)

    def peer_reported_false_identities(self, node_id):
        peer = self.clientdb.get_peer(node_id)
        if peer is not None:
            peer['rank'] *= 0.8
            peer['rank'] += 0.2 * 30
            self.clientdb.update_peer(peer)

    def peer_reported_false_requests(self, node_id):
        peer = self.clientdb.get_peer(node_id)
        if peer is not None:
            peer['rank'] *= 0.8
            peer['rank'] += 0.2 * 30
            self.clientdb.update_peer(peer)

    def add_score(self, score):
        """Attempts adding a new score to the blockchain."""

        # tools.echo('add score: ' + str(score['id']))
        add_val = self.update_database_with_score(score)
        if add_val > 0:
            return add_val

        # length = self.db.get('length')
        # if not length:
        #     length = layer_core.get_score_length()
        # self.db.put('length', length+1)
        self.db.put('length', layer_core.get_score_length())
        # tools.techo('add score: ' + str(score['id']))
        return 0

    def add_identity(self, identity):
        """Attempts adding a new identity to the blockchain."""

        # tools.echo('add identity: ' + str(identity['hash']))
        add_val = self.update_database_with_identity(identity)
        if add_val > 0:
            return add_val

        # identity_length = self.db.get('identity_length')
        # if not identity_length:
        #     identity_length = layer_core.get_identity_length()
        # self.db.put('identity_length', identity_length+1)
        self.db.put('identity_length', layer_core.get_identity_length())
        # tools.techo('add identity: ' + str(identity['hash']))
        return 0

    def add_request(self, _request):
        """Attempts adding a new request to the blockchain."""

        add_val = self.update_database_with_request(_request)
        if add_val > 0:
            return add_val

        # request_length = self.db.get('request_length')
        # if not request_length:
        #     request_length = layer_core.get_request_length()
        # self.db.put('request_length', request_length+1)
        self.db.put('request_length', layer_core.get_request_length())
        return 0

    def update_database_with_score(self, new_score):
        try:
            # validation
            ret_intchk = self.score_integrity_check(new_score)
            if ret_intchk > 0:
                return ret_intchk

            db_session = session()

            # add score
            row = None
            if new_score['id']:
                row = db_session.query(Score).filter(
                    Score.id == new_score['id']).first()

            if row is None:
                row = Score(id=new_score['id'], address=new_score['address'], hash=new_score['hash'], keyHash=new_score['keyHash'],
                            score=new_score['score'], category=new_score['category'], provider_sig=new_score['provider_sig'], signer_sig=new_score['signer_sig'])
                db_session.add(row)
                db_session.commit()
                # {'status': 200, 'msg': 'Score added succesfully'}
                return 0
            else:
                # {'status': 400, 'msg': 'Identity existing'}
                return 3
        except Exception as e:
            # print(e)
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4

    def update_database_with_identity(self, new_identity):
        try:
            db_session = session()
            res_intchk = self.identity_integrity_check(new_identity)
            if res_intchk > 0:
                return res_intchk

            # add identity
            row = db_session.query(Identity).filter(
                Identity.hash == new_identity['hash']).first()

            if row is None:
                row = Identity(hash=new_identity['hash'], address=new_identity['address'], keyHash=new_identity['keyHash'],
                               provider_sig=new_identity['provider_sig'], signer_sig=new_identity['signer_sig'], user=None)
                db_session.add(row)
                db_session.commit()
                # {'status': 200, 'msg': 'Identity added succesfully'}
                return 0
            else:
                # {'status': 400, 'msg': 'Identity existing'}
                return 3
        except Exception as e:
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4

    def update_database_with_request(self, new_request):
        try:
            # validation
            ret_intchk = self.request_integrity_check(new_request)
            if ret_intchk > 0:
                return ret_intchk

            db_session = session()

            # add request
            row = None
            if new_request['id']:
                row = db_session.query(Requests).filter(
                    Requests.id == new_request['id']).first()

            if row is None:
                row = Requests(id=new_request['id'], address=new_request['address'], hash=new_request['hash'],
                               timestamp=new_request['timestamp'], provider_sig=new_request['provider_sig'])
                db_session.add(row)
                db_session.commit()
                # {'status': 200, 'msg': 'Requests added succesfully'}
                return 0
            else:
                # {'status': 400, 'msg': 'Requests existing'}
                return 3
        except Exception as e:
            # print(e)
            # {'status': 400, 'msg': 'error occurred', 'data': str(e)}
            return 4
