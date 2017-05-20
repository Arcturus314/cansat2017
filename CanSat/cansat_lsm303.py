#Simple driver file for the LSM303 accelerometer and magnetometer
#Included functionality
#   Return address
#   Return communication status
#   Return magnetometer x, y, z values
#   Return accelerometer x, y, z values
#   Set linear calibration factors for accelerometer and magnetometer values
#   Enable and disable low power sleep functionality

import smbus

#Calibration factors
#of form val_new = (scale)val_old + offset
accel_x_scale = 1
accel_y_scale = 1
accel_z_scale = 1
accel_x_offset = 0
accel_y_offset = 0
accel_z_offset = 0

comp_x_scale = 1
comp_y_scale = 1
comp_z_scale = 1
comp_x_offset = 0
comp_y_offset = 0
comp_z_offset = 0

#Device address
accel_addr_rd = 0x31
accel_addr_wr = 0x30
comp_addr_rd = 0x3D
comp_addr_wr = 0x3C

#Default device parameters
p_mode = True  #True = high power, False = off
u_mode = True  #True = 100Hz, False = 50Hz
d_mode = True  #True = +-8G FSD, False = +-2G FSD

accel_state = True #accelerometer communication state



def init(power, update, deflection):
    global bus
    global accel_state
    try:
        bus = smbus.SMBus(1) #on i2c bus 1

        accel_state = True
    except IOError, err:
        accel_state = False

def getState():
    global accel_state
    return accel_state  
    
def getPower():
    global p_mode
    return p_mode

def getUpdate():
    global u_mode
    return u_mode

def getDefl():
    global d_mode
    return d_mode


