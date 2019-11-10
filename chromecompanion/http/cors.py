from bottle import response, request

class cors(object):
    name = 'enable_cors'
    api = 2
    cors_host = '*'
    if not cors_host:
        cors_host = '*'

    def __init__(self, host = '*'):
        self.cors_host = host

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = self.cors_host
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors
