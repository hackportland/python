#!/usr/bin/python3

"""
Protoype of gamepad configuration, based on configuration of EmulationStation:
  * listen for device button press
  * map events (MENU, FIRE, DIRECTION)
"""

# update the user
print ("\nCONFIG PROTOYPE TEST\n")

# support for evdev and event codes
import evdev

# support for I/O monitoring functions to monitor multiple inputs(FMI: https://pymotw.com/2/select/)
from select import select

# search for button press from any device
selected_gamepad=False

# tell the user what is expected
print ("Press any button on gamepad to configure it...\n")

while selected_gamepad==False:

 # the current set of devices, converted to file descriptors for select    
 devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
 
 # convert the devices to a dictionary of file descriptors so the select module can be used to monitor multiple devices 
 devices = {dev.fd: dev for dev in devices}

 # iterate over devices with select, processing channels that have new data
 for device in devices:
    #print ("%s,%s,%s"%(device.path, device.name,device.phys))
    # search for any button presses
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
         # watch for button events (KEY events) for button presses ()
         if (event.type == evdev.ecodes.EV_KEY):
            # uncomment show info in human readable format  
            #print(evdev.categorize(event))  
             
            # button was pressed on a gamepad, exit the search
            #print ("button pressed...")

            # save this gamepad as the selected device 
            selected_gamepad=devices[fd] 
            break

    # if a gamepad was found, stop iterating through gamepads 
    if selected_gamepad!=False:
            break

# now configure the device
print ("Configuring '%s' gamepad \n"%(selected_gamepad.name))

# map buttons
buttons=['FIRE','MENU', 'EXIT']
button_mapping={}
for b in buttons:
    print ("Press button for '%s'"%(b))
    # wait for a button
    for event in selected_gamepad.read_loop():
       # only process button presses (KEY, down)  
       if event.type == evdev.ecodes.EV_KEY and event.value==1:
         #print ("button pressed...")
         #print(evdev.categorize(event)) 

         # save this event code, mapping to the specified event
         button_mapping[event.code]=b
         
         # exit this loop
         break

# map sticks
sticks=['ROBOT_DRIVE','TURRENT']
stick_mapping={}
for s in sticks:
    print ("Move a stick for '%s'"%(s))
    # wait for a stick movement (events of type EV_ABS)
    for event in selected_gamepad.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
          # determine which stick was moved
          if event.code in [evdev.ecodes.ABS_Y, evdev.ecodes.ABS_X]:
            # map the left joystick
            stick_mapping[evdev.ecodes.ABS_Y]='Y'
            stick_mapping[evdev.ecodes.ABS_X]='X'  
          if event.code in [evdev.ecodes.ABS_RX, evdev.ecodes.ABS_RX]:
            # map the right joystick
            stick_mapping[evdev.ecodes.ABS_RY]='Y'
            stick_mapping[evdev.ecodes.ABS_RX]='X'  
          break  


# loop till EXIT is pressed
# TODO: post changes to MQTT broker (publish topics)
print ("Looping till EXIT is pressed...")
for event in selected_gamepad.read_loop():
    # process button presses (KEY, down)  
    if event.type == evdev.ecodes.EV_KEY and event.value==1:
      # if this button was mapped, process it
      if event.code in button_mapping.keys():  
        # tell the user which mapped event occured
        print ("  pressed %s"%(button_mapping[event.code]))
        if button_mapping[event.code]=="EXIT":
          print ("Exiting...")
          break  

    # process stick movements (EV_ABS)  
    if event.type == evdev.ecodes.EV_ABS:
      # if this stick was mapped, process it
      if event.code in stick_mapping.keys():
        print ("  moved %s stick, value=%s"%(stick_mapping[event.code], event.value))
              
      