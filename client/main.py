# main.py -- put your code here!
import ssd1306
from machine import I2C, Pin
import rfid
import time
import network
import urequests as requests
import sys

"""import logging
logger = logging.getLogger('disempower')
logger.setLevel(logging.DEBUG)

logger.addHandler(logging.StreamHandler())
fileh = logging.FileHandler('disempower.log')
fileh.setLevel(logging.CRITICAL)
"""


def make_display():
    sda = Pin.board.Y10
    scl = Pin.board.Y9
    bus = I2C(sda=sda, scl=scl)
    print ("Scan:", bus.scan())
    display = ssd1306.SSD1306_I2C(128, 32, bus)

    return display


def main_loop():
    print ("starting main loop")

    DISPLAY = make_display()
    DISPLAY.poweron()
    DISPLAY.fill(1)
    DISPLAY.text("starting...", 8, 12, 0)
    DISPLAY.show()

    READER = rfid.PN532()

    READER.SAM_configuration()

    LOGGED_IN = None

    REMAIN, TOTAL = 0, 0

    GREEN = Pin("LED_GREEN")
    RED = Pin("LED_RED")
    BLUE = Pin("LED_BLUE")

    LOOP_TIME = 300
    CARD_TIME = 2000
    WEB_TIME = 12000

    now = time.ticks_ms()
    NEXT_TICK = now
    NEXT_CARD = now
    NEXT_WEB = now

    NEXT_CARD = NEXT_WEB = time.ticks_ms()

    BLINK = 1

    while True:

        frame_time = time.ticks_ms()

        if time.ticks_diff(frame_time, NEXT_TICK) < 0:
            continue

        NEXT_TICK = time.ticks_add(frame_time, LOOP_TIME)

        GREEN.value(REMAIN == 0)
        BLUE.value(LOGGED_IN is None)
        BLINK = not BLINK
        RED.value(BLINK)
#
        DISPLAY.fill(0)
        if LOGGED_IN:
            DISPLAY.text(str(LOGGED_IN), 8, 2)
            DISPLAY.text(str(REMAIN), 8, 12)
            DISPLAY.text(str(TOTAL), 8, 22)

            avail = min(REMAIN / 10, 1.0)
            h = int(32 * avail)
            top = 32 - h
            DISPLAY.fill_rect(100, top, 28, h, 1)

        else:
            DISPLAY.text("Logged out", 8, 12)

        DISPLAY.show()

        if time.ticks_diff(NEXT_CARD, frame_time) < 0:

            result = None
            try:
                result = READER.read_user_id(4)
                NEXT_CARD = time.ticks_add(frame_time, CARD_TIME)
            except RuntimeError as e:
                print ("CARD READ ERROR")
                print (e)
                result = None
                DISPLAY.fill(0)
                DISPLAY.text("Could not read card", 8, 12)
                DISPLAY.show()
                READER._wakeup()

            except OSError as e:
                print ("read timeout")
                DISPLAY.fill(0)
                DISPLAY.text("Card reader timeout", 8, 12)
                DISPLAY.show()
                READER._wakeup()


            if result:

                if LOGGED_IN == result:
                    print (LOGGED_IN, "LOG OUT")
                    LOGGED_IN = None
                    REMAIN = 0
                    TOTAL = 0

                else:
                    if LOGGED_IN:
                        print (LOGGED_IN, "LOG OUT")
                    print (result, "LOG IN", len(result))
                    LOGGED_IN = result
                    REMAIN = 0
                    TOTAL = 0
                    NEXT_WEB = frame_time

        if time.ticks_diff(NEXT_WEB, frame_time) < 0:

            if LOGGED_IN is not None and len(LOGGED_IN):

                print ("checking status")
                DISPLAY.fill(1)
                DISPLAY.text("checking", 8, 12, 0)
                DISPLAY.show()

                r, g, b = RED.value, GREEN.value, BLUE.value
                RED.value(1)
                GREEN.value(1)
                BLUE.value(1)

                req = 'http://theodox.pythonanywhere.com/check/{}'.format(LOGGED_IN)
                info = requests.get(req).json()
                REMAIN = info['remaining']
                TOTAL = info['total']
                NEXT_WEB = time.ticks_add(frame_time, WEB_TIME)

                RED.value(r)
                GREEN.value(g)
                BLUE.value(b)

                DISPLAY.fill(0)
                DISPLAY.show()

    print ("LOOP COMPLETE")


if __name__ == '__main__':

    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect('simonides', '300spartans!')

    print("waiitng for network")
    time.sleep(4.0)

    try:
        main_loop()
    except Exception as e:
        sys.print_exception(e)
        with open("crashlog.txt", 'wt') as crashlog:
            sys.print_exception(e, crashlog)
    finally:
        nic.disconnect()
