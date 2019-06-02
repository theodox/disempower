5/5
===

* soldered display works now. The SSD1306_I2C class is the one to use.  Not clear what the refresh rate is. Working toy code:

    # main.py -- put your code here!
    import ssd1306
    from machine import I2C, Pin

    def make_display():
        sda = Pin.board.X10
        scl = Pin.board.X9
        bus = I2C (sda=sda, scl =scl)
        print ("Scan:", bus.scan())
        display = ssd1306.SSD1306_I2C(128,32, bus)
        return display

the library uses machine.I2C not pyb.I2C


* using pyb.i2c I can see the NFC reader after adding pull-up resistors (brown-black-orange-gold on the scl and sda lines)
* Still can't get reliable read-writes, i may have messed up while trying to accomodate the micropython syntax
* 
 
* PyD connects to wifi properly, but spams that annoying error message

* cleaning the soldering iron tip REALLY MATTERS.  Using the wire brush on the dremel seems to work very well

* hardware pull-up on SCL and SDA breaks the display module

* client:  use transcrypt to build, make sure to add the library to window with if__name__ = __main__

