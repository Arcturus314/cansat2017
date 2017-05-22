#simple driver file for the l3gd20 gyroscope

#TODO
#   everything

import smbus

#calibration factors
#of form val_new = (scale)val_old + offset
x_scale = 1
y_scale = 1
z_scale = 1
x_offset = 0
y_offset = 0
z_offset = 0

#device address
l3gd20_addr = 0x6B

#device parameters
p_mode = True #True for normal mode, False for power-down mode
u_mode = True #True for 760Hz update rate, False for 95Hz

#device_state
l3dg20_state = True #true if working communication, false if communication error


