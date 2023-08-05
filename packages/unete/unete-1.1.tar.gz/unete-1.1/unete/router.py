import service
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from easydict import EasyDict as edict

class Router:

    def __init__ (self, module, config = {}):
        config = edict(config)

        self.service = service.Service(module)
        try:
            self.host = config.host
        except:
            self.host = "0.0.0.0"
         
        self.port = config.port
    
    def route (self, url, args):
        return self.service.execute(url, args)
    
    def serve (self):
        self.server = HTTPServer((self.host, self.port), self.Handler())

        print("Server running at: http://" + self.host + ":" + str(self.port))

        self.server.serve_forever()
    
    def Handler (self):

        class BaseHandler(BaseHTTPRequestHandler):
            def do_GET (sock):
                sock.send_response(200)

                sock.send_header('Content-type','application/json')
                sock.end_headers()

                sock.wfile.write(bytes(json.dumps({
                    "status": "err",
                    "result": "METHOD_UNSUPPORTED"
                }), "utf8"))
        
            def do_POST (sock):
                _json = {}

                try:
                    str = ""
                    data = sock.rfile.read(int(sock.headers['content-length']))
                    args = json.loads(data.decode("utf8"))

                    _json = { "status": "ok", "result": self.route(sock.path, args)}
                except Exception as exc:
                    _json = { "status": "err", "result": exc.args }
                
                sock.send_response(200)

                sock.send_header('Content-type','application/json')
                sock.end_headers()

                sock.wfile.write(bytes(json.dumps(_json), "utf8"))
                sock.connection.close()

        return BaseHandler