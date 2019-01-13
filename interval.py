
INTERVALS = {}


def to_minutes(day, hour, minute):
    return day * 1440 + hour * 60 + minute


def from_minutes(mins):
    day = mins % 1440
    remainder = mins - (day * 1440)
    hour = remainder % 60
    minute = remainder - (hour * 60)
    return day, hour, minute


def create(start_tuple, end_tuple):
    return to_minutes(*start_tuple), to_minutes(*end_tuple)


def add(user, interval):
    start, end = interval
    if user not in INTERVALS:
        INTERVALS[user] = []

    insert_at = 0
    for idx, val in enumerate(INTERVALS[user]):
        valstart, valend = val
        if val == interval:
            return
        if valstart < start:
            insert_at = idx + 1
        else:
            break

    INTERVALS[user].insert(insert_at, interval)


def remove(user, interval):
    idx = INTERVALS[user].index(interval)
    del INTERVALS[user][idx]


def check(user, now_tuple):
    minutes = to_minutes(*now_tuple)
    for i_start, i_end in INTERVALS[user]:
        if i_start <= minutes <= i_end:
            return i_end - minutes

    return 0


def save():
    with open('interval_db', 'w') as handle:
        handle.write("{")
        serialized = ["'{}':{}".format(name, INTERVALS[name]) for name in INTERVALS]
        handle.write(", ".join(serialized))
        handle.write("}\n")


def load():
    try:
        with open('interval_db', 'r') as handle:
            text = handle.read()

        interval_data = eval(text)
        INTERVALS.clear()
        INTERVALS.update(interval_data)
        return len(INTERVALS)
    except IOError:
        return 0
