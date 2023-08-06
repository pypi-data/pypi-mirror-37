import copy
import json
import os
import tempfile
import threading
from pprint import pprint
import psutil as psutil
# WARNING! Do not remove below import line. PyInstaller depends on it
from engineio import async_threading
from flask import Flask, request, Response, send_file, jsonify
from flask_socketio import SocketIO

from layernode import tools, engine, custom
from layernode import layer_core
from layernode.blockchain import BlockchainService
from layernode.service import Service


async_threading  # PyCharm automatically removes unused imports. This prevents it


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.hex()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def blockchain_synced(func):
    def wrapper(*args, **kwargs):
        if engine.instance.blockchain.get_chain_state() == BlockchainService.IDLE:
            return func(*args, **kwargs)
        else:
            return 'Blockchain is syncing. This method is not reliable while operation continues.\n' + \
                   str(engine.instance.db.get('length')) + '-' + \
                   str(engine.instance.db.get('known_length')) + '---' + \
                   str(engine.instance.db.get('identity_length')) + '-' + \
                   str(engine.instance.db.get('knwon_identity_length')) + '---' + \
                   str(engine.instance.db.get('request_length')) + '-' + \
                str(engine.instance.clientdb.get('known_request_length'))

    # To keep the function name same for RPC helper
    wrapper.__name__ = func.__name__

    return wrapper


app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
listen_thread = None


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def run():
    def thread_target():
        socketio.run(app, host=host,
                     port=engine.instance.config['port']['api'])

    global listen_thread
    # host = os.environ.get('LAYERNODE_API_HOST', "localhost")
    host = engine.instance.config['LAYERNODE_API_HOST']
    listen_thread = threading.Thread(target=thread_target, daemon=True)
    listen_thread.start()
    print("Started API on {}:{}".format(
        host, engine.instance.config['port']['api']))
    """
    Deprecated in favor of electron app
    import webbrowser
    webbrowser.open('http://' + host + ':' + str(engine.instance.config['port']['api']))
    """


@socketio.on('connect')
def connect():
    print("%s connected" % request.sid)
    return ""


@app.route('/', methods=['GET', 'POST'])
def hello():
    return "~Healthy and alive~"


@app.route('/add_identity', methods=['POST'])
@blockchain_synced
def add_identity():
    params = request.get_json()
    # {
    #     'signer_request': {
    #         'provider_request': {
    #             'address': '0x011a28420578a06728dd537754d0f3d9b73e5f57',
    #             'keyHash': '1413f5327216dca7ed7b7f8632d2a203a0892aba',
    #             'hash': 'Hello World'
    #         },
    #         'provider_sig': '0xa2f74a9f636da1ccc37e193a27564939aeb9692694b69b4ddd6a21e964de6686417934225e06ecab3c4693b6364d2078e03f1989e52c595b079b66fcf7b10bdd1b'
    #     },
    #     'signer_sig': '3065023100fbe668f78bc6ef9ecf078d9aacf40617883a1d6dc079222d01cc1aa92f1c9e7542858fa2ad75253cbe1bc1476de181f5023079d92b41b2f0c3ec4a4fef96bb33b06b4b75040e45851716ec531d625c17d536dcee1f79aab28e109f385b867dfc520d'
    # }

    # validate params
    try:
        signer_request = params['signer_request']
        signer_sig = params['signer_sig']

        provider_request = signer_request['provider_request']
        provider_sig = signer_request['provider_sig']

        address = provider_request['address']
        # address = address.lower()
        keyHash = provider_request['keyHash']
        hash = provider_request['hash']

        # verification will be done in layer_core : add action
        # signer_sig verify - (signer_request, signer_sig)
        # provider_sig verify - (provider_request, provider_sig)
    except Exception:
        return generate_json_response({'status': 400, 'msg': 'missing request params'})

    try:
        add_result = engine.instance.blockchain.add_identity({'hash': hash, 'address': address, 'keyHash': keyHash,
                                                              'provider_sig': provider_sig, 'signer_sig': signer_sig, 'user': None})
        if add_result == 0:
            return generate_json_response({'status': 200, 'msg': 'Identity added succesfully'})
        elif add_result == 1:
            return generate_json_response({'status': 400, 'msg': 'invalid provider address'})
        elif add_result > 200 and add_result < 300:
            return generate_json_response({'status': 400, 'msg': 'signature_verify failed', 'err_code': add_result})
        elif add_result == 3:
            return generate_json_response({'status': 400, 'msg': 'Identity existing'})
        elif add_result == 4:
            return generate_json_response({'status': 400, 'msg': 'error occurred'})
        elif add_result == 5:
            return generate_json_response({'status': 400, 'msg': 'containing empty field'})
        else:
            return generate_json_response({'status': 400, 'msg': 'unknown error'})
    except Exception as e:
        return generate_json_response({'status': 400, 'msg': str(e)})


