import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata

ADAFRUIT_IO_USERNAME = "TobiasAndre"
ADAFRUIT_IO_KEY = "aio_ykvq11nMbubLzljmo8pvxtpauy4Z"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

digital_output = board.get_pin('d:7:o')
analog_input = board.get_pin('a:0:i')

try:
    digital = aio.feeds('digital')
    analog = aio.feeds('analog')
except RequestError:
    feed = Feed(name='digital')
    feed2 = Feed(name='analog')
    digital = aio.create_feed(feed)
    analog = aio.create_feed(feed2)

while True:
    data = aio.receive(digital.key)
    data2 = aio.send(analog.key, analog_input.read())

    if data.value == "ON":
        digital_output.write(True)
    else:
        digital_output.write(False)
    time.sleep(3)
