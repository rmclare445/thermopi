import time
import RPi.GPIO     as GPIO
import Adafruit_DHT as ad
import thermo_query as tq
import write_log    as wl
#import email_notify as en
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

# Write header to log
wl.write_log(" T(F) | H(%) | Time     | S")

try:
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
                stat = tq.query( lt[3], lt[4], temp, GPIO.input(18) )
                
                # If status change is warranted, change status
                if stat is not None:
                    GPIO.output(18, stat)
                    log_stat = "T" if stat else "F"
            
            # Write state and times to log
            ## Need to add date to log
            wl.write_log(" %0.1f | %02d   | %02d:%02d:%02d | %s" \
                        % ( temp, hum, lt[3], lt[4], lt[5], log_stat ))
        
            # Add new temp, delete oldest even if perturbation magnitude is high
            temps = update( temp, temps )
            
        time.sleep(1/freq)
        
finally:
    GPIO.output(18, False)
    GPIO.cleanup( )
    wl.write_log("thermopi terminated")
    # try:
        # en.sendmail( time.asctime( ) )
    # except:
        # raise RuntimeWarning("Unable to send email.")
