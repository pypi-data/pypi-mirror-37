import bottle


def __cors_dict(origin=None):
    origin = '*' if origin is None else origin
    cors_string = 'Origin, Accept , Content-Type, X-Requested-With, X-CSRF-Token'
    CORS_HEADERS = {'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
                    'Access-Control-Allow-Headers': cors_string,
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Origin': origin}
    return CORS_HEADERS


def abort(code=500, text='Unknown Error.'):
    """ Aborts execution and causes a HTTP error. """
    origin = bottle.request.headers.get('Origin')
    d = __cors_dict(origin)
    raise bottle.HTTPError(code, text, **d)


def add_cors(app, allow_credentials=True):
    @app.hook('after_request')
    def add_cors_headers():
        origin = bottle.request.headers.get('Origin')
        d = __cors_dict(origin)
        bottle.response.headers.update(d)

    def docstring_fn(fn, method):
        def newfn():
            doc = fn.__doc__
            doc = 'No docstring' if doc is None else doc
            return method + '\n' + doc
        return newfn

    new_routes = []
    for route in app.routes:
        if route.method != 'OPTIONS':
            new_routes.append((route.rule, docstring_fn(route.callback,
                                                        route.method)))
    for r, fn in new_routes:
        app.route(r, method=['OPTIONS'])(fn)

    return app
