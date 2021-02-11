import time
import RPi.GPIO as GPIO
import Adafruit_DHT as ad
import thermo_query as tq

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)

DHT_SENSOR = ad.DHT22
DHT_PIN = 4

try:
    while True:

        # There's an issue where every now and again, the sensor returns
        # a very low number for a short time

        # Thermometer adjusts slowly and fluctuates slightly.  Beware
        # fluctuations near thresholds (need tolerances).
        hum, temp = ad.read_retry(DHT_SENSOR, DHT_PIN)
        temp      = temp * (9/5.) + 32.
        print(temp)
        
        # There should be some tolerance so that it's not too delicate
        # and constantly switching back and forth
        stat = tq.query(time.localtime()[3], time.localtime()[4], temp)

        if stat:
            if not GPIO.input(18):
                GPIO.output(18, True)
        else:
            if GPIO.input(18):
                GPIO.output(18, False)

        time.sleep(2)
finally:
    GPIO.output(18, False)
    GPIO.cleanup()

