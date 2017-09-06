# CCUnRPC
CryptoCurrencies Unified Remote Procedure Call interface

Realize typical unified methods for management of cryptocurrencies daemons as extensions for [Supervisor’s](http://supervisord.org/xmlrpc.html) XML-RPC API.
It is a python-module for supervisord.

Deploy:

Download and unpack to `/usr/lib/python2.7/dist-packages/ccunrpc/`

  files:
  * `__init__.py`
  * `common.py`
  * `rpc_%currency_daemon_name%.py`


Methods:
--------


-
get_height()

    python -c "import xmlrpclib;print xmlrpclib.ServerProxy('http://root:password@localhost:9001/RPC2').ccunrpc.get_height()"


