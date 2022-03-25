import sys
import time
import RPi.GPIO     as GPIO
import Adafruit_DHT as ad
import thermo_query as tq
import write_log    as wl
from   tools        import *
from   read_nl      import read_nl

# Set up GPIO board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up relay signal
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)
log_stat = "F"

# Empty list for averaging temperatures
temps = [0] * 4

try:
    # Redirect system output to logs
    sys.stdout = open('logs/log.stdout', 'w')
    sys.stderr = open('logs/log.stderr', 'w')
    while True:

        # Retrieve humidity, temperature, and local time
        hum, temp = ad.read_retry(ad.DHT22, 4)
        temp = C_to_F( temp )
        lt = time.localtime( )

        # Check namelist for frequency
        freq = read_nl( )['freq']

        # Discard data with unreasonably high humidity (indicator of bad data)
        if hum <= 104.:
            # Ensure perturbation magnitude is reasonable (don't react to bad data)
            if pert( temp, temps ) < 1.5:  ## and toggle: # for switch button

                # Check whether conditions warrant a change in relay status
                stat = tq.query( lt, temp, GPIO.input(18) )

                # If status change is warranted, change status
                if stat is not None:
                    GPIO.output(18, stat)
                    log_stat = "T" if stat else "F"
                    wl.write_ops( lt, stat, temp )

            # Write state and times to log
            wl.write_state( temp, hum, log_stat, lt )

            # Add new temp, delete oldest even if perturbation magnitude is high
            temps = update( temp, temps )

        time.sleep(1/freq)

finally:
    # Clear GPIO config
    GPIO.output(18, False)
    GPIO.cleanup( )
    # Close and redirect output
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    sys.stderr.close()
    sys.stderr = sys.__stderr__
    wl.write_ops(lt, bulletin="thermopi terminated")
