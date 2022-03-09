# importing libraries
import time
from Adafruit_IO import Client, ThrottlingError
import pyfirmata

# adafruit dashboard info
ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ""

# set the variable aio to be the adafruit client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# setting the variable board to the com4 port with an arduino connected
board = pyfirmata.Arduino('COM5')

# starting board to be the communication board
pyfirmata.util.Iterator(board).start()

# make a digital_output1 variable for digital pin 2
# make a digital_output2 variable for digital pin 3
# make an analog_input variable for analog pin 0
digital_output1 = board.get_pin('d:2:o')
digital_output2 = board.get_pin('d:3:o')
analog_input = board.get_pin('a:0:i')

# make variables for adafruit feeds
# digital1 variable for digital1 feed
# digital2 variable for digital2 feed
# analog variable for analog feed
digital1 = aio.feeds('digital1')
digital2 = aio.feeds('digital2')
analog = aio.feeds('analog')

# loop that reads the digital input from adafruit and writes it to the board
# and the analog input from Arduino get written to adafruit
# first try the loop except when ThrottlingError happens, if ThrottlingError happens print a message and wait for 61 seconds
while True:
    try:
        data1 = aio.receive(digital1.key)
        data2 = aio.receive(digital2.key)
        boo = aio.send(analog.key, analog_input.read())

        if data1.value == "ON":
            digital_output1.write(True)
        else:
            digital_output1.write(False)
        if data2.value == "ON":
            digital_output2.write(True)
        else:
            digital_output2.write(False)
        time.sleep(3)
    
    except ThrottlingError:
        print("*Dead*")
        time.sleep(61)
