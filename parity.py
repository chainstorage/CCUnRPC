# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface
# Implement API for parity

import requests
from requests.auth import HTTPBasicAuth
import sys
import xmlrpclib
from subprocess import check_output, CalledProcessError, STDOUT


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
        r = requests.post(self.rpc_url,
                          auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword),
                          json=data)
        if r.status_code == requests.codes.ok:
            self.payload['data'] = int(r.json()['result'], 0)
            self.payload['status'] = 'OK'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload

    def get_wallet(self):
        """
        Return the xmlrpclib.Binary object with current wallet.
        For 'parity' it is gzipped tar archive of 'keys' directory.
        """
        try:
            res = check_output("tar czf /secrets/wallet.tgz *",
                               cwd='/secrets/keys', stderr=STDOUT, shell=True)
        except CalledProcessError as e:
            self.payload['status'] = 'Error'
            self.payload['data'] = 'RC {}: {}'.format(e.returncode, e.output)
            return self.payload

        try:
            with open('/secrets/wallet.tgz', 'rb') as w_bak:
                self.payload['data'] = xmlrpclib.Binary(w_bak.read())
            self.payload['file_type'] = 'tgz'
            self.payload['status'] = 'OK'
        except IOError:
            self.payload['data'] = 'Can not read /secrets/wallet.tgz'
            self.payload['status'] = 'Error'
        return self.payload


def make_main_rpcinterface(supervisord):
    main_rpcinterface = CCunRPCmain(supervisord)
    return main_rpcinterface
