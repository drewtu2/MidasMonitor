import os
from flask import Flask, requests

app = Flask(__name__)

# Route to the basic "Hello World" page.... 
@app.route("/")
def hello():
  return "Hello world!"

# Handle the GroupMe Notification of a new message that has arrived
@app.route("/bot", methods=["POST"])
def handleGroupme():
  print(request.get_json)

# Handle the arrival of a miner status update. 
@app.route("/localDump", methods["POST"])
def handleMinerUpdate:
  print
  


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)

