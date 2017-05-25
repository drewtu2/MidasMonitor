
source minerConfig

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
