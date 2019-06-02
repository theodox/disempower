# main.py -- put your code here!
import ssd1306
from machine import I2C, Pin
import rfid
import time
import network
import socket
import json


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

    while True and count < failsafe:
        count += 1
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

                req = "GET /check/{} HTTP/1.1\r\n\r\n".format(LOGGED_IN)

                sock.write(req.encode('utf-8'))
                response = sock.read()
                if response:
                    json_response = response.splitlines()[-1]
                    print (json.loads(json_response))

            time.sleep(0.2)
            continue

        if LOGGED_IN == result:
            print (LOGGED_IN, "LOG OUT")
            LOGGED_IN = None

        else:
            print (LOGGED_IN, "LOG OUT")
            print (result, "LOG IN", len(result))
            LOGGED_IN = result

        time.sleep(4.0)

    print ("LOOP COMPLETE")


if __name__ == '__main__':

    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect('simonides', '300spartans!')

    time.sleep(4.0)

    try:
        main_loop()
    finally:
        nic.disconnect()
