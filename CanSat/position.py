import datastore
import math
import fusion

#In order to track position, we need to find differences in time and position over short periods of time
#To accomodate this we need to create lists which store cansat position and orientation over time
#CanSat position will be stored in x and y coordinates (in m) from its starting position
#CanSat orientation will be stored in three values:
#   Tilt angle, degrees from direction of mg
#   x-y orientation relative to N
#   x-y orientation of direction of tilt


trans_pos = [(0,0,0,0)] #translational position, composed of tuples (x,y,time)
or_pos    = [(0,0,0,0)] #orientational position, composed of tuples (tilt, x-y, x-y t, time)

accel_data = [[0,0,0,0],[0,0,0,0]]#two accelerometer data points ((xVal, yVal, zVal, time), (...))
mag_data = [[0,0,0,0],[0,0,0,0]]#two magnetometer data points
gyro_data = [[0,0,0,0],[0,0,0,0]]#two gyroscope data points

motion_track = fusion.Fusion()

def init_data():
    datastore.get_accelerometer_data(False)    
    datastore.get_magnetometer_data(False)
    datastore.get_gyroscope_data(False)
def make_tuple(in_arr):
    #returns a tuple from the first three indices of the given array
    return in_arr[0],in_arr[1],in_arr[2]

def get_current_trans_pos():
    return trans_pos[len(trans_pos)-1]
def get_current_or_pos():
    return or_pos[len(or_pos)-1]
def get_current_accel_data():
    return accel_data[1]
def get_current_mag_data():
    return mag_data[1]
def update_raw_data():
    global accel_data,mag_data,gyro_data
    #x-y-z according to the IMU will differ from x-y-z according to the module.
    #Here x-y-z will be converted to module orientation, with:
    #   xpos: towards front of module, viewed from top
    #   ypos: towards right of module, viewed from top
    #   zpos: towards top of module
    for i in xrange(2):
        accel_data[i][0] = -1*datastore.get_accelerometer_diff()[i][2] #x
        accel_data[i][1] = -1*datastore.get_accelerometer_diff()[i][0] #y 
        accel_data[i][2] = datastore.get_accelerometer_diff()[i][1] #z
        accel_data[i][3] = datastore.get_accelerometer_diff()[i][3] #time

        mag_data[i][0]   = -1*datastore.get_magnetometer_diff()[i][2]
        mag_data[i][1]   = -1*datastore.get_magnetometer_diff()[i][0]
        mag_data[i][2]   = datastore.get_magnetometer_diff()[i][1]
        mag_data[i][3]   = datastore.get_magnetometer_diff()[i][3]

        gyro_data[i][0]   = -1*datastore.get_gyroscope_diff()[i][2]
        gyro_data[i][1]   = -1*datastore.get_gyroscope_diff()[i][0]
        gyro_data[i][2]   = datastore.get_gyroscope_diff()[i][1]
        gyro_data[i][3]   = datastore.get_gyroscope_diff()[i][3]

    motion_track.update(make_tuple(accel_data[1]),make_tuple(gyro_data[1]),make_tuple(mag_data[1]))
    return None

def trap_int(timenew, timeold, valnew, valold):
    #Trapezoidal integration method
     return (timenew-timeold)*(valold)+0.5*(timenew-timeold)*(valnew-valold)

def calc_trans_pos():
    update_raw_data()
    global accel_data, mag_data, trans_pos
    #now we need to calculate the difference in accelerometer data
    #can be done by considering reimann sums
    #xDiff = (tnew-told)*(xnew+xold)*0.5
    xDiff = trap_int(accel_data[1][3],accel_data[0][3],accel_data[1][0],accel_data[0][0])
    yDiff = trap_int(accel_data[1][3],accel_data[0][3],accel_data[1][1],accel_data[0][1])
    zDiff = trap_int(accel_data[1][3],accel_data[0][3],accel_data[1][2],accel_data[0][2])
    
    newTime = accel_data[0][3]

    newX = get_current_trans_pos()[0]+xDiff
    newY = get_current_trans_pos()[1]+yDiff
    newZ = get_current_trans_pos()[2]+zDiff
    
    trans_pos.append( (newX, newY, newZ, newTime) )
def calc_gyro_or():
    update_raw_data()
    global gyro_data
    #This calculation can be done via a similar method
    #to accelerometer translational position calc
    xDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][0],gyro_data[0][0])
    yDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][1],gyro_data[0][1])
    zDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][2],gyro_data[0][2])
    
    newTime = gyro_data[0][3]

    newX = get_current_or_pos()[0]+xDiff
    newY = get_current_or_pos()[1]+yDiff
    newZ = get_current_or_pos()[2]+zDiff
    
    or_pos.append( (newX, newY, newZ, newTime) )
def calc_accel_or():
    update_raw_data()
    pitch = math.atan((accel_data[1][0])/(accel_data[1][0]**2+accel_data[1][2]**2))
    roll  = math.atan((accel_data[1][1])/(accel_data[1][1]**2+accel_data[1][2]**2))
    return pitch,roll

def return_current_trans_pos():
    calc_trans_pos()
    return get_current_trans_pos()
def return_current_or_pos():
    calc_gyro_or()
    return get_current_or_pos()

def get_orientation():
    update_raw_data()
    return motion_track.heading, motion_track.pitch, motion_track.roll

