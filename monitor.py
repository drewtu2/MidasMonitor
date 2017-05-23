import psutil
import groupy 
import requests
from samplePsutil import testData
from datetime import datetime
import json
import jsonpickle
import tests

HEROKU_URL = "https://midas-monitor.herokuapp.com"
ETHERMINE_URL = "https://ethermine.org/api/miner_new/3c76329390da17c727fa1bbbeb2fc45c80a7d92f"
DEBUG = 0

class monitor:

  def __init__(self):
    # TODO: Switch when running on Midas
    #sensorTempResponse = psutil.sensors_temperatures()
    #self.amdGpus = self.buildGpuList(sensorTempResponse)
    self.amdGpus = self.buildGpuList(testData)

    self.logfileName = "midas.log"
    self.maxTemp = 70
    self.botName = "Bot of Midas"
    try:
      self.bot = self.getBot() 
    except:
      print("Could not create bot")
      self.bot = None
  # Gets the gorupme bot associated with the groupme chat
  def getBot(self):
    bots = groupy.Bot.list()
    fbots = bots.filter(name = self.botName)
    return fbots.first
 
 # Takes a dictionary of shwtemp and returns a list of gpuInfos
  # Dict of shwtemps => List of GPUs
  def buildGpuList(self, sensorData):
    amdGpus = sensorData["amdgpu"]
    gpuList = []
    count = 0
    for gpu in amdGpus:
      gpuList.append(gpuInfo(gpu, count))
      count +=1
    return gpuList
  
  # Record temperatures into a log file
  def recordTemps(self):
    with open(self.logfileName, "a") as logfile:
      logfile.write(str(datetime.now()) + "\n")
      logfile.write("*" * 80)
      logfile.write("\n")
      for gpu in self.amdGpus:
        logfile.write(gpu.printGpu())
      logfile.write("*" * 80 + "\n")

  # Prints all the gpus in the gpu list
  def printGpus(self):
    for gpu in self.amdGpus:
      gpu.printGpu()

  # Check temperatures and alert if temperatures exceed a determined amount
  def checkTemps(self):
    for gpu in self.amdGpus:
      if gpu.getCurrentTemp() > self.maxTemp:
        # Send Alert
        if bot is not None:
          self.bot.post("GPU " + str(gpu.getGpuNumber()) + " Running Hot!")
          self.bot.post("Running at " + str(gpu.getCurrentTemp()))
      else:
        pass
  # Posts current miner information to the heroku server
  def postUpdate(self):
    frozen = jsonpickle.encode(self.amdGpus)
    r = requests.post(HEROKU_URL + "/localDump", frozen)

#    r.status_code = 404
#    r.reason = "could not find shit"

    if (r.status_code != 200):
      print(str(r.status_code), r.reason)
      
      self.bot.post("Heartbeat to Heroku Failed: " 
                    + str(r.status_code) + " "
                    + r.reason)

class gpuInfo:
# Takes a shwtemp and returns a gpuInfo Object
  def __init__(self, shwtemp, gpuNumber):
    self.label = shwtemp[0]
    self.currentTemp = shwtemp[1]
    self.highTemp = shwtemp[2]
    self.criticalTemp = shwtemp[3]
    self.gpuNumber = gpuNumber

  # Returns the label of this object
  def getLabel(self):
    return self.label

  # Returns the currentTemp of this object
  def getCurrentTemp(self):
    return self.currentTemp

  # Returns the highTemp of this object
  def getHighTemp(self):
    return self.highTemp

  # Returns the criticalTemp of this object
  def getCriticalTemp(self):
    return self.criticalTemp
  
  # Returns the gpuNumber of this object
  def getGpuNumber(self):
    return self.gpuNumber

  # Prints GPU object
  def printGpu(self):
    printout = \
      "AMD GPU " + str() + "\n"\
       + "*" * 10 + "\n"\
       + "label: " + self.label + "\n"\
       + "Current Temp: " + str(self.currentTemp) + "\n"\
       + "High Temp: " + str(self.highTemp) + "\n"\
       + "CriticalTemp: " + str(self.criticalTemp) + "\n"
    print(printout)
    return printout

  # Returns the property of the gpu object as a csv string
  def gpu2csv(self):
    return str(self.gpuNumber + ","\
        + self.label + ","\
        + self.currentTemp + ","\
        + self.highTemp + ","\
        + self.criticalTemp)


class PoolStatus:
  
  def __init__(self, url = ETHERMINE_URL):
    if DEBUG:
      # Debug Version 
      with open('ethermine.json') as json_data:
        self.json = json.load(json_data)
    else:
      # Real version
      self.json = requests.get(url).json()
  # Returns the address being used from ethermine 
  def getAddress(self):
    return self.json["address"]
  
  # Returns the total hashrate of the wallet from ethermine
  def getHashrate(self):
    return self.json["hashRate"]

  # Returns the amount of Eth generated per minute from ethermine 
  def getEthPerMin(self):
    return self.json["ethPerMin"]
  
  # Returns the usd generated per minute from ethermine
  def getUsdPerMin(self):
    return self.json["usdPerMin"]

  # Returns a string of the PoolStatus
  def getStatus(self):
    return("Address: " + self.getAddress() + "\n" + \
    "Hashrate: " + self.getHashrate() + "\n" + \
    "Eth per min: " + str(self.getEthPerMin()) + "\n" +\
    "USD per min: " + str(self.getUsdPerMin()))

  # Print String
  def printStatus(self):
    print(self.getStatus())
    return self.getStatus()

class SystemStatus:
  
  def __init__(self, poolStatus, gpuStatuses):
    # A Pool Status
    self.pool = poolStatus

    # A List of GpuInfos
    self.gpus = gpuStatuses

  # Updates the pool status with a given pool status
  def setPool(self, poolStatus):
    self.pool = poolStatus

  # Updates the gpu stautses with a given list of gpu statuses
  def setGpus(self, gpuStatuses):
    self.gpus = gpuStatuses

  def printStatus(self):
    message = str("Pool Info:" + "\n"
                  + self.pool.printStatus() + "\n"
                  + "Gpu Info: ")
    for gpu in self.gpus:
      message += gpu.printGpu()
    print(message)
    return message
'''
# Running stuff
m = monitor()
m.recordTemps()
m.checkTemps()
'''
if __name__ == "__main__":
#  tests.testPoolStatus()
#  tests.testSystemStatus()
  m = monitor()
  m.postUpdate()
