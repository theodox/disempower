try:
    import usocket as socket
except:
    import socket

import sys
import traceback
optimize = 'WiPy' in sys.platform


ERROR = """\
HTTP/1.0 500 Internal Server Error

<html>
<pre>
{}
</pre>

<h3> request</h3>
<pre>
{}
</pre>
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


def not_found(req):
    """
    returns the 404 for a URL that is not in the routes table
    """
    return NOT_FOUND.format(req.get('url', 'URL')).encode('utf-8')


def route(rt):
    """
    a flask-style route decorator for functions. Return results
    as strings, the decorator will handle the rest
    """
    def deco(fn):
        def wrapped(req):
            try:
                result = fn(req)
                return CONTENT.format(result).encode('utf-8')
            except Exception as e:
                result = traceback.format_exc()
                return ERROR.format(result, req).encode('utf-8')

        ROUTES[rt] = wrapped
        return wrapped
    return deco


def parse_request(stream):
    results = {}
    hdr_line = stream.readline().decode('utf-8')
    if not hdr_line:
        return results
    method, url, protocol = hdr_line.split(' ')
    results['method'] = method
    results['protocol'] = protocol
    try:
        route, items = url.split('?')
        query = {}
        for kvp in items.split("&"):
            try:
                k, v = kvp.split("=")
                query[k] = v
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
                key, _, value = hdr_line.partition(":")
                results[key] = value
        except Exception as e:
            results['error'] = str(e)
            break

    return results


def main(micropython_optimize=False):
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        req = parse_request(client_stream)
        url = req.get('url')

        handler = ROUTES.get(url, not_found)
        client_stream.write(handler(req))

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        counter += 1
        print()


def serve():
    print("server started (optimize:{})".format(optimize))
    main(optimize)
