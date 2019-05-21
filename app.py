from bottle import route, run, Bottle, request, template, TEMPLATE_PATH, abort, response, redirect, static_file
import interval
import re
import auth
import json
import ast

#------------------

app = Bottle()
# TEMPLATE_PATH.insert(0, 'html')


SESSION_TIMEOUT = 300


def authorized():
    if not auth.in_session(request):
        return abort(401, "You must be logged in to view this page.")
    else:
        return None
    # use 'returm authorized() or xxxx'


@app.get("/static/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static")


@app.get("/static/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="__target__")


'''
# this is for static files, like CSS
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='__target__')'''

# landing page is login if we're not logged in,
# otherwise status


@app.get("/")
def landing():
    if auth.in_session(request):
        return redirect('/status')
    else:
        return template('frontpage.tpl', users=interval.get_users())

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


@app.route('/credit/<user>', method="POST")
def add_credit(user):

    amount = int(request.forms.get('credits', 0))
    result = authorized()
    if result:
        return result

    interval.add_credit(user, amount)
    return redirect('/user/' + user)


@app.route("/interval/<user>", method="POST")
def add_interval(user):
    result = authorized()
    if result:
        return result

    action = request.forms.get('action')

    days = ast.literal_eval(request.forms.get('days'))
    start_time = request.forms.get('start_time')
    end_time = request.forms.get('end_time')
    start_time = [int(k) for k in start_time.split(":")]
    end_time = [int(k) for k in end_time.split(":")]

    print ("days", days, 'action', action)
    for start_day in days:

        if action == 'add':
            interval.add_interval(
                user,
                (start_day, start_time[0], start_time[1]),
                (start_day, end_time[0], end_time[1])
            )
        elif action == 'block':
            interval.add_blackout(
                user,
                (start_day, start_time[0], start_time[1]),
                (start_day, end_time[0], end_time[1])
            )
        elif action == 'clear':
            interval.clear_intervals(user)
            break
        elif action == 'unblock':
            interval.clear_blackouts(user)
            break

    return redirect("/user/" + user)


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
        intervals = interval.get_ui_intervals(user)
        context[user] = {'available': available,
                         'daily': daily,
                         'weekly': weekly,
                         'credits': credits,
                         'cap': cap,
                         'intervals': intervals,
                         'user': user,
                         'blackouts': []
                         }

    return template('status.tpl', context=json.dumps(context), users=interval.get_users())


@app.route("/user/<user>")
def user_page(user):
    available = interval.check(user)
    daily = interval.get_daily_allowance(user)
    weekly = interval.get_weekly_allowance(user)
    credits = interval.get_credits(user)
    cap = interval.get_cap(user)
    intervals = interval.get_ui_intervals(user)
    blackouts = interval.get_ui_blackouts(user)
    context = {user:
               {'available': available,
                'daily': daily,
                'weekly': weekly,
                'credits': credits,
                'cap': cap,
                'intervals': intervals,
                'user': user,
                'blackouts': blackouts
                }
               }

    return template('user.tpl', context=json.dumps(context),
                    username=user,
                    credits=credits, intervals=intervals,
                    users=interval.get_users())



