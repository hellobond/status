#port of status.cpp

import time
import subprocess
import RPi.GPIO as GPIO


class Shutdown:
    
    def __init__(self, SHUTDOWN_SW):
        self.shutdown_pressed = 0
        self.state = 0
        self.SW = SHUTDOWN_SW
        self.down = 0
        self.up = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SHUTDOWN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(SHUTDOWN_SW, GPIO.BOTH, callback=self.shutSWISR)


    def shutSWISR(self, chan):
        self.shutdown_pressed = 1

    def todo(self):
        #args = ["sudo", "shutdown"to, "now"]
        args = ["sudo", "sh", "tool_operator_down.sh"]
        print subprocess.call(args)


    def logic(self):
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
        cont = 1
        while cont:
            cont = self.logic()