import gevent
import gevent.pywsgi
import gevent.queue
import base64
import random
import string

from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport

dispatcher = RPCDispatcher()
transport = WsgiServerTransport(
    max_content_length=100 * 1024,
    queue_class=gevent.queue.Queue
)

# start wsgi server as a background-greenlet
wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 5000), transport.handle)
gevent.spawn(wsgi_server.serve_forever)

rpc_server = RPCServerGreenlets(
    transport,
    JSONRPCProtocol(),
    dispatcher
)

def write_file(data, filename=None):
    if filename is None:
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"received_{random_suffix}.bin"
    with open(filename, "wb") as f:
        f.write(data)
    return filename

@dispatcher.public
def upload_file(filename, contents_b64):
    binary_data = base64.b64decode(contents_b64)
    
    # Check if the file is greater than 50 KB (50 * 1024 bytes)
    if len(binary_data) > 50 * 1024:
        return "Error: File exceeds the 50 KB limit"

    saved_name = write_file(binary_data, filename)
    return f"File {saved_name} ({len(binary_data)} bytes) saved successfully"


@dispatcher.public
def reverse_string(s):
    return s[::-1]

# in the main greenlet, run our rpc_server
rpc_server.serve_forever()