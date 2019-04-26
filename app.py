from bottle import route, run, Bottle, request, template, TEMPLATE_PATH, abort, response, redirect, static_file
import interval
import re
import auth
import json


#------------------

app = Bottle()
#TEMPLATE_PATH.insert(0, 'html')


SESSION_TIMEOUT = 300


def authorized():
    if not auth.in_session(request):
        return abort(401, "You must be logged in to view this page.")
    else:
        return None
    # use 'returm authorized() or xxxx'


# this is for static files, like CSS
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

# landing page is login if we're not logged in,
# otherwise status


@app.get("/")
def landing():
    if auth.in_session(request):
        return redirect('/status')
    else:
        return template('frontpage.tpl')

# login dialog


@app.route("/login", method="POST")
def login_dialog():
    user = request.forms.get('username') or ""
    password = request.forms.get('password') or ""

    sesh, secret = auth.login(user, password)
    response.set_cookie('session', sesh, secret=secret,
                        max_age=SESSION_TIMEOUT)
    return redirect("/")


# log out and return to login screen
@app.route('/logout')
def logout():
    auth.logout(request)
    redirect("/")


@app.route('/credits')
def credits():
    return authorized() or template('credits.tpl')


@app.route('/check/<user>')
def check_user(user):
    return {
        'user': interval.check(user),
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route('/credit/<user>/<amount:int>')
def add_credit(user, amount):

    result = authorized()
    if result:
        return result

    interval.add_credit(user, amount)
    return {
        'user': user,
        'credits': interval.CREDITS.get(user, 0)
    }


@app.route("/interval/<user>/<numbers>")
def add_interval(user, numbers):
    result = authorized()
    if result:
        return result

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
    result = authorized()
    if result:
        return result

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
    result = authorized()
    if result:
        return result

    interval.set_daily_allowance(user, amount)
    return {
        'user': user,
        'daily': interval.get_daily_allowance(user)
    }


@app.route("/weekly/<user>/<amount:int>")
def set_weekly(user, amount):
    result = authorized()
    if result:
        return result

    interval.set_weekly_allowance(user, amount)
    return {
        'user': user,
        'weekly': interval.get_weekly_allowance(user)
    }


@app.route("/status")
def status():
    context = {}
    for user in interval.get_users():
        available = interval.check(user)
        daily = interval.get_daily_allowance(user)
        weekly = interval.get_weekly_allowance(user)
        credits = interval.get_credits(user)
        cap = interval.get_cap(user)
        intevals = interval.get_intervals(user)

        context[user] = {'available': available,
                         'daily': daily,
                         'weekly': weekly,
                         'credits': credits,
                         'cap': cap,
                         'intevals': intevals,
                         'user': user
                         }
    return template('status.tpl', context=json.dumps(context), M11='<button>Nicky</button>', included='<h1>Test</h1>' )


interval.DAILY_BANK['nicky'] = 10
interval.add_interval('nicky', (6, 15, 0), (6, 23, 0))
interval.WEEKLY_BANK['helen'] = 60
interval.add_interval('helen', (2,15,30), (2, 20,0))

app.run(host='localhost', port=8080)
