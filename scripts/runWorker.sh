###############################################################################
# Andrew tu
# This script is intended to be run as a chron job every "N" minutes. 
# This script is responsible for setting up and running worker.py to 
# send a heartbeat to the Heroku server responsible for monitoring the 
# ethereum miner...
###############################################################################


# Set up Variables

# Location on Midas
export MIDAS_HOME="~/Documents/MidasMonitor/"

# Location on Andrew MBPR
#export MIDAS_HOME="/Users/Andrew/Dropbox/Northeastern/Projects/MidasMonitor/"

echo MIDAS_HOME = $MIDAS_HOME

source $MIDAS_HOME/setup
source $MIDAS_HOME/venv/bin/activate

#python $MIDAS_HOME/lib/worker.py

echo Last run: $(date) >> $MIDAS_HOME/worker.log
