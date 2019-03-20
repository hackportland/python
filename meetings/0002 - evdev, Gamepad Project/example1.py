#!/usr/bin/python3

"""
Read the devices connected to the computer.  Change the mode of the gamepad and run this script again.
"""

# update the user
print ("\nDEVICE LIST TEST\n")

# support for evdev
import evdev

# iterate over the devices present in /dev/input
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

# show details for all of the devices found
print ("Device Path, Device Name, Device Phys ID")
for device in devices:
    print ("%s,%s,%s"%(device.path, device.name,device.phys))

# add some output at the end
print ("\n\n")
