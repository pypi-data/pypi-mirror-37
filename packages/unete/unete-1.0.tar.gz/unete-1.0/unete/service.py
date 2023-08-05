from easydict import EasyDict as edict

class Service:

    def __init__(self, module):
        self.module = module
        self.map = map(module)

    def execute (self, url, args = []):
        try:
            method = self.map[url]
        except:
            raise { "statusCode": 404, "code": 'METHOD_NOT_FOUND', "method": url }
        
        return method(*args)

def map (module, base_route = ''):
    routes = edict({})

    for i in module:
        sub_module = module[i]
        route = base_route + '/' + i

        if callable(sub_module):
            routes[route] = sub_module
        elif isinstance(sub_module, edict):
            routes = { **routes, **map(sub_module, route)}
        else:
            routes[route] = (lambda _sub_module: (lambda: _sub_module))(sub_module)
    
    keys = list(routes.keys())
    
    if not base_route:
        routes['/'] = lambda: keys
    
    return routes