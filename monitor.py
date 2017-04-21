import psutil
from samplePsutil import testData
from datetime import datetime

class monitor:

  def __init__(self):
    #sensorTempResponse = psutil.sensors_temperatures()
    #self.amdGpus = sensorTempResponse("amdgpu")
    self.amdGpus = testData["amdgpu"]
    self.logfileName = "midas.log"

  def recordTemps(self):
    with open(self.logfileName, "a") as logfile:
      logfile.write(str(datetime.now()) + "\n")
      logfile.write("*" * 80)
      logfile.write("\n")
      logfile.write(self.getGpuTempList())
      logfile.write("*" * 80 + "\n")

  # Takes a list of GPU shwtemps and returns them in a printable format
  # List of shwtemps => String
  def getGpuTempList(self):
    count = 0
    printout = ""
    for gpu in self.amdGpus:
      printout += self.getGpuShwtemps(gpu, count)
      count += 1
    return printout
 
  # Takes a GPU shwtemp and returns it in a printable format 
  # GpuShwtemp + Number => String
  def getGpuShwtemps(self, gpu, count):
    printout = \
      "AMD GPU " + str(count) + "\n"\
       + "*" * 10 + "\n"\
       + "label: " + gpu[0] + "\n"\
       + "Current Temp: " + str(gpu[1]) + "\n"\
       + "High Temp: " + str(gpu[2]) + "\n"\
       + "CriticalTemp: " + str(gpu[3]) + "\n\n"
    return printout

  # Prints all current GPU temps to the screen
  def printGpuTempList(self):
    print(self.getGpuTempList())

m = monitor()
m.recordTemps()
