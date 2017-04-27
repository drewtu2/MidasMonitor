# MidasMonitor

## Goal
The goal of this project is to produce a resource that can monitor the GPU temperatures
and regulate fans to maintain a given target temperature. The intent is that it
will run alongside an ethminer script and providing useful information about the 
state of the machine. This informaiton may either be posted or queried.

Goals still in progress...

## Setup

```
  pip install -r requirements.txt
```

### Docs:
psutil: (http://pythonhosted.org/psutil/#sensors)



## TODO

### Basic
~~- Get GPU temperatures from the system~~
~~-- Set up helper funcitons to get this information~~
~~- Log results in logfile~~
- Integrate dwarfpool's API to provide readouts with log file?
- Should be run as a chron job?

### System adjustment
- Target GPU temperature 75 degrees C - regulate fan speeds to meet targets

### Groupme API Integration
- Send alerts to phone if temperatures exceed 80 degrees C
- Query dwarfpool API and post information to GroupMe Chat on request

### Bells and Whistles to the Max
- Submit querys from Alexa
- Graph temperature over time, correlate to hash rate over time

