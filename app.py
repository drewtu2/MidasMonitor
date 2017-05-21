import os

# Write the keyfile needed by groupme
with open(".groupy.key", "w") as key_file:
  key_file.write(os.environ.get("GROUPME_APIKEY"))

import groupy
from flask import Flask, request

################################################################################
# Initialization
################################################################################
app = Flask(__name__)

g = groupy.Group.list().filter(group_id=os.environ.get("GROUPME_GROUPID")).first
b = groupy.Bot.list().filter(bot_id=os.environ.get("GROUPME_BOTID")).first

ETHERMINE_URL = "https://ethermine.org/api/miner_new/3c76329390da17c727fa1bbbeb2fc45c80a7d92f"

'''
A Status is a
- Miner Status
- Pool Status

A Miner Status is a
  List of gpuInfo Objects

A Pool Status is a
  Pool Status Object
'''

status = "Request Received"


################################################################################
# Helper Functions
################################################################################

# Run when groupme triggers the callback url. 
def handleBotCallback():
  message = g.messages().newest.text
  print(message)
  if "status" in message.lower():
    b.post(status)
  return "OK"
  
# Runs when the miner sends an update. 
def updateStatus(minerStatus):
  status.gpus = minerStatus
  status.ethermine = PoolStatus(ETHERMINE_URL)


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
  updateMinerStatus(requests.get_json())


################################################################################
# App Launch 
################################################################################
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)

