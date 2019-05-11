from org.transcrypt.stubs.browser import document, console

STATUS = {}


def set_status(blob):
    global STATUS
    STATUS = blob


def get_status():
    global STATUS
    return STATUS


def draw_calendar():

    print ("draw_calendar", get_status())

    canvas = document.getElementById("fred")

    w = canvas.scrollWidth
    h = canvas.scrollHeight

    ctx = canvas.getContext('2d')

    # rect is a 4-tuple of 0-1 coords
    def draw_rect(rect, fillStyle):
        left = rect[0] * w
        right = rect[2] * w
        top = rect[1] * h
        bottom = rect[3] * h
        ctx.fillStyle = fillStyle
        ctx.fillRect(left, top, right - left, bottom - top)

    BG = '#f9fae3'
    COLS = '#e5faf5'
    BLANK = '#ffffff'

    draw_rect((0, 0, 1, 1), BG)
    for i in range(7):
        if i % 2 == 0:
            lf = i / 7
            r = (i + 1) / 7
            draw_rect((lf, 0, r, 1), COLS)

    ctx.strokeStyle = BLANK
    for i in range(1, 25):
        divider = (i / 25) * h
        ctx.beginPath()
        ctx.moveTo(0, divider)
        ctx.lineTo(w, divider)
        ctx.moveTo(w, divider + 1)
        ctx.lineTo(0, divider + 1)
        ctx.stroke()

    ctx.font = "18px Sanserif"
    ctx.fillStyle = '#111111'

    for i, t in enumerate(('Mon', 'Tues', 'Weds',
                           'Thurs', 'Fri', 'Sat', 'Sun')):
        lf = (i / 7) * w
        size = ctx.measureText(t).width
        ctx.fillText(t, lf + (size / 2), 19, w / 7)


def resize_handler():
    frame = document.getElementById('frame')
    canvas = document.getElementById('fred')
    w = frame.scrollWidth
    # have to remember to account for
    # the padding, otherwise race condition
    # makes the canvas grow...
    canvas.width = (w - 32)
    canvas.height = (25 * 20)
    draw_calendar()
    print("resized")


if __name__ == '__main__':
    resize_handler()
    window.onresize = resize_handler
