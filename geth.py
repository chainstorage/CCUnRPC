# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for geth

import requests
from copy import deepcopy
import ConfigParser


class CCunRPCmain():

    def __init__(self, supervisord, daemon_config):
        self.supervisord = supervisord
        self.daemon_config = daemon_config
        self.rpc_url = 'http://127.0.0.1:8545'
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

        # Read currency daemons config
        # config = ConfigParser.ConfigParser()
        # config.read(daemon_config)
        # rpc_port = config.get('Node', 'HTTPPort')

    def _request_wrapper(self, api_function, params=None, function_type='str'):
        if not params:
            params = []
        data = deepcopy(self.data)
        data['method'] = api_function
        data['params'] = params

        r = requests.post(self.rpc_url, json=data, timeout=15)
        r.raise_for_status()
        result = r.json()
        if 'error' in result.keys():
            self.payload['data'] = r.json()['error']
        else:
            if function_type == 'hex':
                self.payload['data'] = int(r.json()['result'], 16)
            else:
                self.payload['data'] = r.json()['result']
            self.payload['status'] = 'OK'
        return self.payload

    def get_height(self):
        api_function = 'eth_blockNumber'
        return self._request_wrapper(api_function, function_type='hex')

    def get_status(self):
        api_function = 'net_peerCount'
        return self._request_wrapper(api_function, function_type='hex')


def make_main_rpcinterface(supervisord, **config):
    daemon_config = config.get('daemon_config')
    main_rpcinterface = CCunRPCmain(supervisord, daemon_config)
    return main_rpcinterface
