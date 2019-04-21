from bottle import route, run, Bottle
import interval
import re

app = Bottle()


def list_filter(config):
    ''' Matches a comma separated list of numbers. '''
    delimiter = config or ','
    regexp = r'\d+(%s\d)*' % re.escape(delimiter)

    def to_python(match):
        return map(int, match.split(delimiter))

    def to_url(numbers):
        return delimiter.join(map(str, numbers))

    return regexp, to_python, to_url


app.router.add_filter('list', list_filter)


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


interval.DAILY_BANK['nicky'] = 10
interval.add_interval('nicky', (6, 15, 0), (6, 23, 0))

app.run(host='localhost', port=8080)
