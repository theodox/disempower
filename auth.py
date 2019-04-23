import hashlib
import datetime
import configparser


_cfg = configparser.ConfigParser()
_cfg.read('conf.ini')

SECRET = _cfg['auth']['secret']


def blake(bytes):
    h = hashlib.blake2b()
    h.update(bytes)
    return h.hexdigest()


SESSIONS = {}


def validate(user, password):
    hashed = blake(password.encode('utf-8'))
    try:
        return hashed == _cfg[user]['password']
    except KeyError:
        return False


def login(user, password):
    if validate(user, password):
        SESSIONS.clear()
        timeval = datetime.datetime.now().timestamp()
        key = str(int(timeval)) + "%?" + user
        token = blake(key.encode('utf-8'))
        SESSIONS[token] = user
        return token, SECRET
    return None, SECRET


def logout(request):

    session_id = request.get_cookie('session', secret=SECRET)
    print ("logout", session_id)
    try:
        del SESSIONS[session_id]
    except KeyError:
        pass


def in_session(request):
    session_id = request.get_cookie('session', secret=SECRET)
    return SESSIONS.get(session_id, None)

 