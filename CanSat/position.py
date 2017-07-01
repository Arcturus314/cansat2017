import datastore
import math
import MadgwickAHRS as bIMU 
import time as exttime
import arduino_interface

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
gps_pos   = [(0,0,0,0,0,0)] #tuples fix,speed,altitude,latitude,longitude,time
accel_data = [[0,0,0,0],[0,0,0,0]]#two accelerometer data points ((xVal, yVal, zVal, time), (...))
mag_data = [[0,0,0,0],[0,0,0,0]]#two magnetometer data points
gyro_data = [[0,0,0,0],[0,0,0,0]]#two gyroscope data points

init_position = (0,0,0,0,0,0,0,0) #(heading,x-or,y-or,x,y,alt,temperature,time)
init_gps_pos  = (0,0,0,0,0,0)       #(fix,altitude,latitude,longitude,x_pos,y_postime)

sample_rate = 10

dec_places = 3

def setTime(timeVal):
    global init_time
    init_time = timeVal

def time():
    return round(exttime.time()-init_time,3)

def init_data(): #writes initial calculated vales to init_position tuple
    global init_position
    global init_gps_pos
    #initializing data
    datastore.get_accelerometer_data(False)    
    datastore.get_magnetometer_data(False)
    datastore.get_gyroscope_data(False)
    update_raw_data()
    calc_bimu_orientation(sample_rate)
    calc_bimu_orientation(sample_rate)
    calc_trans_pos()
    init_position = make_tuple([get_current_or_pos()[0],get_current_or_pos()[1],get_current_or_pos()[2],get_current_trans_pos()[0],get_current_trans_pos()[1],get_current_env()[1],get_current_env()[0],time()])

    #t = exttime.time()
    gps_data = arduino_interface.get_gps_data()
    #print "gps time",
    #print exttime.time()-t
    if gps_data[0] == 1:
        init_gps_pos = gps_data

def make_tuple(in_arr): #returns a tuple of length 3 or 4 with the same data as the given array
    #returns a tuple from the first three indices of the given array
    if len(in_arr) == 3:
        return in_arr[0],in_arr[1],in_arr[2]
    if len(in_arr) == 4:
        return in_arr[0],in_arr[1],in_arr[2],in_arr[3]
    if len(in_arr) == 8:
        return in_arr[0],in_arr[1],in_arr[2],in_arr[3],in_arr[4],in_arr[5],in_arr[6],in_arr[7]

def get_current_trans_pos(): #returns last element in trans_pos list
    return trans_pos[len(trans_pos)-1]
def get_current_or_pos(): #returns last element in or_pos list
    return or_pos[len(or_pos)-1]
def get_current_gps_pos():
    return gps_pos[len(gps_pos)-1]
def get_last_or_pos(): #retuns second to last element in or_pos list
    return or_pos[len(or_pos)-2]
def get_current_accel_data(): #returns second accel_data tuple
    return accel_data[1]
def get_current_mag_data(): #returns second mag_data tuple
    return mag_data[1]
def get_current_env(): #returns temp,alt from datastore,subtracting initial altitude
    temperature = datastore.get_env_temp_data(False)[0]
    pressure = datastore.get_env_pressure_data(False)[0]
    altitude = (1.0-((pressure/1013.25)**(0.190284)))*44307.69396-init_position[5]
    return round(temperature,dec_places),round(altitude,dec_places)
def update_raw_data(): #moves datastore data to raw data lists
    global accel_data,mag_data,gyro_data
    #x-y-z according to the IMU will differ from x-y-z according to the module.
    #Here x-y-z will be converted to module orientation, with:
    #   xpos: towards front of module, viewed from top
    #   ypos: towards right of module, viewed from top
    #   zpos: towards top of module

    get_accelerometer_diff = datastore.get_accelerometer_diff()
    get_magnetometer_diff = datastore.get_magnetometer_diff()
    get_gyroscope_diff = datastore.get_gyroscope_diff()

    for i in xrange(2):
        accel_data[i][0] = -1*get_accelerometer_diff[i][2] #x
        accel_data[i][1] = -1*get_accelerometer_diff[i][0] #y 
        accel_data[i][2] = get_accelerometer_diff[i][1] #z
        accel_data[i][3] = get_accelerometer_diff[i][3] #time

        mag_data[i][0]   = -1*get_magnetometer_diff[i][2]
        mag_data[i][1]   = -1*get_magnetometer_diff[i][0]
        mag_data[i][2]   = get_magnetometer_diff[i][1]
        mag_data[i][3]   = get_magnetometer_diff[i][3]

        gyro_data[i][0]   = -1*get_gyroscope_diff[i][2]
        gyro_data[i][1]   = -1*get_gyroscope_diff[i][0]
        gyro_data[i][2]   = get_gyroscope_diff[i][1]
        gyro_data[i][3]   = get_gyroscope_diff[i][3]
 
    return None

def calc_bimu_orientation(sample): #uses bIMU.py module, appends heading, x, y, time to or_pos, subtracting initial orientation, and compensating for heading- standardizing along x and y vectors
    global init_position
    global or_pos
    bIMU_data = bIMU.get_orientation(sample)
    #data = round(bIMU_data[0]-init_position[0],dec_places),round(bIMU_data[1]-init_position[0],dec_places),round(bIMU_data[2]-init_position[0],dec_places),time()
    data = round(bIMU_data[0],dec_places),round(bIMU_data[1],dec_places),round(bIMU_data[2],dec_places),time()
    or_pos.append(data)

def trap_int(timenew, timeold, valnew, valold): #trapezoidally finds area within given parameters
    #Trapezoidal integration method
     return (timenew-timeold)*(valold)+0.5*(timenew-timeold)*(valnew-valold)

