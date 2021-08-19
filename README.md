# thermopi v2.1
Smart thermostat with Raspberry Pi

I got annoyed with my ordinary thermostat because I wanted different temperature targets at different times of day.  After determining that replacing it with a relay module governed by a Raspberry Pi would be simple, I set about making my own smart thermostat.  The possibilities for new features are endless and I'm definitely open to suggestions.  Now my wall is ugly where my naked Raspberry Pi Zero W hangs idly by its power cord near the relay, supporting the thermometer's breadboard by jumper wire.  So the next big step will be to build some housing for it.  Other feature ideas are hidden throughout the code in comments.

## Physical configuration

- Use a single relay module connecting furnace signal wire in the N/O position.
  - Relay module input signal wire is currently configured to GPIO18 on RPi.
  - https://www.amazon.com/HiLetgo-Channel-Module-Isolation-Support/dp/B00LW2H5GC/
  
- Use a DHT22 temperature/humidity sensor.
  - Signal wire currently configured to GPIO4 on RPi.
  - https://www.adafruit.com/product/385
  
- Diagram forthcoming

## Preparation

```bash
sudo apt-get update
```

```bash
sudo apt-get upgrade
```

```bash
sudo pip3 install --upgrade setuptools
```

```bash
sudo pip3 install Adafruit_DHT
```

```bash
sudo pip3 install pyyaml
```

```bash
sudo apt-get install screen
```

```bash
sudo chmod 755 thermopi/thermo.sh
```

You may want to use crontab to run thermopi at boot in case of a loss of power.  Just add ```@reboot cd <working_directory>/thermopi; sudo ./thermo.sh``` to your crontab file as demonstrated at https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi

## Usage

To begin operation (if you haven't added the boot command to crontab):

```bash
cd thermopi
```

```bash
sudo ./thermo.sh
```

You can access information about the job and screen by using the following:

```bash
sudo screen -list
sudo screen -r
```

You can confirm that your thermostat is running by checking the state.log.  The most recent entries will reflect the time of the last scan.  If state.log does not exist, then the script has not been executed properly.

```bash
tail state.log
```
