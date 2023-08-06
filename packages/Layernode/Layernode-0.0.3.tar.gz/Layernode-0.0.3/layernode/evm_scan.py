import time

from layernode import blockchain
from layernode import ntwrk
from layernode import tools
from layernode.service import Service, threaded, sync
from layernode.models import session
from layernode.models import Provider, Layernode
import socket


class ProviderScanService(Service):
    def __init__(self, engine):
        # This logic might change. Here we add new peers while initializing the service
        Service.__init__(self, 'provider_scan')
        self.engine = engine

    def on_register(self):
        print("Started Provider Scan")
        return True

    @threaded
    def listen(self):
        """
        scan loop
        """
        # print('scanning provider')
        try:
            p_address_list = self.engine.contracts_sdk.getProviders()
            # print('p_address_list', p_address_list)

            if len(p_address_list) > 0:
                for p_address in p_address_list:
                    p_info = self.engine.contracts_sdk.getProviderByAddress(p_address)
                    p_info['address'] = p_info['address'].lower()

                    p_info['balance'] = self.engine.contracts_sdk.getEscrowBalance(p_address)
                    # p_info['balance'] = 10000
                    # print('p_info', p_info)

                    # store to database
                    db_session = session()
                    row = db_session.query(Provider).filter(Provider.address==p_info["address"]).first()

                    if row is None:
                        row = Provider(p_info["address"], p_info["name"],
                                    p_info["category"], p_info["approved"], p_info["balance"])
                        db_session.add(row)
                        db_session.commit()
                    else:
                        if row.name != p_info["name"] or row.category != p_info["category"] or row.approved != p_info["approved"] or row.balance != p_info["balance"]:
                            row.name = p_info["name"]
                            row.category = p_info["category"]
                            row.approved = p_info["approved"]
                            row.balance = p_info["balance"]
                            db_session.commit()
        except Exception as e:
            pass
            # print(str(e))
            # tools.log(str(e))

        time.sleep(30)


class LayernodeScanService(Service):
    def __init__(self, engine):
        # This logic might change. Here we add new peers while initializing the service
        Service.__init__(self, 'layernode_scan')
        self.engine = engine

    def on_register(self):
        print("Started Layernode Scan")
        return True

    @threaded
    def listen(self):
        """
        scan loop
        """
        # print('scanning layernode')
        try:
            l_address_list = self.engine.contracts_sdk.getLayerNodes()
            # print('l_address_list', l_address_list)

            if len(l_address_list) > 0:
                for l_address in l_address_list:
                    # print('l_address', l_address)
                    l_info = self.engine.contracts_sdk.getLayerNodeByAddress(l_address)
                    # print('l_info', l_info)
                    # {address, url, approved}
                    # layernodes = [
                    #     {"address": "0x12345", "url": "url1", "approved": False},
                    # ]

                    # store to database
                    # try:
                    #     _ip = socket.gethostbyname(item["url"])
                    # except Exception as e:
                    #     continue
                    db_session = session()
                    row = db_session.query(Layernode).filter(Layernode.address==l_info["address"]).first()
                    if row is None:
                        row = Layernode(l_info["address"], l_info["url"], l_info["approved"])
                        db_session.add(row)
                        db_session.commit()
                    else:
                        if row.url != l_info["url"] or row.approved != l_info["approved"]:
                            row.url = l_info["url"]
                            row.approved = l_info["approved"]
                            db_session.commit()
        except Exception as e:
            pass
            # print(str(e))
            # tools.log(str(e))

        time.sleep(30)