@app.route('/add_score', methods=['POST'])
@blockchain_synced
def add_score():
    params = request.get_json()
    # {
    #     'signer_request': {
    #         'provider_request': {
    #             'address': '0x011a28420578a06728dd537754d0f3d9b73e5f57',
    #             'keyHash': '1413f5327216dca7ed7b7f8632d2a203a0892aba',
    #             'hash': 'Hello World'
    #             "score":2,
    #             "category":"ProviderTransactionCategory"
    #         },
    #         'provider_sig': '0xa2f74a9f636da1ccc37e193a27564939aeb9692694b69b4ddd6a21e964de6686417934225e06ecab3c4693b6364d2078e03f1989e52c595b079b66fcf7b10bdd1b'
    #     },
    #     'signer_sig': '3065023100fbe668f78bc6ef9ecf078d9aacf40617883a1d6dc079222d01cc1aa92f1c9e7542858fa2ad75253cbe1bc1476de181f5023079d92b41b2f0c3ec4a4fef96bb33b06b4b75040e45851716ec531d625c17d536dcee1f79aab28e109f385b867dfc520d'
    # }

    # validate params
    try:
        signer_request = params['signer_request']
        signer_sig = params['signer_sig']

        provider_request = signer_request['provider_request']
        provider_sig = signer_request['provider_sig']

        address = provider_request['address']
        # address = address.lower()
        keyHash = provider_request['keyHash']
        hash = provider_request['hash']
        score = provider_request['score']
        category = provider_request['category']

        # verification will be done in layer_core : add action
        # signer_sig verify - (signer_request, signer_sig)
        # provider_sig verify - (provider_request, provider_sig)
    except Exception:
        return generate_json_response({'status': 400, 'msg': 'missing request params'})

    try:
        add_result = engine.instance.blockchain.add_score({'id': None, 'hash': hash, 'address': address, 'keyHash': keyHash,
                                                           'score': score, 'category': category, 'provider_sig': provider_sig, 'signer_sig': signer_sig})
        if add_result == 0:
            return generate_json_response({'status': 200, 'msg': 'Score added succesfully'})
        elif add_result == 1:
            return generate_json_response({'status': 400, 'msg': 'invalid provider address'})
        elif add_result > 200 and add_result < 300:
            return generate_json_response({'status': 400, 'msg': 'signature_verify failed', 'err_code': add_result})
        elif add_result == 3:
            return generate_json_response({'status': 400, 'msg': 'Score existing'})
        elif add_result == 4:
            return generate_json_response({'status': 400, 'msg': 'error occurred'})
        elif add_result == 5:
            return generate_json_response({'status': 400, 'msg': 'containing empty field'})
        elif add_result == 6:
            return generate_json_response({'status': 400, 'msg': 'invalid identity hash'})
        else:
            return generate_json_response({'status': 400, 'msg': 'unknown error'})
    except Exception as e:
        return generate_json_response({'status': 400, 'msg': str(e)})


