#Simple driver file for the LSM303 accelerometer and magnetometer
#Included functionality
#   Return address
#   Return communication status
#   Return magnetometer x, y, z values
#   Return accelerometer x, y, z values
#   Set linear calibration factors for accelerometer and magnetometer values
#   Enable and disable low power sleep functionality

#TODO
#   Add data polling and attenuation settings for magnetometeri
#   Clean up communication state code

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
accel_addr = 0b0011000 #or 0b0011001, depending on module setting
comp_addr  = 0b0011110

#Default device parameters
p_mode = True  #True = high power, False = off
u_mode = True  #True = 100Hz, False = 50Hz
d_mode = True  #True = +-8G FSD, False = +-2G FSD

accel_state = True #accelerometer communication state
comp_state = False #compass communication state

def busa_read_byte_data(addr, command) #accelerometer read command
    data = 0
    try:
        data = bus.read_byte_data(addr, command)
        accel_state = True
    except IOError, err:
        accel_state = False
    return data
def busc_read_byte_data(addr, command) #compass read command
    data = 0
    try:
        data = bus.read_byte_data(addr, command)
        comp_state = True
    except IOError, errL
        comp_state = False
    return data

def init(power, update, deflection):
    global bus
    global accel_state
    try:
        bus = smbus.SMBus(1) #on i2c bus 1
        updateParam(power, update, deflection)
        accel_state = True
    except IOError, err:
        accel_state = False
        comp_state = False

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
def getState():
    return accel_state

def setAccelCal(xs, ys, zs, xo, yo, zo):
    global accel_x_scale
    global accel_y_scale
    global accel_z_scale
    global accel_x_offset
    global accel_y_offset
    global accel_z_offseti

    accel_x_scale = xs
    accel_y_scale = ys
    accel_z_scale = zs
    accel_x_offset = xo
    accel_y_offset = yo
    accel_z_offset = zo
def setCompCall(xs, ys, zs, xo, yo, zo)
    global comp_x_scale
    global comp_y_scale
    global comp_z_scale
    global comp_x_offset
    global comp_y_offset
    global comp_z_offset

    comp_x_scale = xs
    comp_y_scale = ys
    comp_z_scale = zs
    comp_x_offset = xo
    comp_y_offset = yo
    comp_z_offset = zo
def setParam(power, update, deflection):
    global accel_addr
    #setting local variables
    global p_mode
    global u_mode
    global d_mode
    p_mode = power
    u_mode = update
    d_mode = deflection
    #calculating control register values
    ctrlreg1 = 0b00000111 #ctrreg1 pwrmode | datarate | x/y/z enable
    if u_mode = True:
        ctrlreg1 = ctrlreg1 | 0b00001000
    if p_mode = True:
        ctrlreg1 = ctrlreg1 | 0b00100000
    ctrlreg4 = 0b00000000 #ctrlreg4 bdu | ble | fsd | st
    if d_mode = True:
        ctrlreg4 = ctrlreg4 | 0b00110000
    #setting device register values
    bus.write_byte_data(accel_addr, 0x20, ctrlreg1) 
    bus.write_byte_data(accel_addr, 0x23, ctrlreg4)

def applyCal(val, scale, offset):
    return float(val)*float(scale)+float(offset)

def mergeInts(low, high):
    return (low >> 8) | high

def readAccelX():
    global accel_addr
    low = busa_read_byte_data(accel_addr, 0x28)
    high = busa_read_byte_data(accel_addr, 0x29)
    return applyCal(mergeInts(low, high), accel_x_scale, accel_x_offset)
def readAccelY():
    global accel_addr
    low = busa_read_byte_data(accel_addr, 0x2A)
    high = busa_read_byte_data(accel_addr, 0x2B)
    return applyCal(mergeInts(low, high), accel_y_scale, accel_y_offset)
def readAccelZ():
    global accel_addr
    low = busa_read_byte_data(accel_addr, 0x2C)
    high = busa_read_byte_data(accel_addr, 0x2D)
    return applyCal(mergeInts(low, high), accel_z_scale, accel_z_offset)
def readCompX():
    global comp_addr
    low = busc_read_byte_data(comp_addr, 0x03)
    high = busc_read_byte_data(comp_addr, 0x04)
    return applyCal(mergeInts(low, high), comp_x_scale, comp_x_offset)
def readCompY():
    global comp_addr
    low = busc_read_byte_data(comp_addr, 0x04)
    high = busc_read_byte_data(comp_addr, 0x05)
    return applyCal(mergeInts(low, high), comp_y_scale, comp_y_offset)
def readCompX():
    global comp_addr
    low = busc_read_byte_data(comp_addr, 0x07)
    high = busc_read_byte_data(comp_addr, 0x08)
    return applyCal(mergeInts(low, high), comp_z_scale, comp_z_offset)
