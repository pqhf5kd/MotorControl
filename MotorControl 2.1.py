# -----------------------------------------------
# MotorControl
#
# uses https://beta.pybricks.com/ , LEGO City hub, LEGO remote control
# connect 1 or 2 motors of any kind to Port A and B
#
# Version 2.1 / This is a beta, so no guarantee for proper function ;-)
# -----------------------------------------------

from pybricks.pupdevices import DCMotor, Motor, Remote
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.hubs import CityHub
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from uerrno import ENODEV#  control City hubs

# -----------------------------------------------
#  Set user defined values
# -----------------------------------------------

mode=1              # start with function number...
autoacc = False     # accelarate continously when holding butten 

accdelay = 100      # wait for next acceleration (in ms)
step = 10           # accelerate in steps of 10 

vmax1 = 100         # maximum Speed Set1
vmin1 = 20          # minimun speed Set1

vmax2 = 50          # maximum Speed Set2
vmin2 = 10          # minimun speed Set2

# -----------------------------------------------

dirMotorA = 1       # Direction 1 or -1
dirMotorB = 1       # Direction 1 or -1

watchdog = False    #    "True" or "False": Stop motors when loosing remote connection
remoteTimeout =3    #    hub waits x seconds for remote connect after starting hub 

# assign buttons to function1 
# syntax: function = "name"
# name may  be "A+","A-","A0","B+","B-","B0","CENTER"

UP = "A+"
DOWN = "A-"
STOP = "A0"
SWITCH = "CENTER"

# Color and brightness of Hub LEDs
LEDconn = Color.GREEN*0.3       # if Hub connected, color * brightness
LEDnotconn = Color.RED*0.5      # if Hub is not connect, color * brightness

mode=1                          # start with function number...

# -----------------------------------------------
#  function 1 / drive motors
# -----------------------------------------------

def function1():
    if mode == 1:
        vmax = vmax1
        vmin = vmin1

    if mode == 2:
        vmax = vmax2
        vmin = vmin2

    global v
    if CheckButton(UP) and not CheckButton(STOP) : 
        for x in range (1, step + 1):
            v = v + 1
            if v > vmax :
                v = vmax
            if v > 0 and v < vmin:    
                v = vmin
            if abs(v) < vmin:
                v = 0
            drive()
            wait (accdelay)  
        
        # further acceleration if button keeps pressed
        while autoacc == False and CheckButton(UP) :    
            wait (100)
        # avoid changing direction when reaching "0"     
        while v == 0 and  CheckButton(UP):  
            wait (100)
        
    if CheckButton(DOWN) and not CheckButton(STOP):
        
        for x in range (1, step + 1):
            v = v-1
            if v < vmax*-1 :
                v = vmax*-1
            if v < 0 and v > vmin*-1:    
                v = vmin*-1
            if abs(v) < vmin :
                 v = 0   
            drive()
            wait (accdelay)  
        
        # further acceleration if button keeps pressed
        while autoacc == False and CheckButton(DOWN) :    
            wait (100)
        # avoid changing direction when reaching "0"
        while v == 0 and  CheckButton(DOWN) :    
            wait (100)
        
        #wait (accdelay)

    if CheckButton(STOP): 
        v = 0
        drive()
        wait (100)    
        

# -----------------------------------------------
#  function 2
# -----------------------------------------------
           
def function2():
    if CheckButton(UP):
        timer[1].set(3000)
    if timer[1].check(): 
        print("Do something")

# -----------------------------------------------
# program routines and classes
# -----------------------------------------------

# ----CheckButton -------------------------------------------

def CheckButton(x):
    try:
        button = remote.buttons.pressed()
        #print (x)
        if x == "A+"  : x = Button.LEFT_PLUS
        if x == "A-" : x = Button.LEFT_MINUS
        if x == "A0"  : x = Button.LEFT

        if x == "B+"  : x = Button.RIGHT_PLUS
        if x == "B-" : x = Button.RIGHT_MINUS
        if x == "B0"  : x = Button.RIGHT
    
        if x == "CENTER"  : x = Button.CENTER
        
        if x in button:
            return True
        else:
            return False
    except:
        return()

# ----delay -------------------------------------------

class delay:
    def __init__(self,id,time=0,watch=StopWatch(),busy=False):
        self.id=id
        self.time=time
        self.watch=watch
        self.busy=busy
        print ("Init Timer",id)
    # set a timer        
    def set(self,x):
        if  self.busy == False:
            self.busy = True
            self.watch.reset()
            self.time = x
            print("Timer",timer[1].id, "set to",x)
    #check if timer is reached, then return "True"
    def check(self):
        if self.busy == True:
            if self.watch.time() > self.time:
                self.busy = False
                self.time=0 
                print("Timer",timer[1].id, "stopped")
                return(True)
        else:
            return(False)

