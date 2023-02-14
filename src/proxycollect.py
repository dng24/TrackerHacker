#! /bin/env/python3

from mitmproxy import http, proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core
from mitmproxy.addons.proxyserver import Proxyserver
import sys
import asyncio



class Proxy:

    def request(self, flow: http.HTTPFlow):
        print(flow.request.host)
        print(flow.request.pretty_host)
        
async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)

    master = DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(Proxy())
    
    await master.run()
    return master

asyncio.run(start_proxy('127.0.0.1', 8080))

#addons = [Proxy()]

#opts = options.Options(listen_host = '127.0.0.1', listen_port = 8080)

#dm = DumpMaster(opts, with_termlog=True, with_dumper=False)
#dm.server = ProxyServer()
#m.addons.add(addons)

#try:
#    dm.run()
#except:
#    dm.shutdown()
