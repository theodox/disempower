from org.transcrypt.stubs.browser import document, console


def draw_calendar(arg):
    canvas = document.getElementById("fred")

    def c_listener():
        canvas.style.width = '100%'
        canvas.style.height = '100%'
        ctx = canvas.getContext("2d")
        ctx.fillStye = '#ffffb3'
        ctx.fillRect(0, 0, 200, 200)
        ctx.fillStyle = "#99ff99"
        ctx.fillRect(50, 50, 100, 100)
    canvas.addEventListener('click', c_listener, False)


if __name__ == '__main__':
    console.log("woot")
    draw_calendar("hello world")
