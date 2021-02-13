# thermopi v1.1
Smart thermostat with Raspberry Pi

I got annoyed with my ordinary thermostat because I wanted different temperature targets at different times of day.  After determining that replacing it with a relay module governed by a Raspberry Pi would be simple, I set about making my own smart thermostat.  The possibilities for new features are endless and I'm definitely open to suggestions.  Now my wall is ugly where my naked Raspberry Pi Zero W hangs idly by its power cord near the relay, supporting the thermometer's breadboard by jumper wire.  So the next big step will be to build some housing for it.  Other feature ideas are hidden throughout the code in comments.

## Physical configuration

- Use a single relay module connecting furnace heat relay in the N/O position.
  - Relay input signal wire is currently configured to GPIO18 on RPi.
  - https://www.amazon.com/HiLetgo-Channel-Module-Isolation-Support/dp/B00LW2H5GC/
  
- Use a DHT22 temperature/humidity sensor.
  - Signal wire currently configured to GPIO4 on RPi.
  - https://www.adafruit.com/product/385
  
- Diagram forthcoming

## Usage

With peripherals in place, modules acquired, and the namelist filled out, this should get things going:

```bash
sudo python3 thermo.py
```

You may wish to run this in the background or [on a separate screen](https://www.howtogeek.com/662422/how-to-use-linuxs-screen-command/).  You can periodically check the state.log for data and can plot from it.  (I'll add a plotting script at some point, too).
