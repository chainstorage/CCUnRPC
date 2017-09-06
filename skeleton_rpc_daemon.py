import requests
from requests.auth import HTTPBasicAuth
from common import CCunRPC

class CCunRPCmain(CCunRPC):

    def __init__(self, *args):
        super(CCunRPCmain, self).__init__(*args)
        self.rpc_url, self.rpcuser, self.rpcpassword, = self.set_credentials()

    payload = {'data': '',
               'status': 'OK'}

    def set_credentials(self):
        """
        Read currensy daemons config for RPC-acccess credentials
        :return: rpc_url, rpcuser, rpcpassword
        """
        rpc_url = 'http://127.0.0.1:8332'
        rpcuser = ''
        rpcpassword = ''
        with open(self.daemon_config) as conf_file:
            for line in conf_file.readlines():
                if line.split("=")[0] == "rpcuser":
                    rpcuser = line.split("=")[1].strip()
                elif line.split("=")[0] == "rpcpassword":
                    rpcpassword = line.split("=")[1].strip()
        return rpc_url, rpcuser, rpcpassword

    def get_height(self):
        data = {
            'jsonrpc': '1.0',
            'id': 'curltest',
            'method': 'getinfo',
            'params': []
        }
        r = requests.post(self.rpc_url, auth=HTTPBasicAuth(self.rpcuser, self.rpcpassword), json=data)
        if r.status_code == requests.codes.ok:
            self.payload['data'] = r.json()['result']['blocks']
            self.payload['status'] = 'OK'
        else:
            self.payload['data'] = r.text
            self.payload['status'] = 'Error'
        return self.payload

