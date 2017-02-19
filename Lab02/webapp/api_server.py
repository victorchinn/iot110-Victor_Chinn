from gpio import PiGpio
from flask import *

app = Flask(__name__)
pi_gpio = PiGpio()

## ... add APIs <here>

@app.route("/")
def index():
    # create an instance of my pi gpio object class.
    pi_gpio = PiGpio()
    switch_state = pi_gpio.read_switch()
    led1_state = pi_gpio.get_led(1)
    led2_state = pi_gpio.get_led(2)
    led3_state = pi_gpio.get_led(3)
    return render_template('index.html', switch=switch_state,
                                led1=led1_state,
                                led2=led2_state,
                                led3=led3_state)

# ============================== API Routes ===================================
# ============================ GET: /leds/<state> =============================
# read the LED status by GET method from curl for example
# curl http://iot8e3c:5000/led/1
# curl http://iot8e3c:5000/led/2
# -----------------------------------------------------------------------------
@app.route("/leds/<int:led_state>", methods=['GET'])
def leds(led_state):
  return "LED State:" + str(pi_gpio.get_led(led_state)) + "\n"


# =============================== GET: /sw ====================================
# read the switch input by GET method from curl for example
# curl http://iot8e3c:5000/sw
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
# ============================== API Routes ===================================

if __name__ == "__main__":
    app.run(host='192.168.10.54', debug=True)

