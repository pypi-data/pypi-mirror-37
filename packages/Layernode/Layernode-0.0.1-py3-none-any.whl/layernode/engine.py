import signal
import sys
import time

import psutil
import uuid

from layernode import api
from layernode import tools
from layernode.blockchain import BlockchainService
from layernode.client_db import ClientDB
from layernode.database import KeyValueStore
from layernode.models import *
from layernode.my_ipfs import MyIpfs
from layernode.peer_check import PeerCheckService
from layernode.peer_listen import PeerListenService
from layernode.evm_scan import LayernodeScanService, ProviderScanService
from layernode.service import Service, async, threaded
from layernode.state import StateDatabase
from layernode import layer_core
from layernode import tools, custom
from layer.layernode import Layernode as LayernodeSdk
from layer.contracts import Contracts as ContractsSdk
from layer.signer import Signer


def test_layernode_sdk(layernode_sdk):
    try:
        signer = layernode_sdk.signer
        return isinstance(signer, Signer)
    except Exception as e:
        return False


def test_contracts_sdk(contracts_sdk):
    try:
        blockNumber = contracts_sdk.getBlockNumber()
        return blockNumber > 0
    except Exception as e:
        return False


def test_main_database():
    results = [False, False]
    db_session = session()
    test = db_session.query(Test).first()
    if not test:
        test = Test(1)
        db_session.add(test)
        db_session.commit()
    else:
        test.count = 1
        db_session.commit()
    results[0] = True

    test2 = db_session.query(Test).first()
    if test2.count == 1:
        results[1] = True
    else:
        results[1] = False

    return results[0] and results[1]


def test_level_database(db):
    results = [False, False]
    response = db.put('test', 'TEST')
    if response:
        test_response = db.get('test')
        if test_response == 'TEST':
            results[0] = True

    db.simulate()
    response = db.put('test', 'TEST_SIM')
    if response:
        test_response = db.get('test')
        if test_response == 'TEST_SIM':
            db.rollback()
            if db.get('test') == 'TEST':
                results[1] = True

    return results[0] and results[1]


def test_ipfs(myipfs):
    try:
        result = myipfs.api.id()
        return isinstance(result, dict)
    except Exception as e:
        return False


instance = None


class Engine(Service):
    def __init__(self, config, working_dir):
        Service.__init__(self, 'engine')
        self.config = config
        self.working_dir = working_dir

        self.layernode_sdk = LayernodeSdk(
            signer_endpoint=config['signer_endpoint'])
        self.contracts_sdk = ContractsSdk(
            geth_rpc_host=config['geth_rpc_host'])
        self.db = KeyValueStore(self, 'layernode.db')
        self.myipfs = MyIpfs(
            self, config['ipfs']['ip'], config['ipfs']['port'])
        self.blockchain = BlockchainService(self)
        self.peers_check = PeerCheckService(self, self.config['peers']['list'])
        self.peer_receive = PeerListenService(self)
        self.provider_scan = ProviderScanService(self)
        self.layernode_scan = LayernodeScanService(self)
        self.clientdb = ClientDB(self)
        self.statedb = StateDatabase(self)

    def on_register(self):
        print('Starting layernode')

        if not test_layernode_sdk(self.layernode_sdk):
            tools.log("LayerNode SDK service is not working.")
            return False

        if not test_contracts_sdk(self.contracts_sdk):
            tools.log("Contracts SDK service is not working.")
            return False

        if not test_main_database():
            tools.log("Main Database(mysql) service is not working.")
            return False

        if not test_level_database(self.db):
            tools.log("Database service(levelDB) is not working.")
            return False

        if not test_ipfs(self.myipfs):
            tools.log("Ipfs service is not working.")
            # comment this for test
            # return False

        b = self.db.get('init')
        if not b:
            print("Initializing records")
            score_count = layer_core.get_score_length()
            if score_count is None:
                score_count = -1
                return False
            identity_count = layer_core.get_identity_length()
            if identity_count is None:
                identity_count = -1
                return False
            request_count = layer_core.get_request_length()
            if request_count is None:
                request_count = -1
                return False

            self.db.put('init', True)
            self.db.put('length', score_count)
            self.db.put('peer_list', [])
            self.db.put('targets', {})
            self.db.put('times', {})
            self.db.put('identity_length', identity_count)
            self.db.put('request_length', request_count)
            self.db.put('accounts', {})
            self.db.put('job_list', [])
            self.clientdb.put('known_length', score_count)
            self.clientdb.put('known_identity_length', identity_count)
            self.clientdb.put('known_request_length', request_count)

        if not self.blockchain.register():
            sys.stderr.write("Blockchain service has failed. Exiting!\n")
            self.unregister_sub_services()
            return False

        if not self.peer_receive.register():
            sys.stderr.write("Peer Receive service has failed. Exiting!\n")
            self.unregister_sub_services()
            return False

        if not self.peers_check.register():
            sys.stderr.write("Peers Check service has failed. Exiting!\n")
            self.unregister_sub_services()
            return False

        if not self.layernode_scan.register():
            sys.stderr.write("Layernode Scan service has failed. Exiting!\n")
            self.unregister_sub_services()
            return False

        if not self.provider_scan.register():
            sys.stderr.write("Provider Scan service has failed. Exiting!\n")
            self.unregister_sub_services()
            return False

        api.run()

        return True

    def unregister_sub_services(self):
        running_services = set()
        if self.provider_scan.get_state() == Service.RUNNING:
            self.provider_scan.unregister()
            running_services.add(self.provider_scan)
        if self.layernode_scan.get_state() == Service.RUNNING:
            self.layernode_scan.unregister()
            running_services.add(self.layernode_scan)
        if self.peers_check.get_state() == Service.RUNNING:
            self.peers_check.unregister()
            running_services.add(self.peers_check)
        if self.peer_receive.get_state() == Service.RUNNING:
            self.peer_receive.unregister()
            running_services.add(self.peer_receive)
        if self.blockchain.get_state() == Service.RUNNING:
            self.blockchain.unregister()
            running_services.add(self.blockchain)

        for service in running_services:
            service.join()
            print('Closed {}'.format(service.name))

    def get_new_node_id(self):
        my_ip = self.config['my_ip']
        peer_list = self.config['peers']['list']
        for peer in peer_list:
            if peer['ip'] == my_ip:
                return peer['node_id']
        return str(uuid.uuid4())

    def get_my_ip(self):
        my_ip = self.config['my_ip']
        return my_ip

    @threaded
    def stats(self):
        value = psutil.cpu_percent()
        if int(psutil.cpu_percent()) > 0:
            api.cpu_usage(str(value))
        time.sleep(0.1)

    @async
    def stop(self):
        self.unregister_sub_services()
        self.unregister()


def signal_handler(signal, frame):
    sys.stderr.write('Detected interrupt, initiating shutdown\n')
    if instance is not None:
        instance.stop()


def main(config, working_dir):
    # create_tables()
    global instance
    instance = Engine(config, working_dir)
    if instance.register():
        print("Layernode is fully running...")
        signal.signal(signal.SIGINT, signal_handler)
        instance.join()
        print("Shutting down gracefully")
    else:
        print("Couldn't start layernode")
