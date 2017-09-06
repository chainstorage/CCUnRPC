# CCUnRPC - CryptoCurrencies Unified Remote Procedure Call interface

import importlib

class CCunRPC(object):
    def __init__(self, supervisord, daemon, daemon_config):
        self.daemon = daemon
        self.daemon_config = daemon_config
        self.supervisord = supervisord

    def get_height(self):
        """
        This method must return current blockchain height
        :return: {'status': 'OK', 'data': 100500}
        """
        raise Exception


def make_main_rpcinterface(supervisord, **config):
    daemon = config.get('daemon')
    daemon_config = config.get('daemon_config')
    import_classfile = importlib.import_module('ccunrpc.rpc_'+daemon)
    main_rpcinterface = getattr(import_classfile, "CCunRPCmain")
    return main_rpcinterface(supervisord, daemon, daemon_config)
