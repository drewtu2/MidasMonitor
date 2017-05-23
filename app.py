import os

# Write the keyfile needed by groupme
with open(".groupy.key", "w") as key_file:
  key_file.write(os.environ.get("GROUPME_APIKEY"))

import groupy
import jsonpickle
from flask import Flask, request
from monitor import PoolStatus, gpuInfo, SystemStatus, testData
import tests

################################################################################
# Initialization
################################################################################
app = Flask(__name__)

g = groupy.Group.list().filter(group_id=os.environ.get("GROUPME_GROUPID")).first
b = groupy.Bot.list().filter(bot_id=os.environ.get("GROUPME_BOTID")).first

ETHERMINE_URL = "https://ethermine.org/api/miner_new/3c76329390da17c727fa1bbbeb2fc45c80a7d92f"

################################################################################
# Helper Functions
################################################################################

# Run when groupme triggers the callback url. 
def handleBotCallback():
  message = g.messages().newest.text
  print(message)
  if "status" in message.lower():
    b.post(status.printStatus())
  return "OK"
  
# Runs when the miner sends an update. 
def updateStatus(gpuStatus):
  status.gpus = jsonpickle.decode(gpuStatus)
  status.pool = PoolStatus(ETHERMINE_URL)
  return "OK"


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
@app.route("/localDump", methods=["POST"])
def handleMinerUpdate():
  return updateStatus(request.data)


################################################################################
# App Launch 
################################################################################
if __name__ == "__main__":
  # Initalize empty, populate in update. 
  status = SystemStatus(None, None)
  gpuList = tests.genGpuList()
  test_frozen = jsonpickle.encode(gpuList)
  updateStatus(test_frozen)
  b.post("New Code Loaded Sucessfully")

  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)

