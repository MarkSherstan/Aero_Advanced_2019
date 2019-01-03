import numpy as np
from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil
from tkinter import *


# Make a window to display GUI data
window = Tk()
window.title("Aero Heavy Lift Group")


# Make a 5x5 grid
for i in range(5):
    for j in range(5):
        lbl = Label(window, text="");
        lbl.grid(row=i, column=j)


# # Connect to vehicle
# connectionString = "/dev/tty.usbserial-DN04T9FH"
# print "Connecting on: ",connectionString
# vehicle = connect(connectionString, wait_ready = ["groundspeed","attitude","location.global_relative_frame"], baud = 57600)
#
#
# # Vehicle must be armed --> double check if this is true
# while not vehicle.armed:
#     print("Waiting for arming...")
#     print(vehicle.armed)
#     time.sleep(1)


# Servo command
def servoCommand(servoNumber,servoPosition):
    # msg = vehicle.message_factory.command_long_encode(
    # 0, 0,                                 # target_system, target_component
    # mavutil.mavlink.MAV_CMD_DO_SET_SERVO, # command
    # 0,                                    # confirmation
    # servoNumber,                          # servo number
    # servoPosition,                        # servo position between 1000 and 2000
    # 0, 0, 0, 0, 0)                        # param 3 ~ 7 not used
    #
    # vehicle.send_mavlink(msg)
    # vehicle.flush()
    print("Servo: " + str(servoNumber) + " set to: " + str(servoPosition))


# Set all servos to closed
servoCommand(6,1000)
servoCommand(7,1000)
servoCommand(8,1000)
print

# Activate servo functions for CDA, WATER, and HABITAT
def CDAdrop():
    servoCommand(6,2000)

def WATERdrop():
    servoCommand(7,2000)

def HABITATdrop():
    servoCommand(8,2000)


# Buttons for
btn = Button(window, text="CDA", command=CDAdrop)
btn.grid(column=0, row=1)


btn = Button(window, text="WATER", command=WATERdrop)
btn.grid(column=2, row=1)


btn = Button(window, text="HABITAT", command=HABITATdrop)
btn.grid(column=4, row=1)


# Close window and vehicle connection function
def saveAndExit():
    window.destroy()
    vehicle.close()


# Make button for closing
btn = Button(window, text="Save and Exit", command=saveAndExit)
btn.grid(column=2, row=3)


# Run forever until destroyed
window.mainloop()
