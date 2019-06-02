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
    sda = Pin.board.X10
    scl = Pin.board.X9
    bus = I2C(sda=sda, scl=scl)
    print ("Scan:", bus.scan())
    display = ssd1306.SSD1306_I2C(128, 32, bus)

    return display


def main_loop():
    print ("starting main loop")
    READER = rfid.PN532()

    READER.SAM_configuration()

    LOGGED_IN = None

    AVAIL, TOTAL = 0, 0

    GREEN = Pin("LED_GREEN")
    RED = Pin("LED_RED")
    BLUE = Pin("LED_BLUE")

    LOOP_TIME = 300
    CARD_TIME = 2000
    WEB_TIME = 5000

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

        GREEN.value(AVAIL == 0)
        BLUE.value(LOGGED_IN is None)
        BLINK = not BLINK
        RED.value(BLINK)
        print (AVAIL, TOTAL)

        if time.ticks_diff(NEXT_CARD, frame_time) < 0:

            try:
                result = READER.read_user_id(4)
                NEXT_CARD = time.ticks_add(frame_time, CARD_TIME)
            except RuntimeError as e:
                print ("CARD READ ERROR")
                print (e)
                result = None

            if result:

                if LOGGED_IN == result:
                    print (LOGGED_IN, "LOG OUT")
                    LOGGED_IN = None
                    AVAIL = 0
                    TOTAL = 0

                else:
                    if LOGGED_IN:
                        print (LOGGED_IN, "LOG OUT")
                    print (result, "LOG IN", len(result))
                    LOGGED_IN = result
                    AVAIL = 0
                    TOTAL = 0

        if time.ticks_diff(NEXT_WEB, frame_time) < 0:

            if LOGGED_IN is not None and len(LOGGED_IN):
                r, g, b = RED.value, GREEN.value, BLUE.value
                RED.value(1)
                GREEN.value(1)
                BLUE.value(1)

                req = 'http://theodox.pythonanywhere.com/check/{}'.format(LOGGED_IN)
                info = requests.get(req).json()
                print (">>>", info)
                AVAIL = info['available']
                TOTAL = info['total']
                NEXT_WEB = time.ticks_add(frame_time, WEB_TIME)

                RED.value(r)
                GREEN.value(g)
                BLUE.value(b)

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
