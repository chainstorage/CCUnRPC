# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for bitcoind

import requests
from requests.auth import HTTPBasicAuth
import sys
import xmlrpclib


class CCunRPCmain():
    def __init__(self, supervisord, daemon_config):
        self.supervisord = supervisord
        self.daemon_config = daemon_config
        self.rpc_url = 'http://127.0.0.1:8332'
        self.rpcuser = ''
        self.rpcpassword = ''
        self.payload = {'data': '',
                        'status': 'OK'}
        # Read currency daemons config for RPC-acccess credentials
        with open(self.daemon_config) as conf_file:
            for line in conf_file.readlines():
                if line.split("=")[0].strip() == "rpcuser":
                    self.rpcuser = line.split("=")[1].strip()
                elif line.split("=")[0].strip() == "rpcpassword":
                    self.rpcpassword = line.split("=")[1].strip()
                elif line.split("=")[0].strip() == "rpcport":
                    port = line.split("=")[1].strip()
                    self.rpc_url = "http://127.0.0.1:{}".format(port)

    def get_height(self):
        data = {
            'jsonrpc': '1.0',
            'id': 'curltest',
            'method': 'getinfo',
            'params': []
        }
        r = requests.post(self.rpc_url,
                          auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword),
                          json=data)
        if r.status_code == requests.codes.ok:
            self.payload['data'] = r.json()['result']['blocks']
            self.payload['status'] = 'OK'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload

    def get_wallet(self):
        """Return the xmlrpclib.Binary object with current wallet."""
        data = {
            'jsonrpc': '1.0',
            'id': 'curltest',
            'method': 'backupwallet',
            'params': ['/secrets/wallet.backup']
        }
        r = requests.post(self.rpc_url,
                          auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword),
                          json=data)
        if r.status_code == requests.codes.ok:
            try:
                with open('/secrets/wallet.backup', 'rb') as w_bak:
                    self.payload['data'] = xmlrpclib.Binary(w_bak.read())
                self.payload['file_type'] = 'dat'
                self.payload['status'] = 'OK'
            except IOError:
                self.payload['data'] = 'Can not read /secrets/wallet.backup'
                self.payload['status'] = 'Error'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload


def make_main_rpcinterface(supervisord, **config):
    daemon_config = config.get('daemon_config')
    main_rpcinterface = CCunRPCmain(supervisord, daemon_config)
    return main_rpcinterface
