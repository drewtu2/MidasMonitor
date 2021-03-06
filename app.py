import os
import sys
sys.path.append("lib/" )

# Write the keyfile needed by groupme
with open(".groupy.key", "w") as key_file:
  key_file.write(os.environ.get("GROUPME_APIKEY"))

import groupy
import jsonpickle
import constants 
import threading
import time
from flask import Flask, request
from monitor import PoolStatus, gpuInfo, SystemStatus, testData
from datetime import datetime, timedelta

################################################################################
# Initialization
################################################################################
app = Flask(__name__)

g = groupy.Group.list().filter(group_id=os.environ.get("GROUPME_GROUPID")).first
b = groupy.Bot.list().filter(bot_id=os.environ.get("GROUPME_BOTID")).first
lastHeartbeat = datetime.now()

################################################################################
# Helper Functions
################################################################################

# Run when groupme triggers the callback url. 
def handleBotCallback():
  message = g.messages().newest.text
  print(message)
  if message.lower().strip() == "status":
    b.post(status.printStatus())
  elif message.lower().strip() == "help":
    b.post(constants.usage)
  return "OK"
  
# Runs when the miner sends an update. 
def updateStatus(gpuStatus):
  status.gpus = jsonpickle.decode(gpuStatus)
  status.pool = PoolStatus(constants.ETHERMINE_URL)

  lastHeartBeat = datetime.now() 

  # If the hashrate is too low, send warning notification. 
  if status.pool.getHashrate() < constants.MIN_HASHRATE:
    b.post("WARNING: Hashrate at " 
        + str(status.pool.getHashrate()) + "MH/s. Check miner")
  
  return "OK"

# Starts the Heartbeat Checking thread.
def startHeartbeatChecker():
  timerThread = threading.Thread(target=checkHeartbeat)
  timerThread.daemon = True
  timerThread.start()

# Check how long its been since the last heartbeat
# Runs in its own thread. 
def checkHeartbeat():
  next_call = time.time()
  delay = constants.TEN_MINUTES_SECONDS
  #delay = 10
  while True:
    print("Heartbeat called")
    secondsSinceLastBeat = (lastHeartbeat - datetime.now()).total_seconds()
    minutesSinceLastBeat = divmod(secondsSinceLastBeat, constants.SECONDS_PER_MINUTE)
    if minutesSinceLastBeat[0] > constants.HEARTBEAT_TIMEOUT:
      b.post("WARNING: DELAYED HEARTBEAT \n"
          + "Last beat: " + str(minutesSinceLastBeat[0]) + " minutes ago")
    next_call = next_call + delay;
    time.sleep(next_call - time.time())


################################################################################
# URL Routing
################################################################################

# Route to the basic "Hello World" page.... 
@app.route("/")
def hello():
  return "Hello world!"

# Handle the GroupMe Notification of a new message that has arrived
@app.route("/bot", methods=["POST"])
def botCallback():
  return handleBotCallback()


# Handle the arrival of a miner status update. 
@app.route(constants.HEROKU_HEARTBEAT, methods=["POST"])
def handleMinerUpdate():
  return updateStatus(request.data)


################################################################################
# App Launch 
################################################################################
if __name__ == "__main__":
  # Initalize empty, populate in update. 
  status = SystemStatus(None, None)
  gpuList = constants.genGpuList()
  test_frozen = jsonpickle.encode(gpuList)
  updateStatus(test_frozen)

  startHeartbeatChecker()

  b.post("Heroku: New Code Loaded Sucessfully")

  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)

