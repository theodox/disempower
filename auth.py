import hashlib
import datetime
import configparser


_cfg = configparser.ConfigParser()
_cfg.read('conf.ini')


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
