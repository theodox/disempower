# main.py -- put your code here!
import ssd1306
from machine import I2C, Pin
import rfid
import time
import network
import urequests as requests
import sys
import pyb
import gc
"""import logging
logger = logging.getLogger('disempower')
logger.setLevel(logging.DEBUG)

logger.addHandler(logging.StreamHandler())
fileh = logging.FileHandler('disempower.log')
fileh.setLevel(logging.CRITICAL)
"""
# soft reset breakout
ABORT = False
ABORT_SWITCH = pyb.Switch()
# pins

GREEN = Pin("LED_GREEN")
RED = Pin("LED_RED")
BLUE = Pin("LED_BLUE")

POWER = pyb.Pin('X1', Pin.OUT_PP)
DISPLAY = None


def set_led(r, g, b):
    RED.value(r),
    GREEN.value(g),
    BLUE.value(b)

def make_display():
    sda = Pin.board.Y10
    scl = Pin.board.Y9
    bus = I2C(sda=sda, scl=scl)
    print("Scan:", bus.scan())
    display = ssd1306.SSD1306_I2C(128, 32, bus)

    return display

def text_message(text, background = 0):
    DISPLAY.fill(background)
    DISPLAY.text(text, 8, 12, int(not background))
    DISPLAY.show()


def main_loop():
    global DISPLAY
    print("starting main loop")

   
    text_message("starting...", 1)

    try:
        READER = rfid.PN532()
        READER.SAM_configuration()
    except AssertionError:
        text_message("no card reader", 0)
        return


    LOGGED_IN = None
    REMAIN, TOTAL = 0, 0
    LOOP_TIME = 300
    CARD_TIME = 2000
    WEB_TIME = 12000

    now = time.ticks_ms()
    NEXT_TICK = now
    NEXT_CARD = now
    NEXT_WEB = now

    NEXT_CARD = NEXT_WEB = time.ticks_ms()

    BLINK = 1

    def display_finished():
        text_message("Out of time", 0)
        POWER.low()
        set_led(1,0,0)

    def display_logged_out():
        text_message("Logged Out", 0)
        set_led(0,0,0)

    def display_logged_in():
        DISPLAY.fill(0)
        DISPLAY.text(str(LOGGED_IN), 8, 2)
        DISPLAY.text(str(REMAIN), 8, 12)
        DISPLAY.text(str(TOTAL), 8, 22)
        avail = min(REMAIN / 10, 1.0)
        h = int(32 * avail)
        top = 32 - h
        DISPLAY.fill_rect(100, top, 28, h, 1)

    while not ABORT:

        frame_time = time.ticks_ms()

        if time.ticks_diff(frame_time, NEXT_TICK) < 0:
            continue

        NEXT_TICK = time.ticks_add(frame_time, LOOP_TIME)

        GREEN.value(REMAIN == 0)
        BLUE.value(LOGGED_IN is None)
        BLINK = not BLINK
        RED.value(BLINK)

        DISPLAY.fill(0)
        if LOGGED_IN:
            if REMAIN > 0.2:
                display_logged_in()
                POWER.high()
            else:
                display_finished()
                LOGGED_IN = None
                REMAIN = 0
                TOTAL = 0
                POWER.low()
        else:
            display_logged_out()
            POWER.low()

        DISPLAY.show()

        if time.ticks_diff(NEXT_CARD, frame_time) < 0:

            result = None
            try:
                result = READER.read_user_id(4)
                NEXT_CARD = time.ticks_add(frame_time, CARD_TIME)
            except RuntimeError as e:
                print("CARD READ ERROR")
                print(e)
                result = None
                text_message("Cannot read card", 0)
                READER._wakeup()
            except OSError:
                print("read timeout")
                text_message("Card read timeout", 0)
                READER._wakeup()

            if result:
                if LOGGED_IN == result:
                    print(LOGGED_IN, "LOG OUT")
                    LOGGED_IN = None
                    REMAIN = 0
                    TOTAL = 0

                else:
                    if LOGGED_IN:
                        print(LOGGED_IN, "LOG OUT")
                    print(result, "LOG IN", len(result))
                    LOGGED_IN = result
                    REMAIN = 0.25
                    TOTAL = 0
                    NEXT_WEB = frame_time

        if time.ticks_diff(NEXT_WEB, frame_time) < 0:

            if LOGGED_IN is not None and len(LOGGED_IN):

                req = 'http://theodox.pythonanywhere.com/check/{}'.format(LOGGED_IN)
                set_led(0,0,0)
                print("checking status")
                text_message("Checking...", 1)

                response = None
                try:

                    response = requests.get(req)
                    info = response.json()
                except OSError:
                    error = "request timeout"
                    
                    set_led(1,0,0)
                    print(error)

                    text_message("request timeout")
                    LOGGED_IN = None
                    REMAIN = 0
                    TOTAL = 0
                    time.sleep(1)
                else:
                    set_led(0,1,0)

                    REMAIN = info['remaining']
                    TOTAL = info['total']
                    NEXT_WEB = time.ticks_add(frame_time, WEB_TIME)

                    set_led(0,0,1)

                    DISPLAY.fill(0)
                    DISPLAY.show()


                finally:
                    del response

                    
        gc.collect()

    print("LOOP COMPLETE")


if __name__ == '__main__':
    set_led(0,1,1)
    status_display = None
    failsafe = 10
    counter = 0
    while not status_display and  counter <failsafe:
        try:
            status_display = make_display()
        except OSError:
            time.sleep(0.25)
            counter +=1

    if not status_display:
        print ("could not find display")

    DISPLAY = status_display
    set_led(0,0.5,0)

    print (status_display)
    status_display.poweron()
    

    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect('simonides', '300spartans!')

    text_message("wait for WLAN")

    set_led(0,0.5, 0.5)
    connected = False
    for n in range (400):
        connected = nic.isconnected()
        if connected:
            status = nic.ifconfig()
            text_message(status[0], 0)
            break

    set_led(0,1,0)

    time.sleep(2.0)

    def abort_handler():
        global ABORT
        RED.value(1)
        BLUE.value(0)
        GREEN.value(0)
        text_message("shut down")
        ABORT = True

    ABORT_SWITCH.callback(abort_handler)

    try:
        main_loop()
    except Exception as e:
        sys.print_exception(e)
        with open("crashlog.txt", 'wt') as crashlog:
            sys.print_exception(e, crashlog)
        text_message(str(e)[7:-1], 0)

    finally:
        nic.disconnect()
