#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functools import wraps
from inspect import Parameter
from pprint import pprint

import requests

from layernode import custom
from layernode import engine
from layernode import tools


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


actions = dict()
connection_port = 7899
host = os.environ.get('LAYERNODE_API_HOST', 'localhost')


def action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    global actions
    actions[func.__name__] = wrapper
    return wrapper


def make_api_request(method, files=None, **kwargs):
    from requests_toolbelt import MultipartEncoder
    if files is None:
        files = {}
    url = "http://" + str(host) + ":" + str(connection_port) + "/" + method

    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if len(files) > 0:
        fields = {}
        fields.update(kwargs)
        fields.update(files)
        m = MultipartEncoder(fields=fields)
        response = requests.post(url, data=m, headers={
                                 'Content-Type': m.content_type})
    else:
        response = requests.post(url, data=kwargs)
    if response.status_code != 200:
        return {
            'error': response.status_code,
            'message': response.text
        }
    else:
        return response.json()


@action
def start():
    config, working_dir = custom.extract_configuration(dir=None, config=None)
    tools.init_logging(config['DEBUG'], working_dir, config['logging']['file'])
    engine.main(config, working_dir)


@action
def node_id():
    print(make_api_request("node_id"))


@action
def peers():
    peers = make_api_request("peers")
    pprint(peers)


@action
def stop():
    print(make_api_request("stop"))


@action
def score_count():
    result = make_api_request("score_count")
    pprint(result)


@action
def identity_count():
    result = make_api_request("identity_count")
    pprint(result)


def run(argv):
    parser = argparse.ArgumentParser(description='CLI for layernode.')
    parser.add_argument('action', choices=sorted(actions.keys()),
                        help="Main action to perform by this CLI.")
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + custom.version)

    args = parser.parse_args(argv[1:])

    config, working_dir = custom.extract_configuration(dir=None, config=None)
    global connection_port
    connection_port = config['port']['api']

    from inspect import signature
    sig = signature(actions[args.action])
    kwargs = {}
    for parameter in sig.parameters.keys():
        if sig.parameters[parameter].default == Parameter.empty and \
                (not hasattr(args, parameter) or getattr(args, parameter) is None):
            sys.stderr.write("\"{}\" requires parameter {}\n".format(
                args.action, parameter))
            sys.exit(1)
        kwargs[parameter] = getattr(args, parameter)
    actions[args.action](**kwargs)
    return


def main():
    if sys.stdin.isatty():
        run(sys.argv)
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)


if __name__ == '__main__':
    run(sys.argv)
