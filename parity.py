# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for parity

import requests
from requests.auth import HTTPBasicAuth

class CCunRPCmain():
    def __init__(self, supervisord):
        self.supervisord = supervisord
        self.rpc_url = 'http://127.0.0.1:8545'
        self.rpcuser = ''
        self.rpcpassword = ''
        self.payload = {'data': '',
                        'status': 'OK'}

    def get_height(self):
        data = {
            'jsonrpc': '2.0',
            'id': '1',
            'method': 'eth_blockNumber',
            'params': []
        }
        r = requests.post(self.rpc_url, auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword), json=data)
        if r.status_code == requests.codes.ok:
            self.payload['data'] = int(r.json()['result'], 0)
            self.payload['status'] = 'OK'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload

def make_main_rpcinterface(supervisord):
    main_rpcinterface = CCunRPCmain(supervisord)
    return main_rpcinterface
