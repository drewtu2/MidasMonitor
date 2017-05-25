#!/bash/bin

export MIDAS_HOME=~/Documents/MidasMonitor/
source $MIDAS_HOME/setup
source $MIDAS_HOME/venv/bin/activate
python $MIDAS_HOME/lib/worker.py
