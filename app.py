from bottle import route, run, Bottle, request, template, TEMPLATE_PATH, abort, response, redirect
import interval
import re
import auth


#------------------

app = Bottle()
TEMPLATE_PATH.insert(0, 'html')


SESSION_TIMEOUT = 300


@app.get("/")
def tester():
    return template('frontpage.tpl')


@app.route("/login")
@app.route("/login", method="POST")
def temp_login():
    user = request.forms.get('username') or ""
    password = request.forms.get('password') or ""
    
    sesh, secret = auth.login(user, password)
    response.set_cookie('session', sesh, secret=secret,
                        max_age=SESSION_TIMEOUT)
    return sesh


@app.route('/logout')
@app.route('/logout', method="POST")
def temp_logout():
    auth.logout(request)
    redirect("/")


@app.route('/credits')
def credits():
    if not auth.in_session(request):
        return not_authorized()

    return template('credits.tpl')


@app.route('/forbidden')
def not_authorized():
    abort(401, "You must be logged in to view this page.")


@app.route('/check/<user>')
def check_user(user):
    return {
        'user': interval.check(user),
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route('/credit/<user>/<amount:int>')
def add_credit(user, amount):
    if not auth.in_session(request):
        return not_authorized()

    interval.add_credit(user, amount)
    return {
        'user': user,
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route("/interval/<user>/<numbers>")
def add_interval(user, numbers):
    if not auth.in_session(request):
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
    if not auth.in_session(request):
        return not_authorized()

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
    if not auth.in_session(request):
        return not_authorized()

    interval.set_daily_allowance(user, amount)
    return {
        'user': user,
        'daily': interval.get_daily_allowance(user)
    }


@app.route("/weekly/<user>/<amount:int>")
def set_weekly(user, amount):
    if not auth.in_session(request):
        return not_authorized()

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
