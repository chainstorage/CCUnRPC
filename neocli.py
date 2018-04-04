# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for neo-cli

import requests
from requests.auth import HTTPBasicAuth
import sys
import xmlrpclib
import json
from copy import deepcopy


class CCunRPCmain():

    def __init__(self, supervisord, daemon_config):
        self.supervisord = supervisord
        self.daemon_config = daemon_config
        self.rpc_url = 'http://127.0.0.1'
        self.rpcuser = ''
        self.rpcpassword = ''
        self.data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': '',
            'params': []
        }
        self.payload = {
            'data': '',
            'status': "Error"
        }

        # Read currency daemons config for RPC-acccess credentials
        with open(self.daemon_config) as conf_file:
            config_file = json.load(conf_file)
            # if config with error we must EXIT
            rpc_port = config_file['ApplicationConfiguration']['RPC']['Port']
            self.rpc_url = "{}:{}".format(self.rpc_url, rpc_port)

    def _request_wrapper(self, api_function, params=None):
        if not params:
            params = []
        data = deepcopy(self.data)
        data['method'] = api_function
        data['params'] = params

        r = requests.post(self.rpc_url, auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword), json=data)
        r.raise_for_status()
        result = r.json()
        if 'error' in result.keys():
            self.payload['data'] = r.json()['error']
        else:
            self.payload['data'] = r.json()['result']
            self.payload['status'] = 'OK'
        return self.payload

    def get_height(self):
        """Method return current cryptodaemon height"""
        api_function = 'getblockcount'
        return self._request_wrapper(api_function)

    def get_status(self):
        api_function = 'getpeers'
        payload = self._request_wrapper(api_function)
        if payload['status'] == 'OK':
            self.payload['data'] = payload['data']['connected']
        return self.payload

    def get_wallet(self):
        """Return the xmlrpclib.Binary object with current wallet."""
        # TODO: create method for backup wallet.
        return


def make_main_rpcinterface(supervisord, **config):
    daemon_config = config.get('daemon_config')
    main_rpcinterface = CCunRPCmain(supervisord, daemon_config)
    return main_rpcinterface
