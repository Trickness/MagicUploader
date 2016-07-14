# coding=utf8

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCDispatcher

def list_files():
    return "HEllo"

class RequestHandler(SimpleXMLRPCRequestHandler):
#    rpc_paths = ('http://localhost/',)
    def end_headers(self):
        self.send_header("Access-Control-Allow-Headers",
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleXMLRPCRequestHandler.end_headers(self)

server = SimpleXMLRPCServer(("", 8080),allow_none=True,requestHandler=RequestHandler)
server.register_function(list_files)
print ("RPC Started")
server.serve_forever()