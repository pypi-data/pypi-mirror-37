import sys
import ipfsapi
from layernode import tools, custom


class MyIpfs:
    def __init__(self, engine, ip, port):
        self.engine = engine
        self.ip = ip
        self.port = port
        self.api = None
        self.log = dict()
        try:
            self.api = ipfsapi.connect(self.ip, self.port)
        except Exception as e:
            tools.log(e)
            sys.stderr.write('ipfs connection cannot be established!\n')

    def add(self, filename):
        return self.api.add(filename)
        # {'Hash': 'QmWxS5aNTFEc9XbMX1ASvLET1zrqEaTssqt33rVZQCQb22', 'Name': 'test.txt'}

    def add_json(self, data):
        # data = [1, 77, 'lol']
        return self.api.add_json(data)
        # 'QmQ4R5cCUYBWiJpNL7mFe4LDrwD6qBr5Re17BoRAY9VNpd'       

    def get_json(self, hash):
        return self.api.get_json(hash)
        # [1, 77, 'lol']               