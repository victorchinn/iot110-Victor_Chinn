#
# Victor Chinn
# Lab 01
# UW IOT Course
# January 19 2017
#

from flask import Flask
import socket

## Get my machine hostname
# if socket.gethostname().find('.') >= 0:
#     hostname=socket.gethostname()
# else:
#     hostname=socket.gethostbyaddr(socket.gethostname())[0]

hostname ='iot82dd'; 

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello IoT World from Victor Chinn's RPi3: " + hostname + "\r\n"

## Run the website and make sure to make
##  it externally visible with 0.0.0.0:5000 (default port)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
