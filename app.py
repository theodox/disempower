from bottle import route, run, Bottle, request
import interval
import re
import configparser
import hashlib
import datetime

_cfg = configparser.ConfigParser()
_cfg.read('conf.ini')

app = Bottle()


def blake(bytes):
    h = hashlib.blake2b()
    h.update(bytes)
    return h.hexdigest()


SESSIONS = dict()
TIMEOUT = datetime.timedelta(minutes=15)


def validate(user, password):
    hashed = blake(password.encode('utf-8'))
    try:
        return hashed == _cfg[user]['password']
    except KeyError:
        return False


def login(user, password):
    if validate(user, password):
        SESSIONS.clear()
        expires = datetime.datetime.now()
        expires += TIMEOUT
        key = str(int(expires.timestamp())) + user
        token = blake(key.encode('utf-8'))
        SESSIONS[token] = expires
        return token
    return None


def logout(request):

    session_id = request.POST.get('session', request.GET.get('session', None))

    print ("logout", session_id)
    try:
        del SESSIONS[session_id]
    except KeyError:
        pass


def in_session(request):
    session_id = request.POST.get('session', request.GET.get('session', None))

    print ("session id", session_id)
    timeout = SESSIONS.get(session_id, False)
    if not session_id or not timeout:
        print ("no session")
        return 0
    if timeout > datetime.datetime.now():
        print ("valid session")
        return 1
    else:
        print ("session timed out")
        del SESSIONS[session_id]
        return -1

#------------------


@app.route("/login")
@app.route("/login", method = "POST")
def temp_login():

    sesh = login('admin', 'vir clarissimus')
    return sesh

@app.route('/logout')
@app.route('/logout', method="POST")
def temp_logout():
    logout(request)

@app.route('/forbidden')
def not_authorized():
    return "You must be logged in to access this function"


@app.route('/check/<user>')
def check_user(user):
    return {
        'user': interval.check(user),
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route('/credit/<user>/<amount:int>')
def add_credit(user, amount):
    interval.add_credit(user, amount)
    return {
        'user': user,
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route("/interval/<user>/<numbers>")
def add_interval(user, numbers):
    if not in_session(request):
        return not_authorized()

    tokens = [int(k) for k in numbers.split(",")]
    if len(tokens) == 6:
        start = tokens[0:3]
        end = tokens[3:6]
        interval.add_interval(user, start, end)

        return {
            'user': user,
            'start': start,
            'end': end,
            'succeed': True,
            'result': interval.INTERVALS.get(user)
        }
    else:
        return {
            'user': user,
            'succeed': False,
            'result': interval.INTERVALS.get(user)
        }


@app.route("/blackout/<user>/<numbers>")
def add_blackout(user, numbers):
    tokens = [int(k) for k in numbers.split(",")]
    if len(tokens) == 6:
        start = tokens[0:3]
        end = tokens[3:6]
        interval.add_blackout(user, start, end)

        return {
            'user': user,
            'start': start,
            'end': end,
            'succeed': True,
            'result': interval.BLACKOUTS.get(user)
        }
    else:
        return {
            'user': user,
            'succeed': False,
            'result': interval.BLACKOUTS.get(user)
        }


@app.route("/daily/<user>/<amount:int>")
def set_daily(user, amount):
    interval.set_daily_allowance(user, amount)
    return {
        'user': user,
        'daily': interval.get_daily_allowance(user)
    }


@app.route("/weekly/<user>/<amount:int>")
def set_weekly(user, amount):
    interval.set_weekly_allowance(user, amount)
    return {
        'user': user,
        'weekly': interval.get_weekly_allowance(user)
    }


@app.route("/status/<user>")
def status(user):

    available = interval.check(user)
    daily = interval.get_daily_allowance(user)
    weekly = interval.get_weekly_allowance(user)
    credits = interval.get_credits(user)
    cap = interval.get_cap(user)
    intevals = interval.get_intervals(user)

    return {'available': available,
            'daily': daily,
            'weekly': weekly,
            'credits': credits,
            'cap': cap,
            'intevals': intevals,
            'user': user
            }


interval.DAILY_BANK['nicky'] = 10
interval.add_interval('nicky', (6, 15, 0), (6, 23, 0))

app.run(host='localhost', port=8080)
