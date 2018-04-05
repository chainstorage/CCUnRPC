#!/usr/bin/python
# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for bitcoind

import requests
from requests.auth import HTTPDigestAuth


class CCunRPCmain():
    def __init__(self, supervisord, daemon_config):
        self.supervisord = supervisord
        self.daemon_config = daemon_config
        self.rpc_url = 'http://127.0.0.1:18081/'
        self.rpcuser = ''
        self.rpcpassword = ''
        self.payload = {'data': '',
                        'status': 'OK'}

    def get_height(self):
        self.rpc_url = 'http://127.0.0.1:18081/getheight'
        r = requests.post(self.rpc_url,
                          auth=HTTPDigestAuth(self.rpcuser, self.rpcpassword),
                          timeout=15)
        if r.status_code == requests.codes.ok:
            self.payload['data'] = r.json()['height']
            self.payload['status'] = 'OK'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload


def make_main_rpcinterface(supervisord, **config):
    daemon_config = config.get('daemon_config')
    main_rpcinterface = CCunRPCmain(supervisord, daemon_config)
    return main_rpcinterface
