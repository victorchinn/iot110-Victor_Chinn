#!/usr/bin/python
import time
from gpio import PiGpio
from bmp280 import PiBMP280
from debouncer import Debouncer
from flask import *

# create GPIO Object and Switch Debouncer
pi_gpio = PiGpio()
db = Debouncer()
# create an array of my pi bmp280 sensor dictionaries
sensor = {"name" : "bmp280", "addr" : 0x76, "chip" : PiBMP280(0x76) , "data" : {}}
(chip_id, chip_version) = sensor["chip"].readBMP280ID()
sensor["data"]["chip_id"] = chip_id
sensor["data"]["chip_version"] = chip_version

# ============================== Functions ====================================
def get_sensor_values():
    (temperature, pressure) = sensor["chip"].readBMP280All()
    sensor["data"]["temperature"] = { "reading": temperature, "units" : "C" }
    sensor["data"]["pressure"] = { "reading": pressure, "units" : "hPa" }
    return sensor["data"]

# ============================== API Routes ===================================
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
    # create an instance of my pi gpio object class.
    # pi_gpio = PiGpio()
    # switch_state = pi_gpio.read_switch()
    # led1_state = pi_gpio.get_led(1)
    # led2_state = pi_gpio.get_led(2)
    # led3_state = pi_gpio.get_led(3)
    # return render_template('index.html', switch=switch_state,
    #                             led1=led1_state,
    #                             led2=led2_state,
    #                             led3=led3_state)
# ============================ GET: /leds/<state> =============================
# read the LED status by GET method from curl for example
# curl http://iot8e3c:5000/leds/1
# curl http://iot8e3c:5000/leds/2
# curl http://iot8e3c:5000/leds/3
# -----------------------------------------------------------------------------
@app.route("/leds/<int:led_state>", methods=['GET'])
def leds(led_state):
  return "LED State:" + str(pi_gpio.get_led(led_state)) + "\n"


# =============================== GET: /sw ====================================
# read the switch input by GET method from curl for example
# curl http://iot8e3c:5000/switch
# -----------------------------------------------------------------------------
@app.route("/sw", methods=['GET'])
def sw():
  return "Switch State:" + str(pi_gpio.read_switch()) + "!\n"

# ======================= POST: /ledcmd/<data> =========================
# set the LED state by POST method from curl. For example:
# curl --data 'led=1&state=ON' http://iot8e3c:5000/ledcmd
# -----------------------------------------------------------------------------
@app.route("/ledcmd", methods=['POST'])
def ledcommand():
    cmd_data = request.data
    print "LED Command:" + cmd_data
    led = int(str(request.form['led']))
    state = str(request.form['state'])
    if(state == 'OFF'):
        pi_gpio.set_led(led,False)
    elif (state == 'ON'):
        pi_gpio.set_led(led,True)
    else:
        return "Argument Error"

    return "Led State Command:" + state + " for LED number:"+ str(led) + "\n"
# -----------------------------------------------------------------------------

# =========================== Endpoint: /myData ===============================
# read the gpio states by GET method from curl for example
# curl http://iot8e3c:5000/myData
# -----------------------------------------------------------------------------
@app.route('/myData')
def myData():
    def get_state_values():
        while True:
            # return the yield results on each loop, but never exits while loop
            raw_switch = pi_gpio.read_switch()
            debounced_switch = str(db.debounce(raw_switch))
            data_obj = get_sensor_values()
            data_obj["led_red"] = str(pi_gpio.get_led(1))
            data_obj["led_grn"] = str(pi_gpio.get_led(2))
            data_obj["led_blu"] = str(pi_gpio.get_led(3))
            data_obj["switch"] = debounced_switch
            yield('data: {0}\n\n'.format(data_obj))
            time.sleep(1.0)
    return Response(get_state_values(), mimetype='text/event-stream')
# ============================== API Routes ===================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
