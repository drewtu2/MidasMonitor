import psutil
import groupy 
import requests
import json
import jsonpickle
import constants
import os
from subprocess import call
from samplePsutil import testData
from datetime import datetime, timedelta

class monitor:

  def __init__(self):
    # TODO: Switch when running on Midas
    #sensorTempResponse = psutil.sensors_temperatures()
    #self.amdGpus = self.buildGpuList(sensorTempResponse)
    self.amdGpus = self.buildGpuList(testData)

    self.logfileName = "midas.log"
    self.maxTemp = 70
    self.botName = "Bot of Midas"
    self.lastSuccessfulHeartbeat = datetime.now()

    self.g = groupy.Group.list().filter(group_id=os.environ.get("GROUPME_GROUPID")).first

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
    print("Monitor: Checking Temperatures...")
    for gpu in self.amdGpus:
      self._checkTempsHelper(gpu)

  # Helper function for checkTemps
  def _checkTempsHelper(self, gpu):
    if gpu.getCurrentTemp() > self.maxTemp:
      # Send Alert
      if self.bot is not None:
        try:
          self.bot.post("GPU " + str(gpu.getGpuNumber()) + " Running Hot!" + "\n"
                        + "Running at " + str(gpu.getCurrentTemp()))
        except:
          print("Error Posting temp update to Groupme")
      else:
        pass
    else:
      pass

  # Posts current miner information to the heroku server
  def heartBeat(self):
    print("Monitor: sending Heartbeat")
    frozen = jsonpickle.encode(self.amdGpus)
    try:
      r = requests.post(constants.HEROKU_URL + constants.HEROKU_HEARTBEAT, frozen)
      #r.status_code = 404
      #r.reason = "could not find shit"
      if (r.status_code != 200):
        print(str(r.status_code), r.reason)
        self.bot.post("Monitor: Heartbeat to Heroku Failed: " 
                      + str(r.status_code) + " "
                      + r.reason)
      else:
        self.lastSuccessfullHeartbeat = datetime.now()
    except:
      print("ERROR: trying to post heartbeat")

  
  # Restart the miner under the following conditions.
  # If last message in the group is "restart", then miner is dead. 
  # AND
  # 1. If the hashrate in the group is 0
  # OR
  # 2. If the last successfull heartbeat was over an hour ago. 
  #
  # TODO: Actually, just restart if requested...
  def checkAlive(self):
    print("Monitor: Checking if alive...") 
    #if self.restartRequested() && (self.zeroHash() || self.staleHeart()) 
    if self.restartRequested():
      self.rebootMiner()
  
  # Returns a boolean if the last message in the group is exectly "RESTART"
  def restartRequested(self):
    message = self.g.messages().newest.text
    print(message)
    if message.strip()=="RESTART":
      print("Restart request received. Executing...")
      self.bot.post("Restart request received. Executing...")
      return True
    else:
      print("Restart not requested...")
      return False

  # Returns a boolean if the hashrate from ethermine is less than constants.MIN_HASHRATE
  def lowHash(self):
    if PoolStatus().getHashrate() < constants.MIN_HASHRATE:
      return True
    else:
      return False

  # Returns a boolean if the last successfull heartbeat was over an hour ago
  def staleHeart(self):
    secondsSinceLastBeat = (lastSuccessfulHeartbeat - datetime.now()).total_seconds()
    minutesSinceLastBeat = divmod(secondsSinceLastBeat, SECONDS_PER_MINUTE)

    if minutesSinceLastBeat[0] > constants.HEARTBEAT_TIMEOUT:
      return True
    else:
      return False

  # Reboot the machine. All necessary scripts should be started by a cronjob on startup.
  def rebootMiner(self):
    print("Calling reboot...")
    call(["reboot"])

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
  
  def __init__(self, url = constants.ETHERMINE_URL):
    if constants.DEBUG:
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
  # JSON => Float
  def getHashrate(self):
    l = []
    for t in self.json["hashRate"].split():
      try:
        l.append(float(t))
      except ValueError:
        pass
    return l[0]

  # Returns the amount of Eth generated per minute from ethermine 
  def getEthPerMin(self):
    return self.json["ethPerMin"]
  
  # Returns the amount of Eth generated per day from ethermine
  def getEthPerDay(self):
    return self.getEthPerMin()*MINUTES_PER_HOUR*HOUR_PER_DAY

  # Returns the usd generated per minute from ethermine
  def getUsdPerMin(self):
    return self.json["usdPerMin"]

  # Returns the amount of USD generated per day from ethermine
  def getUsdPerDay(self):
    return self.getUsdPerMin()*MINUTES_PER_HOUR*HOUR_PER_DAY

  # Returns a string of the PoolStatus
  def getStatus(self):
    return("Address: " + self.getAddress() + "\n" + \
    "Hashrate: " + str(self.getHashrate()) + "MH/s\n" + \
    "Eth per min: " + str(self.getEthPerMin()) + "\n" +\
    "Eth per day: " + str(self.getEthPerDay()) + "\n" +\
    "USD per min: " + str(self.getUsdPerMin()))+ "\n" +\
    "USD per day: " + str(self.getUsdPerDay()))

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


if __name__ == "__main__":
#  constants.testPoolStatus()
#  constants.testSystemStatus()
  m = monitor()
  #m.heartBeat()
  m.checkAlive()
