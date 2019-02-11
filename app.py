from server import route, serve, is_micropython
import machine
import time

CLOCK = machine.RTC()
CLOCK.init((2019, 1, 1, 12, 0))

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

WEEKDAYS = 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun'


@route("/set_clock")
def set_clock(request):
    print(request)
    global CLOCK
    query = request.get('query')
    if not query:
        return "<h3>unable to parse query</h3>"

    year = int(query['year'])
    month = int(query['month'])
    day = int(query['day'])
    hour = int(query['hour'])
    minute = int(query['min'])

    CLOCK.init((year, month, day, hour, minute))

    return "<h3>clock set</h3>"


@route("/time")
def clock_time(request):

    now = time.localtime()
    day = WEEKDAYS[now[-2] % 6]
    H = now[3]
    M = now[4]
    return '<h3>{}:{}:{}</h3>'.format(day, H, M)


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