@app.route('/get_score', methods=['POST'])
@blockchain_synced
def get_score():
    params = request.get_json()
    # {
    #     "provider_request": {
    #         "hash": "9ds03290dsalk3jkidka23lsfjomvio3zxpoiu0dsajfi",
    #         "address": "0xProviderAddressFromSdk",
    #         "timestamp": 1527764842,
    #     }
    #     "provider_sig": "0d9sa90f/d9sa0f09dsa89d0sa8/fd90sa8f9-08s9df0-as 7d89f7890?fsd89/0xvhuionv"
    # }

    # validate params
    try:
        provider_request = params['provider_request']
        provider_sig = params['provider_sig']

        address = provider_request['address']
        # address = address.lower()
        hash = provider_request['hash']
        timestamp = provider_request['timestamp']
    except Exception:
        return generate_json_response({'status': 400, 'msg': 'missing request params'})

    if not address or not hash or not timestamp:
        return generate_json_response({'status': 400, 'msg': 'containing empty field'})

    # verify sign
    sig_verify_result = engine.instance.layernode_sdk.verify_provider_signature(
        provider_request, provider_sig, address)
    if sig_verify_result > 0:
        return generate_json_response({'status': 400, 'msg': 'signature_verify failed', 'err_code': sig_verify_result+200})

    # check balance
    try:
        add_result = engine.instance.blockchain.add_request(
            {'id': None, 'hash': hash, 'address': address, 'timestamp': timestamp, 'provider_sig': provider_sig})

        if add_result == 0:
            # calc score
            score_data = layer_core.calc_score(address, hash)

            if score_data is None:
                return generate_json_response({'status': 400, 'msg': 'not found any score for the identity'})
            else:
                return generate_json_response({'status': 200, 'msg': 'success', 'data': score_data})
        elif add_result == 1:
            return generate_json_response({'status': 400, 'msg': 'invalid provider address'})
        elif add_result > 200 and add_result < 300:
            return generate_json_response({'status': 400, 'msg': 'signature_verify failed', 'err_code': add_result})
        elif add_result == 3:
            return generate_json_response({'status': 400, 'msg': 'Request existing'})
        elif add_result == 4:
            return generate_json_response({'status': 400, 'msg': 'error occurred'})
        elif add_result == 5:
            return generate_json_response({'status': 400, 'msg': 'containing empty field'})
        elif add_result == 6:
            return generate_json_response({'status': 400, 'msg': 'provider balance is not enough'})
        else:
            return generate_json_response({'status': 400, 'msg': 'unknown error'})
    except Exception as e:
        return generate_json_response({'status': 400, 'msg': str(e)})


@app.route('/peers', methods=['GET', 'POST'])
def peers():
    return generate_json_response(engine.instance.clientdb.get_peers())


@app.route('/node_id', methods=['GET', 'POST'])
def node_id():
    return generate_json_response(engine.instance.db.get('node_id'))


@app.route('/score_count', methods=['GET', 'POST'])
@blockchain_synced
def score_count():
    result = dict(length=engine.instance.db.get('length'),
                  known_length=engine.instance.clientdb.get('known_length'))
    result_text = json.dumps(result)
    return Response(response=result_text, headers={"Content-Type": "application/json"})


@app.route('/identity_count', methods=['GET', 'POST'])
@blockchain_synced
def identity_count():
    result = dict(identity_length=engine.instance.db.get('identity_length'),
                  known_identity_length=engine.instance.clientdb.get('known_identity_length'))
    result_text = json.dumps(result)
    return Response(response=result_text, headers={"Content-Type": "application/json"})


@app.route('/request_count', methods=['GET', 'POST'])
@blockchain_synced
def request_count():
    result = dict(request_length=engine.instance.db.get('request_length'),
                  known_request_length=engine.instance.clientdb.get('known_request_length'))
    result_text = json.dumps(result)
    return Response(response=result_text, headers={"Content-Type": "application/json"})


@app.route('/stop', methods=['GET', 'POST'])
def stop():
    engine.instance.db.put('stop', True)
    shutdown_server()
    print('Closed API')
    engine.instance.stop()
    return generate_json_response('Shutting down')


def generate_json_response(obj):
    result_text = json.dumps(obj, cls=ComplexEncoder)
    return Response(response=result_text, headers={"Content-Type": "application/json"})


def new_score():
    socketio.emit('new_score')


def new_identity():
    socketio.emit('new_identity')


def new_request():
    socketio.emit('new_request')


def peer_update():
    socketio.emit('peer_update')


def cpu_usage(text):
    socketio.emit('cpu_usage', {'message': text})
