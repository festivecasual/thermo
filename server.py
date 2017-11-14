import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

from flask import Flask
app = Flask(__name__)

import subprocess

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

@app.route('/snapshot')
def snapshot():
	sensor = MAX31855.MAX31855(spi=SPI.SpiDev(0, 0))
	temp = sensor.readTempC()
	return '{:d}'.format(int(c_to_f(temp)))

@app.route('/shutdown')
def shutdown():
	subprocess.call(['sudo', 'poweroff'])
	return 'ok'

@app.after_request
def origin_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=6124, debug=True)

