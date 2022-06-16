# thermopi v3.1
Smart thermostat with Raspberry Pi

I like to sleep in the cold but I hate having to get out of bed to a cold house.  Because I couldn't very well change the temperature on my thermostat before waking up, I decided to automate the problem away.  Some investigation revealed that my central heating system is controlled by a single low voltage circuit which turns the furnace on while closed and off when open.  Essentially, the thermostat is just a relay connected to a dumb computer connected to a thermometer.  It made sense to create my own thermostat with a Raspberry Pi Zero W which could control the furnace according to my specific needs and would be connected to WiFi.

The project has been developed over the past year and many features have been added in that time.  The namelist configuration allows changes to be made without interrupting operation.  The locator makes use of a Life360 API to heat the home above a minimum temperature only while occupants are present or close by.  This saves a significant amount of energy which would otherwise be spent heating an empty house.  Another great advantage of this system is the ability to record in situ temperature and humidity continuously.  I plan to include a plotting library for analysis of log files.  Observing the heating profile of my house over the course of several days has brought a lot of insight into how home heating is affected by the diurnal cycle, the presence of warm bodies inside, and even cooking going on in the kitchen.  There are a number of takeaways to be had about efficiency by studying your home's weekly heating profile.

This has been a really fun and educational project and I'll keep working on it indefinitely.  It touches on so many different techniques and concepts but never felt exceptionally challenging (until I started trying to do the Google Sheets integration, yeesh).  I encourage any curious parties to try it out.  Take pictures of your current thermostat wiring, take it out, then follow the instructions below.  


## Physical configuration

- Raspberry Pi Zero W configured to home WiFi network.
  - Enable SSH (then change user/password for security).

- Single relay module connecting furnace signal wire in the N/O position.
  - Relay module input signal wire is currently configured to GPIO18 on RPi.
  - https://www.amazon.com/HiLetgo-Channel-Module-Isolation-Support/dp/B00LW2H5GC/
  
- DHT22 temperature/humidity sensor.
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

Allow execution of thermo script (for running thermo.py on a detached screen).

```bash
sudo chmod +x thermopi/thermo.sh
```

You may want to use crontab to run thermopi at boot in case of a loss of power.  Open the crontab file ```sudo crontab -e``` and add the following line:

```
@reboot cd ~/thermopi && sudo ./thermo.sh
```

## Usage

To begin operation (if you haven't added the boot command to crontab):

```bash
cd thermopi
sudo ./thermo.sh
```

Alternatively, you can manually operate the thermostat by calling the Python script directly:

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

- ```up_tol```: The amount above the target temperature to shut off the furnace.
- ```dn_tol```: The amount below the target temperature to trigger the furnace.

```freq``` is the frequency in Hz of sampling.  For example, a freq of 0.1 samples every 10 seconds.

### Locator configuration

Before enabling the locator, you must first specify your Life360 username, password, and the (lat,lon) of your house (in decimal degrees) in the file ```thermopi/info/keys.py```.  A template is provided in ```therompi/info/example_keys.py```.  Here is a recommended course of action:

```bash
cd thermopi/info
sudo cp example_keys.py keys.py
```

Use an editor to configure the variables in ```keys.py```.

You will also need to enable execution of ```location.py``` and schedule a cron job for it.

```bash
cd thermopi
sudo chmod +x location.py
```

Add some variant of the following line to your crontab (open with ```sudo crontab -e```).  This updates location every minute.

```
* * * * * cd ~/thermopi && sudo ./location.py
```

Now, back in ```thermopi/namelist.yaml```, we can configure the locator settings.

- ```locator```: Set to *True* for on and *False* for off.
- ```radius```: The radial distance (in km) from your house within which normal operation will take place.
-  ```away_T```: The minimum target temperature for when you are outside of the radius.
