source minerConfig

###############################################################################
# Set Fan Speeds (First)
# If this command fails, the mining software will not run. 
# This is desireable because we do not want the mining software to run without 
# the fans having been started...
###############################################################################

# << FAN CODE HERE >> 

###############################################################################
# Start miner depending on arguments
# Which mining pool we use will be dependant on the arguments we're passing in
# Can either be
# - Ethermine
# - Dwarfpool
###############################################################################


if [[ $# -eq 0 ]];
then
  echo "Running Ethermine w/ Stratum" 
  ethminer --farm-recheck 200 -G -S eu1.ethermine.org:4444 -FS us1.ethermine.org:4444 -O 3c76329390da17c727fa1bbbeb2fc45c80a7d92f.Midas

elif [ "$1" == "ethermine" ];
then
  echo "Running Ethermine w/ Stratum" 
  ethminer --farm-recheck 200 -G -S eu1.ethermine.org:4444 -FS us1.ethermine.org:4444 -O 3c76329390da17c727fa1bbbeb2fc45c80a7d92f.Midas

elif [ "$1" == "dwarfpool" ];
then
  echo "Running Dwarfpool"    
  ethminer -G -F http://eth-us.dwarfpool.com:80/3c76329390da17c727fa1bbbeb2fc45c80a7d92f/drewtu2@yahoo.com

fi

