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
        with open(self.daemon_config) as conf_file:
                for line in conf_file.readlines():
                        if line.split("=")[0] == "rpc-login":
                            # self.rpccreds = line.split("=")[1].strip()
                            credentials = line.split("=")[1]
                            self.rpcuser = credentials.split(":")[0]
                            self.rpcpassword = credentials.split(":")[1]


    def get_height(self):
        self.rpc_url = 'http://127.0.0.1:18081/getheight'
        r = requests.post(self.rpc_url, auth=HTTPDigestAuth(self.rpcuser, self.rpcpassword))
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