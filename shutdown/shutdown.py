"""
    shutdown

    ~~~~~~~~~

    A module for shutting down the HWR via executrion of the bash script.

    The HW interface is a off-mom swith pulling the SHUTDOWN_SW pin low for >=3 sec.

    :author: Galen Church
    :copyright: 2017

"""

# ------------------------------------------------
#   Imports
# ------------------------------------------------


import time
import subprocess
import RPi.GPIO as GPIO

# ------------------------------------------------
# Classes
# ------------------------------------------------

class Shutdown:
    
    def __init__(self, SHUTDOWN_SW):
        self.shutdown_pressed = 0
        self.state = 0
        self.SW = SHUTDOWN_SW
        self.down = 0
        self.up = 0

        #set GPIO to reference IO Pins based on BCM convention
        GPIO.setmode(GPIO.BCM)
        
        #set SHUTDOWN_SW to input with internal pull-up
        GPIO.setup(SHUTDOWN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #configure inturrupts to trigger of both rising and falling edges
        GPIO.add_event_detect(SHUTDOWN_SW, GPIO.BOTH, callback=self.shutSWISR)


    def shutSWISR(self, chan):
        """Callback function acting as ISR.  Sets inturrupt flag.
        """
        self.shutdown_pressed = 1

    def todo(self):
        """Function executed when shutdown conditions are met.  
        Currently executes tool_operator_down.sh as root in current dir
        """
        args = ["sudo", "sh", "tool_operator_down.sh"]
        print subprocess.call(args)


    def logic(self):
        """The logic of the shutdown loop without the loop.
        state = 0: First inturrupt tripped set self.down with start of 3sec count.
        state = 1: waiting for 3sec to pass to execure self.todo().  
            if inturrupt triggered and self.SW is High, i.e. button was released, set state = 0
        """
        if self.shutdown_pressed and (self.state ==  0):
            if not GPIO.input(self.SW):
                self.down = time.clock()
                self.shutdown_pressed = 0
                print "ShuttingDown...press detected"
                time.sleep(.00005)
                self.state = 1
                return 1
            return 1
        if self.state == 1:
            self.up = time.clock()
            delta = self.up - self.down

            if self.shutdown_pressed and GPIO.input(self.SW):
                self.state = 0
                self.shutdown_pressed = 0
                return 1
            else:
                if delta >= 3:
                    print "Shutting Down Now!"
                    self.todo()
                    return 0
                    #break
        return 1

    def loop(self):
        """Lazy loop for testing.  
        """
        cont = 1
        while cont:
            cont = self.logic()   