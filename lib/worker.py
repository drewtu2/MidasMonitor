import constants
import monitor

if __name__ == "__main__":
  m = monitor.monitor()
  m.checkAlive()
  m.checkTemps()
  m.heartBeat()
