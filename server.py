import sys
is_micropython = 'WiPy' in sys.platform

if not is_micropython:
    import socket
    partition = str.partition
    from traceback import format_exc
else:
    import usocket as socket

    def format_exc(limit=None, chain=True):
        exc, val, _ = sys.exc_info()
        return repr(exc) + '\n' + repr(val)

    def partition(py_string, sep):
        if not py_string:
            return '', '', ''
        idx = str.index(py_string, sep)
        if idx <= 0:
            return py_string, '', ''
        else:
            return py_string[:idx], py_string[idx], py_string[idx + 1:] if len(py_string) > idx else ''

ERROR = """\
HTTP/1.0 500 Internal Server Error

<html>
<h3>500 server error</h3>
</div color='0x999999'>
<pre>
{err}
</pre>
</div>
<div>
original request:
{req}
</div>
</html>
"""

CONTENT = """\
HTTP/1.0 200 OK

<html>
{}
</hmtl>
"""

NOT_FOUND = """\
HTTP/1.0 404 Not Found

<html>
{} not found
</html>
"""

ROUTES = dict()


def route_not_found(req):
    """
    returns the 404 for a URL that is not in the routes table
    """
    return NOT_FOUND.format(req.get('url', 'URL')).encode('utf-8')


def route(rt, method="GET"):
    """
    a flask-style route decorator for functions. Return results
    as strings, the decorator will handle the rest
    """
    def deco(fn):
        def wrapped(req):
            try:
                result = fn(req)
                return CONTENT.format(result).encode('utf-8')
            except Exception:
                result = format_exc()
                return ERROR.format(err=result, req=req).encode('utf-8')

        ROUTES[(rt, method)] = wrapped
        return wrapped
    return deco


def parse_request(stream):
    results = {}
    hdr_line = stream.readline().decode('utf-8')
    if not hdr_line:
        return results
    method, url, protocol = hdr_line.split(' ')
    results['method'] = method.strip()
    results['protocol'] = protocol.strip()
    try:
        route, items = url.split('?')
        query = {}
        for kvp in items.split("&"):
            try:
                k, v = kvp.split("=")
                query[k] = v.strip()
            except ValueError:
                query[kvp] = True
    except ValueError:
        route, query = url, {}
    results['url'] = route
    results['query'] = query

    while hdr_line not in ('', '\r\n'):
        try:
            hdr_line = stream.readline().decode('utf-8')
            if len(hdr_line) > 2:
                key, _, value = partition(hdr_line, ":")
                results[key] = value.strip()
        except Exception as e:
            results['error'] = str(e)
            break

    return results


def main(is_micropython=False):
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        try:
            client_socket, _ = s.accept()

            if not is_micropython:
                # cpython
                client_stream = client_socket.makefile("rwb")
            else:
                # micropython
                client_stream = client_socket

            req = parse_request(client_stream)
            if req and req['url']:  # skip malformed requests
                handler = ROUTES.get(
                    (req['url'], req['method']),
                    route_not_found
                )
                client_stream.write(handler(req))

            client_stream.close()
            if not is_micropython:
                client_socket.close()

        except Exception as e:
            print("SERVER ERROR")
            print(repr(e))

            break


def serve():
    print("server started (optimize:{})".format(is_micropython))
    main(is_micropython)
