import time
import RPi.GPIO     as GPIO
import Adafruit_DHT as ad
import thermo_query as tq
import write_log    as wl
from tools import *

# Set up GPIO board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up relay signal
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)

# Empty list for averaging temperatures
temps = [0] * 4

# Write header to log
wl.write_log(" T(F) | H(%) | Time")

try:
    while True:
        # Retrieve humidity, temperature, and local time
        hum, temp = ad.read_retry(ad.DHT22, 4)
        temp = C_to_F( temp )
        lt = time.localtime()
        
        if pert( temp, temps ) < 3.:
            stat = tq.query( lt[3], lt[4], temp, 
                             GPIO.input(18) )
            
            try:
                GPIO.output(18, stat)
        
        # Write state and times to log
        wl.write_log(" %0.1f | %02d   | %02d:%02d:%02d" \
                    % ( temp, hum, lt[3], lt[4], lt[5] ))
        
        # Add new temp, delete oldest
        temps = update( temp, temps )
        time.sleep(5)
finally:
    GPIO.output(18, False)
    GPIO.cleanup()

