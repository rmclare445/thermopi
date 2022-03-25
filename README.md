# thermopi v3.0
Smart thermostat with Raspberry Pi

I got annoyed with my ordinary thermostat because I wanted different temperature targets at different times of day.  After determining that replacing it with a relay module governed by a Raspberry Pi would be simple, I set about making my own smart thermostat.  The possibilities for new features are endless and I'm definitely open to suggestions.  Now my wall is ugly where my naked Raspberry Pi Zero W hangs idly by its power cord near the relay, supporting the thermometer's breadboard by jumper wire.  So the next big step will be to build some housing for it.  Other feature ideas are hidden throughout the code in comments.

## Physical configuration

- Use as Raspberry Pi Zero W configured to your home WiFi network.
  - Enable SSH (then change user/password for security).

- Use a single relay module connecting furnace signal wire in the N/O position.
  - Relay module input signal wire is currently configured to GPIO18 on RPi.
  - https://www.amazon.com/HiLetgo-Channel-Module-Isolation-Support/dp/B00LW2H5GC/
  
- Use a DHT22 temperature/humidity sensor.
  - Signal wire currently configured to GPIO4 on RPi.
  - https://www.adafruit.com/product/385
  
- Diagram forthcoming

## Preparation

Make sure your system is up-to-date.

```bash
sudo apt-get update
sudo apt-get upgrade
sudo pip3 install --upgrade setuptools
```

Install necessary libraries.

```bash
sudo pip3 install Adafruit_DHT
sudo pip3 install pyyaml
```

Clone this repository.

```bash
sudo git clone https://github.com/rmclare445/thermopi.git
```

### Optional prep

Install screen so you can run it continuously in the background.

```bash
sudo apt-get install screen
```

Allow execution of thermo script (for running thermo.py on a detched screen).

```bash
sudo chmod +x thermopi/thermo.sh
```

You may want to use crontab to run thermopi at boot in case of a loss of power.  Just add ```@reboot cd <working_directory>/thermopi; sudo ./thermo.sh``` to your crontab file as demonstrated at https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi

## Usage

To begin operation (if you haven't added the boot command to crontab):

```bash
cd thermopi
sudo ./thermo.sh
```

You can manually operate the thermostat by calling the Python script directly:

```bash
sudo python3 thermo.py
```

You can access information about the job and screen by using the following:

```bash
sudo screen -list
sudo screen -r
```

You can confirm that your thermostat is running by checking the state log.  The most recent entries will reflect the time and state of the last cycle.  If it does not exist, then the script has not been executed properly.

```bash
tail logs/log.state
```

## Configuring Operation

All options for operation of the furnace can be configured by altering the ```thermopi/namelist.yaml``` file.  The namelist is read in every cycle and can be adjusted during operation.  The first three options within the namelist are the phase configuration options.  There should be an equal number of each (up to 1440) which determines the total number of phases.

- ```phase_hr```: Specifies the starting hour of a new phase (must use 24-hour format).
- ```phase_min```: Specifies the starting minute of respective phase.
- ```phase_T```: Specifies the target temperature of respective phase.

The next two options are the tolerances.  Generally you want to undershoot your target temperature before running the furnace and/or overshoot it before shutoff.  This prevents the furnace from switching on and off too often.

- ```up_tol```: The amount above the target temperature to shutoff the furnace.
- ```dn_tol```: The amount below the target temperature to trigger the furnace.

```freq``` is the frequency in Hz of sampling.  For example, a freq of 0.1 samples every 10 seconds.

### Locator configuration

Before enabling the locator, you must first specify your Life360 username, password, and the (lat,lon) of your house (in decimal degrees) in the file ```thermopi/info/keys.py```.  A template is provided in ```therompi/info/example_keys.py```.  Here is arecommended course of aciton:

```bash
cd thermopi/info
sudo cp example_keys.py keys.py
```

Use an editor to configure the variables in ```keys.py```.

Now, back in ```thermopi/namelist.yaml```, we can configure out locator settings.

- ```locator```: Set to True for on and False for off.
- ```radius```: The radial distance (in km) from your house within which normal operation will take place.
-  ```away_T```: The minimum target temperature for when you are outside of the radius.
