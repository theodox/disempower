from bottle import Bottle, request, template, TEMPLATE_PATH, abort, response, redirect, static_file
import disempower.interval as interval
import disempower.auth as auth
import json
import ast
import os

import logging
logger = logging.getLogger("disempower")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


disempower_dir = os.path.dirname(__file__)
views_dir = os.path.join(disempower_dir, 'views')
static_dir = os.path.join(disempower_dir, 'static')
js_dir = os.path.join(disempower_dir, '__target__')
save_file = os.path.abspath(os.path.join(disempower_dir, '..', 'disempowerdb'))

app = Bottle()
TEMPLATE_PATH.insert(0, views_dir)


SESSION_TIMEOUT = 300


def authorized():
    if not auth.in_session(request):
        return abort(401, "You must be logged in to view this page.")
    else:
        return None
    # use 'returm authorized() or xxxx'


@app.get("/static/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root=static_dir)


@app.get("/static/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root=js_dir)


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
    interval.save(save_file)
    redirect("/")

# add a user -----------------


@app.route("/newuser")
def new_user():
    return authorized() or template("newuser.tpl", users=interval.get_users())


@app.route('/adduser', method="POST")
def add_user():
    not_auth = authorized()
    if not_auth:
        return not_auth

    new_user_name = request.forms.get('username')
    if new_user_name not in interval.get_users():
        for d in range(7):
            interval.add_interval(new_user_name, (d, 8, 0), (d, 21, 0))
        interval.add_credit(new_user_name, 60)
        interval.set_weekly_allowance(new_user_name, 0)
        interval.set_daily_allowance(new_user_name, 60)
        interval.save(save_file)
    return redirect('/user/' + new_user_name)


@app.route('/clear_intervals/<user>', method="POST")
def clear_interval(user):
    result = authorized()
    if result:
        return result
    interval.clear_intervals(user)
    return redirect("/user/" + user)


@app.route('/clear_blackouts/<user>', method="POST")
def clear_blackouts(user):
    result = authorized()
    if result:
        return result
    interval.clear_blackouts(user)
    return redirect("/user/" + user)


@app.route("/interval/<user>", method="POST")
def add_interval(user):
    result = authorized()
    if result:
        return result

    action = request.forms.get('action_type')

    days = ast.literal_eval(request.forms.get('days'))
    start_time = request.forms.get('start_time')
    end_time = request.forms.get('end_time')
    start_time = [int(k) for k in start_time.split(":")]
    end_time = [int(k) for k in end_time.split(":")]

    for start_day in days:

        start_tuple = start_day, start_time[0], start_time[1]
        end_tuple = start_day, end_time[0], end_time[1]

        if action == 'add':
            interval.add_interval(user, start_tuple, end_tuple)
        elif action == 'block':
            interval.add_blackout(user, start_tuple, end_tuple)

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


@app.route('/credit/<user>', method="POST")
def set_credit(user):

    amount = int(request.forms.get('credits', 0))
    result = authorized()
    if result:
        return result

    interval.set_credit(user, amount)
    interval.save(save_file)
    return redirect('/user/' + user)


@app.route('/cap/<user>', method="POST")
def set_credit(user):

    amount = int(request.forms.get('cap', 60))
    result = authorized()
    if result:
        return result

    interval.set_cap(user, amount)
    interval.save(save_file)
    return redirect('/user/' + user)


@app.route("/daily/<user>", method="POST")
def set_daily(user):
    result = authorized()
    if result:
        return result

    amount = int(request.forms.get('daily_cred', '0'))

    interval.set_daily_allowance(user, amount)
    interval.save(save_file)
    return redirect('/user/' + user)


@app.route("/weekly/<user>", method='POST')
def set_weekly(user):
    result = authorized()
    if result:
        return result

    amount = int(request.forms.get('weekly_cred', '0'))

    interval.set_weekly_allowance(user, amount)
    interval.save(save_file)
    return redirect('/user/' + user)


@app.route("/delete/<user>")
def delete_user(user):
    result = authorized()
    if result:
        return result

    interval.delete_user(user)
    return redirect("/")


@app.route("/status")
def status():
    context = {}
    for user in interval.get_users():
        intervals = interval.get_ui_intervals(user)
        context[user] = {
            'intervals': intervals,
            'user': user,
            'blackouts': []
        }

    return template('status.tpl',
                    context=json.dumps(context),
                    users=interval.get_users())


@app.route("/user/<user>")
def user_page(user):
    daily = interval.get_daily_allowance(user,)
    weekly = interval.get_weekly_allowance(user)
    credits = interval.get_credits(user)
    cap = interval.get_cap(user)
    intervals = interval.get_ui_intervals(user)
    blackouts = interval.get_ui_blackouts(user)
    context = {user: {
        'intervals': intervals,
        'user': user,
        'blackouts': blackouts}
    }

    return template('user.tpl', context=json.dumps(context),
                    username=user,
                    credits=credits,
                    intervals=intervals,
                    daily=daily,
                    weekly=weekly,
                    cap=cap,
                    users=interval.get_users())


@app.route('/check/<user>')
def check(user):

    users = interval.get_users()

    if user in users:
        return {'remaining': interval.check(user), 'total': interval.get_credits(user)}
    else:
        return {'remaining': -1, 'total': -1}


# load the database when imported
try:
    interval.load(save_file)
except IOError:
    print ("no save file")
