import uuid
import os
from cdecimal import Decimal
from layernode import tools

version = "0.001"


def generate_default_config():
    config = dict()
    config['DEBUG'] = False
    config['database'] = {
        'DB_USERNAME': 'layer_user',
        'DB_PASSWORD': 'layer_password',
        'DB_HOST': 'localhost',
        'DATABASE_NAME': 'layernode'
    }

    config['logging'] = {
        'file': 'log'
    }

    config["port"] = {
        "api": int(os.environ.get('LAYERNODE_API_PORT', '7001')),
        "peers": int(os.environ.get('LAYERNODE_PEERS_PORT', '7002'))
    }

    config["peers"] = {
        "list": [
            {
                'node_id': 'b56c5fb7-00bd-45c7-abe0-b35ca8e5dcc4',
                'ip': '18.212.123.235',
                'port': 7002,
                'rank': 1,
                'length': -1,
                'identity_length': -1,
                'request_length': -1
            },
            {
                'node_id': '4efc4993-43f8-4701-8087-9aa5859ded7e',
                'ip': '54.164.121.250',
                'port': 7002,
                'rank': 1,
                'length': -1,
                'identity_length': -1,
                'request_length': -1
            }
        ],
        "download_limit": 190
    }

    config['my_ip'] = '127.0.0.1'
    config['geth_rpc_host'] = 'http://localhost:8545'
    config['signer_endpoint'] = 'http://34.201.171.237:5000'
    config['LAYERNODE_API_HOST'] = '0.0.0.0'

    # ipfs setting
    config['ipfs'] = {
        'ip': '18.208.251.253',
        'port': '5001'
    }

    return config


def read_config_file(file_address):
    import yaml
    config = yaml.load(open(file_address, 'rb'))
    if 'DEBUG' in config.keys():
        return config
    else:
        return None


def write_config_file(config, file_address):
    import yaml
    yaml.dump(config, open(file_address, 'w'))


def extract_configuration(dir, config):
    if dir is None:
        working_dir = tools.get_default_dir()
    else:
        working_dir = dir

    working_dir = os.path.join(working_dir, str(version))

    if os.path.exists(working_dir) and not os.path.isdir(working_dir):
        print("Given path {} is not a directory.".format(working_dir))
        exit(1)
    elif not os.path.exists(working_dir):
        print("Given path {} does not exist. Attempting to create...".format(working_dir))
        try:
            os.makedirs(working_dir)
            print("Successful")
        except OSError:
            print("Could not create a directory!")
            exit(1)

    if config is not None:
        config = read_config_file(config)
    elif os.path.exists(os.path.join(working_dir, 'config')):
        config = os.path.join(working_dir, 'config')
        config = read_config_file(config)
    else:
        config = generate_default_config()
        write_config_file(config, os.path.join(working_dir, 'config'))

    if config is None:
        raise ValueError('Couldn\'t parse config file {}'.format(config))

    return config, working_dir
