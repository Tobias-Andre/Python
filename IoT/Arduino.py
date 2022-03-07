# importing libraries
import time
from Adafruit_IO import Client, Feed, RequestError, ThrottlingError
import pyfirmata

# adafruit dashboard info
ADAFRUIT_IO_USERNAME = "TobiasAndre"
ADAFRUIT_IO_KEY = "aio_ykvq11nMbubLzljmo8pvxtpauy4Z"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

pyfirmata.util.Iterator(board).start()

digital_output = board.get_pin('d:7:o')
analog_input = board.get_pin('a:0:i')

digital = aio.feeds('digital')
analog = aio.feeds('analog')

# loop that reads the digital input from adafruit and writes it to the board
# and the analog input from Arduino get written to adafruit
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
        print("your pore")
        time.sleep(65)
