#!/usr/bin/python
import time
from debouncer import Debouncer
from gpio import PiGpio

# create an instance of the pi gpio driver.
pi_gpio= PiGpio()
# create an instance of the switch debouncer
db = Debouncer()
#
print('Debounce my Input Switch (Ctrl-C to stop)...')
while True:
    switch_raw = pi_gpio.read_switch()
    switch_debounced = db.debounce(switch_raw)
    pi_gpio.set_led(1,(switch_raw == 1))
    pi_gpio.set_led(2,(switch_debounced == 1))

    print('SW RAW: {0} SW DEBOUNCED: {1}'.format(switch_raw , switch_debounced))
    time.sleep(0.2)
