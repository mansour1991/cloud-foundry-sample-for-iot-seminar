from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time
import ibmiotf.application


vcap = json.loads(os.getenv("VCAP_SERVICES"))


client = None

deviceId = os.getenv("DEVICE_ID")
deviceType = os.getenv("DEVICE_TYPE")

try:
    options = {
        "org": vcap["iotf-service"][0]["credentials"]["org"],
        "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
        "auth-method": "apikey",
        "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
        "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
    }
    client = ibmiotf.application.Client(options)
    client.connect()

except ibmiotf.ConnectionException as e:
    print e

app = Flask(__name__)

if os.getenv("PORT"):
    port = int(os.getenv("PORT"))
else:
    port = 8080

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/light/<command>', methods=['GET', 'POST'])
def light_route(command):
    print command
    myData = {'command' : command}
    client.publishEvent(deviceType, deviceId, "light", "json", myData)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