# ----drive -------------------------------------------

def drive():
    global vold
    global v
    print (v)
    if vold != v:
        # for each motor 1,2 
        for x in range(1,3):
            # set speed and direction
            s = v*round(motor[x].getDir())
            # real motor commands depending on motor type
            if motor[x].getDir() != 0 and motor[x].getType() == "Motor" : motor[x].obj.run(s*10)
            if motor[x].getDir() != 0 and motor[x].getType() == "DCMotor" : motor[x].obj.dc(s) 
        vold = v
            
# ----portcheck -------------------------------------------

def portcheck(i):
    # list of motors, 1 +2 contain string "DC"
    devices = {
    1: "Wedo 2.0 DC Motor",
    2: "Train DC Motor",
    38: "BOOST Interactive Motor",
    46: "Technic Large Motor",
    47: "Technic Extra Large Motor",
    48: "SPIKE Medium Angular Motor",
    49: "SPIKE Large Angular Motor",
    75: "Technic Medium Angular Motor",
    76: "Technic Large Angular Motor",
}
    port = motor[i].getPort()
    # Try to get the device, if it is attached.
    try:
        device = PUPDevice(port)
    except OSError as ex:
        if ex.args[0] == ENODEV:
            # No device found on this port.
            motor[i].setType("---")
            print(port, ": not connected")
            return ("---")
        else:
            raise

    # Get the device id
    id = device.info()['id']
    
    # Look up the name.
    try:
        # get the attributes for tacho motors
        if "Motor" in devices[id] and not("DC" in devices[id]): 
            motor[i].setType("Motor")
            motor[i].obj = Motor(port)
            speed_limit, acceleration_limit, duty_limit, torque_limit = Motor(port).control.limits()
            motor[i].setSpeed(speed_limit)
            motor[i].setAcc(acceleration_limit)
        # and set type for simple DC Motors    
        if "DC" in devices[id]:
            motor[i].setType("DCMotor")
            motor[i].obj = DCMotor(port)
            
    except KeyError:
        motor[i].stype("unkown")
        print(port, ":", "Unknown device with ID", id)
    wait(100)    
    print ("--")
    print(port, ":", devices[id], motor[i].getType(),motor[i].getSpeed(),motor[i].getAcc())

# ---- device  -------------------------------------------
    
class device():
    # store the device infos for each motor
    def __init__(self,port,dir):
        self.port = port
        self.dir = dir
        self.type=""
        self.speed=99
        self.acc=99
        self.obj=""
                
    def setType(self,x) : self.type = x
    def setSpeed(self,x): self.speed = x
    def setAcc(self,x)  : self.acc = x
    
    def getType(self)   : return self.type
    def getPort(self)   : return self.port
    def getDir(self)    : return self.dir
    def getSpeed(self)  : return self.speed
    def getAcc(self)    : return self.acc

# -----------------------------------------------
# globals
# -----------------------------------------------
vmax = vmax1
vmin = vmin1
        
v = 0
vold = 0
remoteConnected = False

# -----------------------------------------------
# Ininitialize
# -----------------------------------------------

hub = CityHub()

#define timers
timer = [0,0,0]
timer[1] = delay(1)
timer[2] = delay(2)
           
#define motors
motor = [0,0,0]
motor[1] = device(Port.A,dirMotorA)
motor[2] = device(Port.B,dirMotorB)

# get the port properties
portcheck(1)
portcheck(2)    

# -----------------------------------------------
# remote connect
# -----------------------------------------------

hub.light.on(Color.RED)
try:
    remote = Remote(timeout=remoteTimeout*1000)
except OSError as ex:
    hub.system.shutdown()

# -----------------------------------------------
# main loop
# -----------------------------------------------

while True:
   
    # --check if remote is connected ---------------------------------
    
    try:
        button = remote.buttons.pressed()
        hub.light.on(LEDconn)
        remoteConnected = True
    except OSError as ex:
        hub.light.on(LEDnotconn)
        print("Remote not connected")
        remoteConnected = False
       
        if watchdog == True:
            v=0
            drive()
        try:
            # reconnect remote
            remote = Remote(timeout=1000)
            wait(100)
            print("Remote reconnected")
            remoteConnected = True
        except OSError as ex:
            print("Remote not connected")

            
    if CheckButton(SWITCH):
        mode = mode+1
        if mode > 2: 
            mode = 1
        print (mode)
        while CheckButton(SWITCH):
            button = remote.buttons.pressed()
            wait (100)

    if mode == 1 :  function1()     
    if mode == 2 :  function1()    
    
    wait(10)
    
