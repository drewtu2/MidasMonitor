# MidasMonitor

## Goal
The goal of this project is to produce a resource that can monitor an ethereum 
mining cluster, allowing the user to maintain connected and informed of the state
of his/her workers at all times.

## Setup

All python dependencies can be installed using pip.
```
  pip install -r requirements.txt
```

This project also requires the following libraries.
```
  lm-sensors
```

NOTE: GroupMe API requires the groupme API key to be set...

### Docs:
psutil: (http://pythonhosted.org/psutil/#sensors)



## TODO

## Vision
- Flask Server runs on Heroku coordinating the monitoring system
- Python script running on the local machine periodically making post requests
- Flask server accepts two types of post requests
  - Callback URL Post Requests from GroupMe 
    - If a status queue message received, send the status of miner and pool
    - RESTART message to restart the miner.
    - Help message to display command information. 
    - Ignores All other messages...
    - * More coming...*
  - Heartbeats from a worker 
    - Updates the locally stored information from of the worker status. To be used
      in next query.
    - Notes when the last heartbeat was received...

### Chron Jobs
The following scripts should be setup as a chron job...

- libs/worker.py: runs every 5 minutes on the worker node.
- scripts/launcher.sh: runs on startup on the worker node.

### System adjustment
- Target GPU temperature 75 degrees C - regulate fan speeds to meet targets

  

### Groupme API Integration
~- Send alerts to phone if temperatures exceed 75 degrees C~
~~- Query ~~dwarfpool~~ ethermine API and post information to GroupMe Chat on request~~


