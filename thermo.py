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

with open("state.log", "a") as f:
    f.write(" T(F)| H(%)  \n")
    f.close()

try:
    while True:

        # There's an issue where every now and again, the sensor returns
        # a very low number for a short time
        
        hum, temp = ad.read_retry(DHT_SENSOR, DHT_PIN)
        temp      = temp * (9/5.) + 32.
        
        stat = tq.query( time.localtime()[3], 
                         time.localtime()[4], 
                         temp, GPIO.input(18) )

        if stat == True:
            GPIO.output(18, True)
            print("TRUE")
        elif stat == False:
            GPIO.output(18, False)
            print("FALSE")
        print(stat)
        # Add times to log
        with open("state.log", "a") as f:
            f.write(" %0.1f   | %02d \n" % (temp, hum))
            f.close()

        time.sleep(5)
finally:
    GPIO.output(18, False)
    GPIO.cleanup()

