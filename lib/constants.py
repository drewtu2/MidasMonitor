################################################################################
# Constants
################################################################################

# URLs
ETHERMINE_URL = "https://ethermine.org/api/miner_new/3c76329390da17c727fa1bbbeb2fc45c80a7d92f" 
HEROKU_URL = "https://midas-monitor.herokuapp.com"
HEROKU_HEARTBEAT = "/localDump"
# Timing
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60 
HOURS_PER_DAY = 24
TEN_MINUTES_SECONDS = 10 * SECONDS_PER_MINUTE
HEARTBEAT_TIMEOUT = 10 # MINUTES

# Other
MIN_HASHRATE = 30
DEBUG = 0

usage = ("status: displays a status message of the mining system. \n"
        "RESTART: restarts the machine\n"
        "help: displays help message")
################################################################################
# Import Modules
################################################################################
import monitor

################################################################################
# Utility Functions 
################################################################################
def genGpuList():
  count = 0
  gpuList = []
  for gpu in monitor.testData["amdgpu"]:
    gpuList.append(monitor.gpuInfo(gpu, count))
    count += 1
  return gpuList

def testSystemStatus():
  ps = monitor.PoolStatus()
  gpuList = monitor.monitor().amdGpus
  s = monitor.SystemStatus(ps, gpuList)

  s.printStatus()

def testPoolStatus():
  s = monitor.PoolStatus()
  assert s.getHashrate() == "44.1 MH/s", "Hashrate Failed"
  assert s.getAddress() == "3c76329390da17c727fa1bbbeb2fc45c80a7d92f", "Address Failed: " + s.getAddress()
  assert s.getEthPerMin() ==  0.0000303759502223839, "EthPerMin Faied"
  assert s.getUsdPerMin() == 0.00265303549242301, "UsdPerMin Failed"
