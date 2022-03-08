# importing libraries
import time
from Adafruit_IO import Client, Feed, RequestError, ThrottlingError
import pyfirmata

# adafruit dashboard info
ADAFRUIT_IO_USERNAME = ''
ADAFRUIT_IO_KEY = ''

# set the variable aio to be the adafruit client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# setting the variable board to the com4 port with an arduino connected
board = pyfirmata.Arduino('COM4')

# starting board to be the communication board
pyfirmata.util.Iterator(board).start()

# make a digital_output variable for digital pin 7
# make an analog_input variable for analog pin 0
digital_output = board.get_pin('d:7:o')
analog_input = board.get_pin('a:0:i')

# make variables for adafruit feeds
# digital variable for digital feed
# analog variable for analog feed
digital = aio.feeds('digital')
analog = aio.feeds('analog')

# loop that reads the digital input from adafruit and writes it to the board
# and the analog input from Arduino get written to adafruit
# first try the loop except when ThrottlingError happens, if ThrottlingError happens print a message and wait for 61 seconds
while True:
    try:
        data = aio.receive(digital.key)
        data2 = aio.send(analog.key, analog_input.read())

        if data.value == "ON":
            digital_output.write(True)
        else:
            digital_output.write(False)
        time.sleep(3)
    
    except ThrottlingError:
        print("*Dead*")
        time.sleep(61)
