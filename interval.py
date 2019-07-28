from datetime import datetime, timedelta
from collections import defaultdict
import itertools
import pickle
import time

import logging
logger = logging.getLogger("disempower.interval")

CREDITS = defaultdict(int)      # per-user bank
INTERVALS = defaultdict(list)   # per-user allowable times
BLACKOUTS = defaultdict(list)   # per-user forbidden times
CAPS = dict()                  # per-user max credits
DAILY_BANK = defaultdict(int)  # add every day at 00:00
WEEKLY_BANK = defaultdict(int)  # add every week at 00:00 on Monday

# last tick time per user; -1 if user is inactive
ACTIVE = defaultdict(int)

LAST_TICK = -1
LAST_TOPOFF = 17990

WEEK = 10080
DAY = 1440
HR = 60


# Daylght savings, from Python TZ example code
DSTSTART = datetime(1, 4, 1, 2)
DSTEND = datetime(1, 10, 25, 1)
# these could be configured for other time zones
OFFSET_DST = -420
OFFSET_ST = -480


def get_time_offset(utc):
    def first_sunday_on_or_after(dt):
        days_to_go = 6 - dt.weekday()
        if days_to_go:
            dt += timedelta(days_to_go)
        return dt

    start = first_sunday_on_or_after(DSTSTART.replace(year=utc.year))
    end = first_sunday_on_or_after(DSTEND.replace(year=utc.year))

    if start < utc < end:
        return OFFSET_DST
    else:
        return OFFSET_ST


def to_minutes(day, hour, minute):
    '''week-day, hour, minute to minuts.  days are 0-6'''
    minute_overage = minute // 60
    hour += minute_overage
    minute %= 60

    hour_overage = hour // 24
    day += hour_overage
    hour %= 24
    day %= 7

    return (day * DAY) + (hour * HR) + minute


def from_minutes(mins):
    """
    converts a minute value into a day-hour-minute tuple
    """
    day = mins // 1440
    remainder = mins - (day * 1440)
    hour = remainder // 60
    minute = remainder - (hour * 60)
    return day, hour, minute


def _add(user, start_tuple, end_tuple, target=INTERVALS):

    # ignore zero-length interval
    if start_tuple == end_tuple:
        return

    sd, sh, sm = start_tuple
    ed, eh, em = end_tuple

    wrap = ed < sd
    if wrap:
        start_one = to_minutes(sd, sh, sm)
        end_one = WEEK
        start_two = 0
        end_two = to_minutes(ed, eh, em)
        segments = ((start_two, end_two), (start_one, end_one),)
    else:
        segments = ((to_minutes(sd, sh, sm), to_minutes(ed, eh, em)), )

    for s in segments:
        if s not in target[user]:

            target[user].append(s)
    target[user].sort()


def add_interval(user, st, en):
    _add(user, st, en, INTERVALS)


def add_blackout(user, st, en):
    _add(user, st, en, BLACKOUTS)


def get_ui_blackouts(user):
    as_dates = ((from_minutes(s), from_minutes(e))
                for s, e in BLACKOUTS[user])
    return list(as_dates)


def clear_blackouts(user):
    BLACKOUTS[user].clear()


def clear_intervals(user):
    INTERVALS[user].clear()


def _remove(user, interval, dictionary):
    idx = dictionary[user].index(interval)
    del dictionary[user][idx]


def remove(user, interval):
    _remove(user, interval, INTERVALS)


def remove_blackout(user, interval):
    _remove(user, interval, BLACKOUTS)


def add_credit(user, amount):
    total = CREDITS.get(user, 0)
    total += amount
    CREDITS[user] = total


def set_credit(user, amount):
    CREDITS[user] = amount


def set_cap(user, amount):
    CAPS[user] = amount


def check(user):
    """
    returns positive # of minutes remaining,
    0 if not in an active interval,
    """

    now_minute = tick(user)

    remaining = 0

    for i_start, i_end in get_intervals(user):
        if i_start <= now_minute <= i_end:
            remaining = max(remaining, i_end - now_minute)

    user_total = CREDITS.get(user, 0)

    # FIX:  as written this will return a false
    # countdown to midnight on Sunday if there
    # is a wraparound interval to Monday morning...

    return min(remaining, user_total)


def server_time(now):
    local_time_offset = get_time_offset(now)
    # server runs UTC, but the minute conversion is hard-coded to
    # a simplified version of Pacific time : -7 during the
    # PST interval, -8 the rest of the time
    now_minute = to_minutes(now.weekday() % 7, now.hour, now.minute)
    now_minute += local_time_offset
    now_minute %= WEEK

    return now_minute


def tick(user):

    now = datetime.utcnow()
    daily_topoff(now)

    now_minute = server_time(now)

    recent = ACTIVE[user]
    if recent == -1:
        recent = now_minute

    delta = now_minute - recent
    msg = "time: {}, {}, {}, {}, 'delta', {}, 'credits' {} "
    logger.info(msg.format(now, from_minutes(now_minute), ACTIVE[user], delta, CREDITS[user]))

    # wraparounds for normalized time
    if delta < 0:
        delta += WEEK

    # assume longer interval =  dropped connection
    # expect multiple polls per minute

    if delta > 3:
        delta = 0
        logger.warning("dropped connection")

    CREDITS[user] -= delta
    CREDITS[user] = max(0, CREDITS[user])

    ACTIVE[user] = now_minute
    return now_minute


