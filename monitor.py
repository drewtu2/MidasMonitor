import psutil
from samplePsutil import testData


class monitor:

  def __init__(self):
    sensorTempResponse = psutil.sensors_temperatures()
    self.amdGpus = sensorTempResponse("amdgpu")
    
  def printGpuTemp(self):
    count = 0;
    for gpu in self.amdGpus.items():
      print("AMD GPU " + count)
      print("*" * 10)
      print("label: " + gpu(0))
      print("Current Temp: " + gpu(1))
      print("High Temp: " + gpu(2))
      print("CriticalTemp: " + gpu(3))
      print()
      count += 1

