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

# Set initial memberdist value just in case
memberdist = 0

try:
    # Redirect system output to logs
    sys.stdout = open('logs/log.stdout', 'w')
    sys.stderr = open('logs/log.stderr', 'w')
    while True:

        try:
            # Read settings from namelist
            nml_opts = read_nl( )
        
            # Retrieve humidity, temperature, and local time
            hum, temp = ad.read_retry(ad.DHT22, 4)
            temp = C_to_F( temp )
            lt = time.localtime( )

            # Discard data with unreasonably high humidity (indicator of bad data)
            if hum <= 104.:
                # Ensure perturbation magnitude is reasonable (don't react to bad data)
                if pert( temp, temps ) < 1.5:  ## and toggle: # for switch button
                
                    # Get minimum member distance from file
                    if nml_opts['locator']:
                        try:
                            with open("member_distance", "r") as f:
                                memberdist = float( f.read() )
                        except:
                            print( "%02d%02d%02d_%02d:%02d:%02d - Unable to read member_distance!" %
                                    (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5]) )

                    # Check whether conditions warrant a change in relay status
                    stat = tq.query( lt, temp, GPIO.input(18), memberdist, nml_opts )

                    # If status change is warranted, change status
                    if stat is not None:
                        GPIO.output(18, stat)
                        log_stat = "T" if stat else "F"
                        wl.write_ops( lt, stat, temp )

                # Write state and times to log
                wl.write_state( temp, hum, log_stat, lt )

                # Add new temp, delete oldest even if perturbation magnitude is high
                temps = update( temp, temps )

            time.sleep(1/nml_opts['freq'])

        except Exception as e: print(e)
            
finally:
    # Clear GPIO config
    GPIO.output(18, False)
    GPIO.cleanup( )
    # Close and redirect output
    wl.write_ops(lt, bulletin="thermopi terminated")
    sys.stdout.close()
    #sys.stdout = sys.__stdout__
    sys.stderr.close()
    #sys.stderr = sys.__stderr__
