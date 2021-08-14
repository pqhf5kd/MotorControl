# MotorControl

This is simple program using pybricks to control motors connected to a LEGO Powered Up City Hub.
You need https://beta.pybricks.com/ to install it on the hub.
Use the first lines to configure according you needs.

# Requirements
You need:
* Browser with Bluetooth support, like Chrome or Edge
* The editor:  https://beta.pybricks.com/ 
* LEGO City hub, LEGO remote control

When installed in your hub no Smart device is needed any more.
Connect 1 or 2 motors of any kind to Port A and/or B

# Customizing
In the first section you find same parameters to customize the control

You can use two profiles to set 
* minimum speed
* maximum speed
* accelerate in steps of ...
* wait for next acceleration step(in ms)

Example\
*Profil_A = (20,100,10,100)*

Set the direction of the two motors\
*dirMotorA = 1*        
*dirMotorB = -1* \
B will rotate opposite to A

Accelarate continously when holding button  
*autoacc = True     (or „False“)* 

assign buttons to function   
*UP = "A+"* means: use the "A+" button to increase speed\

„Switch“ changes between Profil_A and Profil_B

Watchdog
Stop motors when loosing remote connection
*watchdog = True*
Continue driving when connection is lost, you can reconnect the remote by pressing the green button
*watchdog = False*

Hub waits x seconds for remote connect after starting hub 
*remoteTimeout =3*

Color and brightness of Hub LEDs
*LEDconn = Color.GREEN*0.3*       # if Hub connected, color * brightness
*LEDnotconn = Color.RED*0.5*      # if Hub is not connect, color * brightness
