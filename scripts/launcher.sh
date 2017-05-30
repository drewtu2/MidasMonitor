#!/bin/bash

set -e

# Ensure this is being run as root
if [ "$EUID" -ne 0 ]
then echo "Please run as root"
  exit
fi

source minerConfig

###############################################################################
# Set Fan Speeds (First)
# If this command fails, the mining software will not run. 
# This is desireable because we do not want the mining software to run without 
# the fans having been started...
###############################################################################

./setFanSpeed.sh 200

###############################################################################
# Start miner depending on arguments
# Which mining pool we use will be dependant on the arguments we're passing in
# Can either be
# - Ethermine
# - Dwarfpool
###############################################################################

##################
# Constants
##################

# Wallet to mine to 
AT_JB_WALLET="3c76329390da17c727fa1bbbeb2fc45c80a7d92f"
WALLET=$AT_JB_WALLET

# Name of the worker
WORKER_NAME="Midas"
EMAIL="drewtu2@yahoo.com"

####################################
# Run on ethermine with ethminer
####################################
_ethminer_ethermine() {
  echo "Running Ethermine w/ Stratum" 
  ethminer --farm-recheck 200 -G -S eu1.ethermine.org:4444 -FS us1.ethermine.org:4444 -O $WALLET.$WORKER_NAME
};

####################################
# Run on dwarfppool with ethminer
####################################
_ethminer_dwarfpool() {
  echo "Running Dwarfpool"
  ethminer -G -F http://eth-us.dwarfpool.com:80/$AT_JB_WALLET/$EMAIL
};


####################################
# Based on arguments, determine what
# to run...
####################################
if [[ $# -eq 0 ]];
then
  _ethminer_ethermine
elif [ "$1" == "ethermine" ];
then
  _ethminer_ethermine
elif [ "$1" == "dwarfpool" ];
then
  _ethminer_dwarfpool
fi

