import datastore

#In order to track position, we need to find differences in time and position over short periods of time
#To accomodate this we need to create lists which store cansat position and orientation over time
#CanSat position will be stored in x and y coordinates (in m) from its starting position
#CanSat orientation will be stored in three values:
#   Tilt angle, degrees from direction of mg
#   x-y orientation relative to N
#   x-y orientation of direction of tilt


trans_pos = [(0,0,0,0)] #translational position, composed of tuples (x,y,time)
or_pos    = [(0,0,0,0)] #orientational position, composed of tuples (tilt, x-y, x-y t, time)

accel_data = ((0,0,0,0),(0,0,0,0))#two accelerometer data points ((xVal, yVal, zVal, time), (...))
mag_data = ((0,0,0,0),(0,0,0,0))#two magnetometer data points

def init_data():
    datastore.get_accelerometer_data(False)    
    datastore.get_magnetometer_data(False)

def get_current_trans_pos():
    return trans_pos[len(trans_pos)-1]
def get_current_or_pos():
    return or_pos[len(or_pos)-1]

def update_raw_data():
    global accel_data,mag_data
    accel_data = datastore.get_accelerometer_diff()
    mag_data   = datastore.get_magnetometer_diff() 
    
def calc_trans_pos():
    update_raw_data()
    global accel_data, mag_data
    #now we need to calculate the difference in accelerometer data
    #can be done by considering reimann sums
    #xDiff = (tnew-told)*(xnew+xold)*0.5
    xDiff = 0.5*(accel_data[1][3]-accel_data[0][3])*(accel_data[1][0]-accel_data[0][0])
    yDiff = 0.5*(accel_data[1][3]-accel_data[0][3])*(accel_data[1][1]-accel_data[0][1])
    zDiff = 0.5*(accel_data[1][3]-accel_data[0][3])*(accel_data[1][2]-accel_data[0][2])
    
    newTime = accel_data[0][3]

    newX = get_current_trans_pos()[0]+xDiff
    newY = get_current_trans_pos()[1]+yDiff
    newZ = get_current_trans_pos()[2]+zDiff
    
    trans_pos.append(newX, newY, newZ, newTime)


def return_current_trans_pos():
    calc_trans_pos()
    return get_current_trans_pos()