def daily_topoff(today_datetime):
    global LAST_TOPOFF

    current_day_timestamp = today_datetime.timestamp()
    current_day_serial = int(current_day_timestamp // 86400)

    for d in range(LAST_TOPOFF + 1, current_day_serial + 1):
        next_day = datetime.utcfromtimestamp(d * 86400)
        logger.info(">", next_day)
        local_time_offset = get_time_offset(next_day)
        now_minute = to_minutes(next_day.weekday() %
                                7, next_day.hour, next_day.minute)
        now_minute += local_time_offset
        now_minute %= WEEK
        day_number = now_minute // DAY
        logger.info("topoff {} {}".format(d, day_number))

        for u in DAILY_BANK:
            daily = DAILY_BANK[u] or 0
            logger.info(">D>", daily, DAILY_BANK)
            CREDITS[u] += daily

            if day_number == 0:
                weekly = WEEKLY_BANK[u] or 0
                logger.info(">W>", weekly, WEEKLY_BANK)
                CREDITS[u] += weekly

            CREDITS[u] = min(CREDITS[u], CAPS.get(u, 180))

    LAST_TOPOFF = current_day_serial


def set_cap(user, amount):
    CAPS[user] = amount


def get_cap(user):
    return CAPS.get(user, 180)


def set_daily_allowance(user, amount):
    DAILY_BANK[user] = amount


def get_daily_allowance(user):
    return DAILY_BANK.get(user)


def set_weekly_allowance(user, amount):
    WEEKLY_BANK[user] = amount


def get_weekly_allowance(user):
    return WEEKLY_BANK.get(user)


def set_credits(user, amount):
    CREDITS[user] = amount


def get_credits(user):
    return CREDITS.get(user, 0)


def get_users():
    return INTERVALS.keys()


def delete_user(user):
    for each_dict in (INTERVALS, CREDITS, WEEKLY_BANK, DAILY_BANK, CAPS, BLACKOUTS):
        try:
            each_dict.pop(user)
        except:
            pass


def get_intervals(user):

    logger.debug(str([(from_minutes(s), from_minutes(e)) for s, e in BLACKOUTS[user]]))

    ints = (k for k in INTERVALS[user])
    for b in BLACKOUTS[user]:
        ints = (j for j in blackout_filter(ints, b))

    return (tuple(map(round, t)) for t in ints)


def get_ui_intervals(user):

    as_dates = ((from_minutes(s), from_minutes(e))
                for s, e in get_intervals(user))
    return list(as_dates)


def blackout_filter(interval_stream, blackout):

    for interval in interval_stream:

        if max(*interval) <= min(*blackout):
            yield interval
            continue

        if min(*interval) >= max(*blackout):
            yield interval
            continue

        if min(*blackout) > min(*interval):
            yield ((min(*interval), min(*blackout)))

        if max(*blackout) < max(*interval):
            yield (max(*blackout), max(*interval))


def save(filename):

    state = {
        'CREDITS': CREDITS,
        'INTERVALS': INTERVALS,
        'BLACKOUTS': BLACKOUTS,
        'DAILY_BANK': DAILY_BANK,
        'WEEKLY_BANK': WEEKLY_BANK,
        'CAPS': CAPS
    }

    with open(filename, 'wb') as handle:
        pickle.dump(state, handle)


def load(filename):
    with open(filename, 'rb') as handle:
        state = pickle.load(handle)
        CREDITS.clear()
        CREDITS.update(state['CREDITS'])
        BLACKOUTS.clear()
        BLACKOUTS.update(state['BLACKOUTS'])
        INTERVALS.clear()
        INTERVALS.update(state['INTERVALS'])
        ACTIVE.clear()
        DAILY_BANK.clear()
        DAILY_BANK.update(state['DAILY_BANK'])
        WEEKLY_BANK.clear()
        WEEKLY_BANK.update(state['WEEKLY_BANK'])
        CAPS.clear()
        CAPS.update(state['CAPS'])

        for u in CREDITS:
            ACTIVE[u] = -1


if __name__ == '__main__':

    # testing time shift
    now = datetime.utcnow()

    pacific_time_offset = get_time_offset(now)

    now_minute = to_minutes(now.weekday() % 7, now.hour, now.minute)

    print ("UTC", now)
    print ("raw", now_minute)
    print ("offset", pacific_time_offset)
    now_minute += pacific_time_offset
    now_minute %= WEEK
    print ("pst", now_minute)

    now = datetime.now()
    confirm = to_minutes(now.weekday() % 7, now.hour, now.minute)
    print ("confirm", confirm)
    CAPS['nicky'] = 120
    CREDITS['nicky'] = 0
    ACTIVE['nicky'] = -1
    DAILY_BANK['nicky'] = 10
    WEEKLY_BANK['nicky'] = 5
    DAILY_BANK['helen'] = 7

    add_interval('nicky', (6, 23, 0), (0, 8, 0))
    add_interval('nicky', (0, 9, 30), (0, 13, 30))
    add_blackout('nicky', (0, 7, 0), (0, 9, 45))
    add_blackout('nicky', (0, 11, 0), (0, 12, 00))
    add_blackout('nicky', (0, 13, 15), (0, 20, 20))

    print (INTERVALS['nicky'])
    print (BLACKOUTS['nicky'])
    print (get_intervals('nicky'))
    print (get_ui_intervals('nicky'))
    # save("test_db")
