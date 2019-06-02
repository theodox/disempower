# main.py -- put your code here!
import ssd1306
from machine import I2C, Pin
import rfid
import time
import network
import socket
import json
import urequests as requests

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

    failsafe = 512
    count = 0

    LOGGED_IN = None

    AVAIL, TOTAL = 0, 0

    GREEH = Pin("LED_GREEN")
    RED = Pin("LED_RED")

    while True and count < failsafe:
        count += 1

        GREEH.value(AVAIL == 0)
        RED.value(count % 2 == 0)

        try:
            result = READER.read_user_id(4)
        except RuntimeError:
            print ("CARD READ ERROR")
            result = None

        if result is None:
            if count % 8 == 0 and LOGGED_IN is not None:

                address = ('192.168.0.6', 8080)

                sock = socket.socket()
                sock.connect(address)

                req = 'GET /check/{} HTTP/1.1\r\nHost = "theodox.pythonanywhere.com"\r\n'.format(LOGGED_IN)

                sock.write(req.encode('utf-8'))
                response = sock.read()
                if response:
                    json_response = response.splitlines()[-1]
                    try:
                        blob = json.loads(json_response)
                    except:
                        blob = {}
                    AVAIL, TOTAL = blob.get(LOGGED_IN, (0, 0))

                    print ("available", AVAIL, "total", TOTAL)

            time.sleep(0.2)
            continue

        if LOGGED_IN == result:
            print (LOGGED_IN, "LOG OUT")
            LOGGED_IN = None
            AVAIL = 0
            TOTAL = 0

        else:
            print (LOGGED_IN, "LOG OUT")
            print (result, "LOG IN", len(result))
            LOGGED_IN = result
            AVAIL = 0
            TOTAL = 0

        time.sleep(4.0)

    print ("LOOP COMPLETE")


REQ = '''GET /check/nicky HTTP/1.1
Host: theodox.pythonanywhere.com
Content-Type: text/html
'''.encode('utf-8')

if __name__ == '__main__':

    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect('simonides', '300spartans!')

    r = requests.get("http://theodox.pythonanywhere.com/check/nicky")
    print(r.json())
    
    nic.disconnect()

"""

    time.sleep(4.0)

    try:
        main_loop()
    except Exception as e:
        logger.exception(e)
    finally:
        nic.disconnect()
"""
