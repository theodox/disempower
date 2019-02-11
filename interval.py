import time

CREDITS = {}
INTERVALS = {}
BLACKOUTS = {}

WEEK = 10080

def to_minutes(day, hour, minute):
    '''week-day, hour, minute to minuts.  days are 0-6'''
    return day * 1440 + hour * 60 + minute


def from_minutes(mins):
    day = mins % 1440
    remainder = mins - (day * 1440)
    hour = remainder % 60
    minute = remainder - (hour * 60)
    return day, hour, minute


def create(start_tuple, end_tuple):
    return to_minutes(*start_tuple), to_minutes(*end_tuple)


def _add(user, interval, dictionary):
    start, end = interval
    if user not in dictionary:
        dictionary[user] = []

    insert_at = 0
    for idx, val in enumerate(dictionary[user]):
        valstart, valend = val
        if val == interval:
            return
        if valstart < start:
            insert_at = idx + 1
        else:
            break

    dictionary[user].insert(insert_at, interval)


def _remove(user, interval, dictionary):
    idx = dictionary[user].index(interval)
    del dictionary[user][idx]


def add_interval(user, interval):
    _add(user, interval, INTERVALS)


def add_blackout(user, interval):
    _add(user, interval, BLACKOUTS)


def remove(user, interval):
    _remove(user, interval, INTERVALS)


def remove_blackout(user, interval):
    _remove(user, interval, BLACKOUTS)


def add_credit(user, amount):
    total = CREDITS.get(user, 0)
    total += amount
    CREDITS[user] = total


def check(user):
    """
    returns positive # of minutes remaining,
    0 if not in an active interval, 
    negative number of minutes to the end of current blackout

    """


    minutes = now_minutes()

    remaining = 0
    for i_start, i_end in INTERVALS.get(user, []):
        if i_start <= minutes <= i_end:
            remaining = i_end - minutes

    if remaining:
        for b_start, b_end in BLACKOUTS.get(user, []):
            if b_start <= minutes <= b_end:
                return -1 * (b_end - minutes)

    user_total = CREDITS.get(user, 0)
    return min(remaining, user_total)


def save(dictionary, filename):
    with open(filename, 'w') as handle:
        handle.writelines(str(dictionary))


def load(filename):
    try:
        with open(filename, 'r') as handle:
            text = handle.read()
            return eval(text)
    except:
        return dict()


def TEST():
    CREDITS['test'] = 30
    began = (now_minutes() - 12) % WEEK
    ends = (now_minutes() + 30) % WEEK


def now_minutes():
    now = time.localtime()
    day = now[-2]
    H = now[3]
    M = now[4]
    return to_minutes(day, H, M)
