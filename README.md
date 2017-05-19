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

NOTE: GroupMe API requires the groupme API key to be set...

### Docs:
psutil: (http://pythonhosted.org/psutil/#sensors)



## TODO

## Vision
- Flask Server Running on hosted server as a service type thing (HerokU)
- Python script running on the local machine periodically making post requests
- Remote server accepts post requests from boththe main computer and also other students
- When remote server receives request from GroupMe 
-- Evaluates, If it is a status
  queue message from groupme, send the most up to date information. 
-- If it is from the local server, update local variables with the current local 
   state of the machine which will be sent back to users from any GroupMe interface

### Basic
~~- Get GPU temperatures from the system~~
~~-- Set up helper funcitons to get this information~~
~~- Log results in logfile~~
- Integrate dwarfpool's API to provide readouts with log file?
- Should be run as a chron job?

### System adjustment
~- Target GPU temperature 75 degrees C - regulate fan speeds to meet targets~
-- Just use `fancontrol` module?
  

### Groupme API Integration
~- Send alerts to phone if temperatures exceed 80 degrees C~
- Query ~~dwarfpool~~ ethermine API and post information to GroupMe Chat on request

### Bells and Whistles to the Max
- Submit querys from Alexa
- Graph temperature over time, correlate to hash rate over time

