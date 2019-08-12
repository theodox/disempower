# disempower
a micropython web app for controlling a power switch

The system has two parts -- a web app that handles admin tasks and a micropython client which handles connections to the server.  The client uses an Adafruit PN532 RFID reader to read user ID's from cards and then then connects to the server to see if a particular account has available time,  If there is time, a GPIO pin activates an (external) opto-electric switch, controlling access to a TV or other electronic device.

My working implementation uses a Pyboard Model D.