def calc_trans_pos(): #calculates the translational position given accelerometer values, appends to trans_pos
    global accel_data, mag_data, trans_pos

    #We first need to compensate accel_data with current CanSat position
    accel_data_comp = [[0,0,0,0],[0,0,0,0]]
    accel_data_comp[0][3] = accel_data[0][3]
    accel_data_comp[1][3] = accel_data[1][3]

    accel_data_comp[0][0] = (accel_data[0][1]*math.cos(dtr*get_last_or_pos()[0])+accel_data[0][0]*math.cos(dtr*(90-get_last_or_pos()[0])))*math.sin(dtr*get_last_or_pos()[1])
    accel_data_comp[0][1] = (accel_data[0][1]*math.sin(dtr*get_last_or_pos()[0])+accel_data[0][0]*math.sin(dtr*(90-get_last_or_pos()[0])))*math.sin(dtr*get_last_or_pos()[2])

    accel_data_comp[0][0] = (accel_data[0][1]*math.cos(dtr*get_current_or_pos()[0])+accel_data[0][0]*math.cos(dtr*(90-get_current_or_pos()[0])))*math.sin(dtr*get_current_or_pos()[1])
    accel_data_comp[0][1] = (accel_data[0][1]*math.sin(dtr*get_current_or_pos()[0])+accel_data[0][0]*math.sin(dtr*(90-get_current_or_pos()[0])))*math.sin(dtr*get_current_or_pos()[2])

    #now we need to calculate the difference in accelerometer data
    #can be done by considering reimann sums
    #xDiff = (tnew-told)*(xnew+xold)*0.5
    xDiff = trap_int(accel_data_comp[1][3],accel_data_comp[0][3],accel_data_comp[1][0],accel_data_comp[0][0])
    yDiff = trap_int(accel_data_comp[1][3],accel_data_comp[0][3],accel_data_comp[1][1],accel_data_comp[0][1])
    
    newTime = accel_data_comp[0][3]

    newX = get_current_trans_pos()[0]+xDiff
    newY = get_current_trans_pos()[1]+yDiff
    

    #We still have to consider gps data in order to bound the calculated accelerometer position
    #t = exttime.time()
    gps_data = arduino_interface.get_gps_data()
    #print "gps time",
    #print exttime.time()-t
    gps_pos.append(gps_data)
    if init_gps_pos[0] == 0 and gps_data[0] == 1:
        init_gps_pos[0] = gps_data[0]
        init_gps_pos[1] = gps_data[2]
        init_gps_pos[2] = gps_data[3]
        init_gps_pos[3] = newX 
        init_gps_pos[4] = newY 
        init_gps_pos[5] = gps_data[4]
    if init_gps_pos[0] == 1 and gps_data[0] == 1:
        #This means that we have a valid GPS lock
        #Now we can calculate Dx and Dy from initial GPS lock 
        lat_mid = (init_gps_pos[2]+gps_data[3])/2.0
        m_per_deg_lat = 111132.954 - 559.822 * math.cos( 2 * lat_mid ) + 1.175 * cos( 4 * latMid)
        m_per_deg_lon = 111132.954 * math.cos ( lat_mid )

        #We need to assume a certain level of precision in our gps readings.
        #I will assime GPS values are accurate +- 5m along x and y axes
        new_gps_x_pos = init_gps_pos[3]+m_per_deg_lon*(gps_data[4]-init_gps_pos[3])
        new_gps_y_pos = init_gps_pos[4]+m_per_deg_lat*(gps_data[3]-init_gps_pos[2])

        gps_x_bounds = [new_gps_x_pos-5.0,new_gps_x_pos+5.0]
        gps_y_bounds = [new_gps_y_pos-5.0,new_gps_y_pos+5.0]

        if not (newX < gps_x_bounds[1] and newX > gps_x_bounds[0]):
            if newX > new_gps_x_pos: 
                newX = gps_x_bounds[1]
            if newX < new_gps_x_pos:
                newX = gps_x_bounds[0]

        if not (newY < gps_y_bounds[1] and newY > gps_y_bounds[0]):
            if newY > new_gps_y_pos: 
                newY = gps_y_bounds[1]
            if newY < new_gps_y_pos:
                newY = gps_y_bounds[0]

    trans_pos.append( (round(newX,dec_places), round(newY,dec_places), round(get_current_env()[1],dec_places), newTime) )

def calc_gyro_or(): #calculates the cansat orientation given gyroscope values, appends to or_pos
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
    
    or_pos.append( (round(newX,dec_places), round(newY,dec_places), round(newZ,dec_places), newTime) )
def calc_accel_or(): #calculates the cansat orientation given accelerometer values, returns pitch and roll
    pitch = math.atan((accel_data[1][0])/(accel_data[1][0]**2+accel_data[1][2]**2))
    roll  = math.atan((accel_data[1][1])/(accel_data[1][1]**2+accel_data[1][2]**2))
    return round(pitch,dec_places),round(roll,dec_places)

def calc_position():
    global sample_rate
    t1 = exttime.time()
    #t = exttime.time()
    update_raw_data()
    #print "update raw data",
    #print exttime.time()-t
    #t = exttime.time()
    calc_bimu_orientation(sample_rate)
    #print "calc bimu orientation",
    #print exttime.time()-t
    #t = exttime.time()
    calc_trans_pos()
    #print "calc trans pos",
    #print exttime.time()-t
    #t = exttime.time()
    t2 = exttime.time()
    sample_rate = 1.0/(t2-t1)

def get_pos_data(all_data):
    if all_data == True:
        return trans_pos,or_pos,gps_pos
    if all_data == False:
        calc_position()
        return get_current_trans_pos(),get_current_or_pos(),get_current_gps_pos()
