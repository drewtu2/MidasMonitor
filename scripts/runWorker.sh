
export MIDAS_HOME=~/Documents/MidasMonitor/
echo MIDAS_HOME = $MIDAS_HOME
source $MIDAS_HOME/setup

source $MIDAS_HOME/venv/bin/activate

python $MIDAS_HOME/lib/worker.py
