# main.py -- put your code here!
import ssd1306
from machine import I2C, Pin

def make_display():
    sda = Pin.board.X10
    scl = Pin.board.X9
    bus = I2C (sda=sda, scl =scl)
    print ("Scan:", bus.scan())
    display = ssd1306.SSD1306_I2C(128,32, bus)

#    display.poweron()
#    display.text("hello world", 16,16, 1)

#    display.show()

    return display