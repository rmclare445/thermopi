import time
import RPi.GPIO     as GPIO
import Adafruit_DHT as ad
import thermo_query as tq
import write_log    as wl

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)

DHT_SENSOR = ad.DHT22
DHT_PIN = 4

hum, temp = ad.read_retry(DHT_SENSOR, DHT_PIN)
temps = [temp, temp, temp]
    
wl.write_log(" T(F) | H(%) |")

try:
    while True:

        # There's an issue where every now and again, the sensor returns
        # a very low number for a short time
        
        # Retrieve humidity, temperature, and local time
        hum, temp = ad.read_retry(DHT_SENSOR, DHT_PIN)
        temp = temp * (9/5.) + 32.
        ti = time.localtime()
        print(temp, temps)
        if abs(temp - (sum(temps)/len(temps))) < 3.:
            stat = tq.query( ti[3], ti[4], temp, 
                             GPIO.input(18) )
            print(stat)
            if stat == True:
                GPIO.output(18, True)
            elif stat == False:
                GPIO.output(18, False)
        
        wl.write_log(" %0.1f | %02d   | %02d%02d%02d" \
                    % (temp, hum, ti[3], ti[4], ti[5]))
        
        temps.append( temp )
        temps = temps[1:]
        time.sleep(5)
finally:
    GPIO.output(18, False)
    GPIO.cleanup()

