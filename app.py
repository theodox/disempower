from server import route, serve, is_micropython

if is_micropython:
    from machine import Pin
else:
    class Pin (object):
        OUT = 1

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, val):
            pass

RELAY = Pin("P1", mode=Pin.OUT)
RELAY(0)


@route("/test")
def test(request):
    result = []
    result.append("<h3>request:</h3>")
    for k, v in request.items():
        result.append(" ".join((k, ":", str(v))))
    return "<br>".join(result)

@route("/on")
def turn_on(request):
    print("power ON")
    RELAY(1)
    return "<h1>power on</h1>"


@route("/off")
def turn_off(request):
    print("power OFF")
    RELAY(0)
    return "<h1>power off</h1>"


@route("/stop")
def turn_off(request):
    try:
        print("server shutdown requested")
        return "server shutting down"
    finally:
        raise SystemExit()


serve()
