#test.py
from shutdown import Shutdown

#Pin 20 as referenced by BCM Documentation.
# (Corresponds to physical pin 38)

swtich_BCM_pin = 20

S = Shutdown(swtich_BCM_pin)

to_continute = 1
while to_continute:
	to_continue = S.logic()