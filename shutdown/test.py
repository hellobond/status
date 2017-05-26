#test.py
from shutdown import Shutdown

S = Shutdown(20)

to_continute = 1
while to_continute:
	to_continue = S.logic()