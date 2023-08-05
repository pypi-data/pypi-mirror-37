from easydict import EasyDict as edict
import http.client
import json

class Connector:
    
    def __init__(self, host):
        self.host = host
        self.map  = edict({})
        self.client = http.client.HTTPConnection(self.host)
    
    def init (self):
        map = self.post('/')
        self.map = self.unmap(map)

    def post (self, method, data = [] ):
        hrequest = self.client.request('POST', method, json.dumps(data))
        hresponse = self.client.getresponse()
        
        result = edict(json.load(hresponse))

        if result.status != 'ok':
            raise Exception(result.result)
        try:
            return result.result
        except:
            return
    
    def unmap (self, array = []):
        map = edict({})

        for url in array:
            keys = url.split('/')
            ref = map

            for i in range(0, len(keys) - 1):
                key = keys[i]
                if not key:
                    continue
                try:
                    ref = map[key]
                except:
                    ref = edict({})
                    map[key] = ref
                
            key = keys[len(keys) - 1]
            
            ref[key] = (lambda _url: lambda *data: self.post(_url, data))(url)
        
        return map

def Connect(host):
    connector = Connector(host)
    connector.init()
    return connector.map