import psutil
from samplePsutil import testData
from datetime import datetime

class monitor:

  def __init__(self):
    #sensorTempResponse = psutil.sensors_temperatures()
    #self.amdGpus = sensorTempResponse("amdgpu")
    self.amdGpus = self.buildGpuList(testData)
    self.logfileName = "midas.log"
    self.maxTemp = 70
  
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
        gpu.printGpu()
      logfile.write("*" * 80 + "\n")

  # Check temperatures and alert if temperatures exceed a determined amount
  def checkTemps(self):
    for gpu in self.amdGpus:
      if gpu.getCurrentTemp() > self.maxTemp:
        # Send Alert
        print("GPU", gpu.getGpuNumber(), "Running Hot!")
        print("Running at", gpu.getCurrentTemp())
      else:
        pass


# Takes a shwtemp and returns a gpuInfo Object
class gpuInfo:
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
       + "CriticalTemp: " + str(self.criticalTemp) + "\n\n"
    print(printout)

m = monitor()
m.recordTemps()
m.checkTemps()
