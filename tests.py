import monitor

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
