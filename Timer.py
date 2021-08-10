# timer 
# -----------------------------------------------
# -----------------------------------------------
#
#
#
# -----------------------------------------------
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Stop, Button
from pybricks.hubs import CityHub
from pybricks.tools import *


# -----------------------------------------------
# program routines and functions
# -----------------------------------------------



#
# -----------------------------------------------
# program routines and functions
# -----------------------------------------------


class mtime:
    def __init__(self,time=0,watch=StopWatch(),busy=False):
        self.time=time
        self.watch=watch
        self.busy=busy
        print ("Init Timer")
            
    def set(self,x):
        if  self.busy == False:
            print("set--------------",x)
            self.busy = True
            self.watch.reset()
            self.time = x
   
    def check(self):
        if self.busy == True:
            if self.watch.time() > self.time:
                self.busy = False
                self.time=0 
                return("A")
                

timer = [1,2,3]
timer[1] = mtime()


FB = Remote()
 
while True:
   
    pressed = FB.buttons.pressed()
    #print (pressed)
    if Button.CENTER in pressed:
        timer[1].set(3000)
    if timer[1].check() == "A":
        print("Time over ")

        
    wait(100)