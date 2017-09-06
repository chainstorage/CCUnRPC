# CCUnRPC
CryptoCurrencies Unified Remote Procedure Call interface

It is a python-module for supervisord.
Realize typical unified methods for management of cryptocurrencies daemons as extensions for [Supervisor’s](http://supervisord.org/xmlrpc.html) XML-RPC API.


Deploy:
-------

Download and unpack to `/usr/lib/python2.7/dist-packages/ccunrpc/`

  files:
  * `__init__.py`
  * `common.py`
  * `rpc_%currency_daemon_name%.py`

Example supervisord config:
---------------------------

    [rpcinterface:ccunrpc]
    supervisor.rpcinterface_factory = ccunrpc.common:make_main_rpcinterface
    daemon = bitcoind
    daemon_config = /config/bitcoin.conf

Methods:
--------

- `get_height()` - Get current height

    python -c "import xmlrpclib;print xmlrpclib.ServerProxy('http://root:password@localhost:9001/RPC2').ccunrpc.get_height()"

