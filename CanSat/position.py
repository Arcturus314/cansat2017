import datastore
import math
import bIMU 
import time

#In order to track position, we need to find differences in time and position over short periods of time
#To accomodate this we need to create lists which store cansat position and orientation over time
#CanSat position will be stored in x and y coordinates (in m) from its starting position
#CanSat orientation will be stored in three values:
#   Tilt angle, degrees from direction of mg
#   x-y orientation relative to N
#   x-y orientation of direction of tilt

dtr = 0.0174532925199 #degrees to radians scaling factor

trans_pos = [(0,0,0,0)] #translational position, composed of tuples (x,y,alt,time)
or_pos    = [(0,0,0,0)] #orientational position, composed of tuples (heading,x,y,time)

accel_data = [[0,0,0,0],[0,0,0,0]]#two accelerometer data points ((xVal, yVal, zVal, time), (...))
mag_data = [[0,0,0,0],[0,0,0,0]]#two magnetometer data points
gyro_data = [[0,0,0,0],[0,0,0,0]]#two gyroscope data points

init_position = (0,0,0,0,0,0,0,0) #(heading,x-or,y-or,x,y,alt,temperature,time)

def init_data(): #writes initial calculated vales to init_position tuple
    datastore.get_accelerometer_data(False)    
    datastore.get_magnetometer_data(False)
    datastore.get_gyroscope_data(False)
    update_raw_data()
    calc_bimu_orientation()
    calc_bimu_orientation()
    calc_trans_pos()

    init_position = make_tuple(get_bimu_orientation()[0],get_current_or_pos()[1],get_current_or_pos()[2],get_current_trans_pos()[0],get_current_trans_pos()[1],get_current_env()[1],get_current_env()[0],time.time())

def make_tuple(in_arr): #returns a tuple of length 3 or 4 with the same data as the given array
    #returns a tuple from the first three indices of the given array
    if len(in_arr) == 3:
        return in_arr[0],in_arr[1],in_arr[2]
    if len(in_arr) == 4:
        return in_arr[0],in_arr[1],in_arr[2],in_arr[3]

def get_current_trans_pos(): #returns last element in trans_pos list
    return trans_pos[len(trans_pos)-1]
def get_current_or_pos(): #returns last element in or_pos list
    return or_pos[len(or_pos)-1]
def get_last_or_pos(): #retuns second to last element in or_pos list
    return or_pos[len(or_pos)-2]
def get_current_accel_data(): #returns second accel_data tuple
    return accel_data[1]
def get_current_mag_data(): #returns second mag_data tuple
    return mag_data[1]
def get_current_env(): #returns temp,alt from datastore,subtracting initial altitude
    global init_position
    temperature = datastore.get_env_temp_data(False)
    pressure = datastore.get_env_pressure_data(False)
    altitude = (init_position[3]/-0.0065)*((pressure/101300)**(0.1901)-1)-init_position[6]
    return temperature,altitude
def update_raw_data(): #moves datastore data to raw data lists
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
 
    return None

def calc_bimu_orientation(): #uses bIMU.py module, appends heading, x, y, time to or_pos, subtracting initial orientation, and compensating for heading- standardizing along x and y vectors
    global init_position
    data = bIMU.get_orientation()[0]-init_position[0],bIMU.get_orientation()[1]-init_position[0],bIMU.get_orientation()[2]-init_position[0],time.time()
    or_pos.append(data)

def trap_int(timenew, timeold, valnew, valold): #trapezoidally finds area within given parameters
    #Trapezoidal integration method
     return (timenew-timeold)*(valold)+0.5*(timenew-timeold)*(valnew-valold)

def calc_trans_pos(): #calculates the translational position given accelerometer values, appends to trans_pos
    update_raw_data()
    global accel_data, mag_data, trans_pos

    #We first need to compensate accel_data with current CanSat position
    accel_data_comp = [(0,0,0,0),(0,0,0,0)]
    accel_data_comp[0][3] = accel_data[0][3]
    accel_data_comp[1][3] = accel_data[1][3]

    accel_data_comp[0][0] = (accel_data[0][1]*math.cos(dtr*get_last_or_pos[0])+accel_data[0][0]*math.cos(dtr*(90-get_last_or_pos[0])))*math.sin(dtr*get_last_or_pos[1])
    accel_data_comp[0][1] = (accel_data[0][1]*math.sin(dtr*get_last_or_pos[0])+accel_data[0][0]*math.sin(dtr*(90-get_last_or_pos[0])))*math.sin(dtr*get_last_or_pos[2])

    accel_data_comp[0][0] = (accel_data[0][1]*math.cos(dtr*get_current_or_pos[0])+accel_data[0][0]*math.cos(dtr*(90-get_current_or_pos[0])))*math.sin(dtr*get_current_or_pos[1])
    accel_data_comp[0][1] = (accel_data[0][1]*math.sin(dtr*get_current_or_pos[0])+accel_data[0][0]*math.sin(dtr*(90-get_current_or_pos[0])))*math.sin(dtr*get_current_or_pos[2])

    #now we need to calculate the difference in accelerometer data
    #can be done by considering reimann sums
    #xDiff = (tnew-told)*(xnew+xold)*0.5
    xDiff = trap_int(accel_data_comp[1][3],accel_data_comp[0][3],accel_data_comp[1][0],accel_data_comp[0][0])
    yDiff = trap_int(accel_data_comp[1][3],accel_data_comp[0][3],accel_data_comp[1][1],accel_data_comp[0][1])
    
    newTime = accel_data_comp[0][3]

    newX = get_current_trans_pos()[0]+xDiff
    newY = get_current_trans_pos()[1]+yDiff
    
    trans_pos.append( (newX, newY, get_current_env()[1], newTime) )
def calc_gyro_or(): #calculates the cansat orientation given gyroscope values, appends to or_pos
    update_raw_data()
    global gyro_data
    #This calculation can be done via a similar method
    #to accelerometer translational position calc
    xDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][0],gyro_data[0][0])
    yDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][1],gyro_data[0][1])
    zDiff = trap_int(gyro_data[1][3],gyro_data[0][3],gyro_data[1][2],gyro_data[0][2])
    
    newTime = gyro_data[0][3]

    newX = (get_current_or_pos()[0]+xDiff)%360.0
    newY = (get_current_or_pos()[1]+yDiff)%360.0
    newZ = (get_current_or_pos()[2]+zDiff)%360.0
    
    or_pos.append( (newX, newY, newZ, newTime) )
def calc_accel_or(): #calculates the cansat orientation given accelerometer values, returns pitch and roll
    update_raw_data()
    pitch = math.atan((accel_data[1][0])/(accel_data[1][0]**2+accel_data[1][2]**2))
    roll  = math.atan((accel_data[1][1])/(accel_data[1][1]**2+accel_data[1][2]**2))
    return pitch,roll

def calc_position():
    update_raw_data()
    calc_bimu_orientation()
    calc_trans_pos()

def get_pos_data(all_data):
    if all_data == True:
        return trans_pos,or_pos
    if all_data == False:
        calc_position()
        return get_current_trans_pos(),get_current_or_pos()
