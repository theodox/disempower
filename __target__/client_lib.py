from org.transcrypt.stubs.browser import document, console, hsl

STATUS = {}


def set_status(blob):
    global STATUS
    STATUS = blob


def get_status():
    global STATUS
    return STATUS


DAY_HRS = tuple(range(8, 22))
DAY_E = "hsl(46, 18%, 96%)"
DAY_O = "hsl(151, 20%, 92%)"
NIGHT_E = "hsl(46, 20%, 87%)"
NIGHT_O = "hsl(151, 30%, 85%)"
DIVIDER = "hsl(180, 0%, 100%, 0.33)"
BACKGROUND = "#FFFFFF"
MARGIN = 30
HOUR_OFFSET = 4

HR_FONT = "12px Arial"
HR_LABEL = "hsl(180,0%,45%)"

DAY_FONT = "18px Arial Black"
DAY_LABEL = "hsl(180,0%,10%)"

USER_COLORS = (
    'hsl(0,50%,50%, 0.25',
    'hsl(90,50%,50%, 0.25',
    'hsl(180,50%,50%, 0.25',
    'hsl(270,50%,50%, 0.25'
)

NOW_COLOR = 'hsl(0, 50%, 60%, 0.75)'


def hour_color(hour, day):
    evenodd = (day % 2) == 0
    if hour in DAY_HRS:
        if evenodd:
            return DAY_E
        else:
            return DAY_O
    else:
        if evenodd:
            return NIGHT_E
        else:
            return NIGHT_O


def draw_calendar():

    canvas = document.getElementById("calendar_canvas")

    w = canvas.scrollWidth
    h = canvas.scrollHeight

    ctx = canvas.getContext('2d')

    # rect is a 4-tuple of 0-1 coords

    def draw_rect(rect, fillStyle):
        left = rect[0] * (w - 2 * MARGIN) + MARGIN
        right = rect[2] * (w - 2 * MARGIN) + MARGIN
        top = rect[1] * h
        bottom = rect[3] * h
        ctx.fillStyle = fillStyle
        ctx.fillRect(left, top, right - left, bottom - top)

    draw_rect((0, 0, 1, 1), BACKGROUND)

    # basic colors
    for day in range(7):
        lf = day / 7
        r = (day + 1) / 7
        for hour in range(1, 25):
            top = hour / 25
            bottom = (hour + 1) / 25
            draw_rect((lf, top, r, bottom), hour_color(hour, day))

    # hour labels
    ctx.font = HR_FONT
    ctx.fillStyle = HR_LABEL
    for i in range(1, 24):

        if i % 2 == 0:
            divider = ((i + 1) / 25) * h + HOUR_OFFSET
            hr = (i % 12) or "Noon"

            if i % 12 < 10 and hr != "Noon":
                hr = str(" {}").format(hr)
            if i > 12:
                hr += " p"
            elif i < 12:
                hr += " a"

            ctx.fillText(hr, 2, divider)

    # day labels
    if w < 512:
        names = 'M', 'T', 'W', 'Th', 'F', 'Sa', 'Su'
    else:
        names = 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'

    ctx.font = DAY_FONT
    ctx.fillStyle = DAY_LABEL

    for i, t in enumerate(names):
        lf = int(((i + .5) / 7) * (w - 2 * MARGIN) + MARGIN)
        size = int(ctx.measureText(t).width / 2)
        ctx.fillText(t, lf - size, 18, int(w / 7))

    status = dict(get_status())

    user_count = len(status.keys())

    for idx, user in enumerate(status.keys()):
        intervals = status[user]['intervals']

        for i in intervals:
            day1, hr1, min1 = i[0]
            day2, hr2, min2 = i[1]

            offset = idx / user_count
            left = (day1 + offset) / 7
            right = (day2 + offset + (1 / user_count)) / 7
            top = (1 + hr1 + min1 / 60) / 25
            bottom = (1 + hr2 + min2 / 60) / 25
            draw_rect((left, top, right, bottom), USER_COLORS[idx % 4])

    # grid lines
    ctx.strokeStyle = DIVIDER
    for i in range(1, 25):
        divider = (i / 25) * h
        ctx.beginPath()
        ctx.moveTo(0, divider)
        ctx.lineTo(w, divider)
        ctx.moveTo(w, divider + 1)
        ctx.lineTo(0, divider + 1)
        ctx.stroke()

    now = __new__(Date())
    hour = now.getHours() + (now.getMinutes() / 60)

    divider = ((hour + 1) / 25)

    draw_rect((0, divider - 0.005, 1, divider + 0.005), NOW_COLOR)


def resize_handler():
    frame = document.getElementById('frame')
    canvas = document.getElementById('calendar_canvas')
    w = frame.scrollWidth
    # have to remember to account for
    # the padding, otherwise race condition
    # makes the canvas grow...
    canvas.width = (w - 32)
    canvas.height = (25 * 20)
    draw_calendar()
    print("resized")


def show_times():
    names = document.getElementById('names')
    while names.firstChild:
        names.removeChild(names.firstChild)

    status = get_status()
    for idx, u in enumerate(status.keys()):

        sp = document.createElement('BUTTON')
        sp.innerHTML = u + ":" + status[u]['credits']
        sp.style.backgroundColor = USER_COLORS[idx]
        sp.style.border = 'None'
        sp.style.color = 'White'
        sp.style.textAlign = 'left'
        sp.style.margin = '0px 8px'
        sp.style.font = "14px Arial"
        sp.style.width = '24%'
        names.appendChild(sp)


if __name__ == '__main__':
    resize_handler()
    window.onresize = resize_handler
    show_times()
    print ("LOADED")
