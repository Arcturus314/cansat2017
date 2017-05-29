import time
import i2c_sensors

#This class will:
#   Serve to store sensor data values in independent arrays
#   Serve to back up sensor data values to a file
#   Serve to refresh sensor data values
#   Serve to provide overall control over sensor power saving and update modes
#   Serve to track and report sensor status
#   Serve to report sensor errors to a file

#Power saving and update:
#Is sorted into several "modes", each for a specific CanSat purpose, optimized for power and performance
#   1) min_power: all sensors at minimum update rates and minimum power
#   2) all_active: all sensors active at max update rates
#   3) envir_log: only humidity, pressure, and temperature sensors active
#   4) track_pos: only GPS, IMU, and barometer active
#   5) heat_map: only sensors required for heat map creation are active

#Sensor |  Comms  | Function
#LSM303 |   I2C   | Magnetometer and Accelerometer
#L3GD20 |   I2C   | Gyroscope and Temperature
#BME280 |   I2C   | Pressure and Humidity and Temperature
#D6T    |   I2C   | 4x4 Thermal Camera
#GPS    | via ard | Provides GPS position and velocity information

#File information:
#All sensor data and timestamps will be logged in "sensor_data.txt"
#All sensor errors and timestamps will be logged in "sensor_error.txt"
#All temperature matrix data will be logged in "temp_data.txt"
data_fileName  = "sensor_data.txt"
error_fileName = "error_data.txt"
temp_fileName  = "temp_data.txt"

#Sensor data lists
accel_data      = [] #{[X1, Y1, Z1, Time1], [X2, Y2, Z2, Time2] ...}
mag_data        = [] #{[X1, Y1, Z1, Time1], [X2, Y2, Z2, Time2] ...}
gyro_data       = [] #{[X1, Y1, Z1, Time1], [X2, Y2, Z2, Time2] ...}
gyro_temp_data  = [] #{[Temp1, Time1], [Temp2, Time2] ...}
pressure_data   = [] #{[P1, Time1], [P2, Time2] ...}
humidity_data   = [] #{[H1, Time1], [H2, Time2] ...}
pres_temp_data  = [] #{[Temp1, Time1], [Temp2, Time2] ...}
temp_array_data = [] #{[ [temp_arr]1, Time1], [ [temp_arr]2, Time2] ...}
temp_ref_data   = [] #{[Temp1, Time1], [Temp2, Time2] ...}

#Sensor I2C addresses
LSM303_accel_addr = 0b0011001 #Can be 0b0011001 OR 0b0011000 depending on wiring
LSM303_mag_addr   = 0b0011110
L3GD20_addr       = 0b1101011 #Can be 0b1101011 OR 0b1101010 depending on wiring
BME280_addr       = 0x77      #Can be 0x77 OR 0x76 depending on wiring
D6T_addr          = 0x0A

#Sensor class imports with power mode 1
accelerometer = i2c_sensors.LSM303_Accel(LSM303_accel_addr, True, True, True)
magnetometer  = i2c_sensors.LSM303_Mag(LSM303_mag_addr, True, True, True)
gyroscope     = i2c_sensors.L3GD20_Gyro(L3GD20_addr, True, True, True)
imu_temp      = i2c_sensors.L3GD20_Temp(L3GD20_addr)
env_pressure  = i2c_sensors.BME280_Pressure(BME280_addr)
env_humidity  = i2c_sensors.BME280_Humidity(BME280_addr)
env_temp      = i2c_sensors.BME280_Temp(BME280_addr)
temp_camera   = i2c_sensors.D6T_Temp_Array(D6T_addr)

#File instantiation
data_file_error  = False #True when file cannot be opened
error_file_error = False #True when file cannot be opened
temp_file_error  = False #True when file cannot be opened
try:
    file = open(data_fileName, "a")
    file.close()
    data_file_error = False 
except IOError, err:
    data_file_error = True

try:
    file = open(error_fileName, "a")
    file.close()
    error_file_error = False
except IOError, err:
    error_file_error = True

try:
    file = open(temp_fileName, "a")
    file.close()
    temp_file_error = False
except IOError, err:
    temp_file_error = True

#general functions
def getTuple(a,b,c):
    return a,b,c

#general file handling methods
def report_error(sensor):
    global error_file_error, error_fileName
    try:
        file = open(error_fileName, "a")
        file.write(sensor)
        file.write(",")
        file.write(str(time.time()))
        file.write('\n')
        file.close()
        error_file_error = False
    except IOError, err:
        error_file_error = True 
def add_data(sensor, data):
    global data_file_error, data_fileName
    try:
        file = open(data_fileName, "a")
        file.write(sensor)
        file.write(",")
        file.write(str(data))
        file.write(",")
        file.write(str(time.time()))
        file.write('\n')
        file.close()
    except IOError, err:
        data_file_error = True
def add_data_3ax(sensor, dataX, dataY, dataZ):
    global data_file_error, data_fileName
    try:
        file = open(data_fileName, "a")
        file.write(sensor)
        file.write(",")
        file.write(str(dataX))
        file.write(",")
        file.write(str(dataY))
        file.write(",")
        file.write(str(dataZ))
        file.write(",")
        file.write(str(time.time()))
        file.write('\n')
        file.close()
    except IOError, err:
        data_file_error = True
def add_temp_matrix(data):
    global temp_file_error, temp_fileName
    try:
        file = open(temp_fileName, "a")
        for i in xrange(15):
            file.write(str(data[0][i]))
            file.write(",")
        file.write(str(data[1]))
        file.write('\n')
        file.close()
    except IOError, err:
        temp_file_error = True
        
#general get methods
def get_data_file_status():
    global data_file_error
    return data_file_error
def get_error_file_status():
    global error_file_error
    return error_file_error

def get_accelerometer_status():
    global accelerometer
    status = accelerometer.getState()
    if status == False:
        report_error("accelerometer")
    return status
def get_accelerometer_settings(): #(power, update, deflection)
    global accelerometer
    return accelerometer.getPower(),accelerometer.getUpdate(),accelerometer.getDefl()
def get_magnetometer_status():
    global magnetometer
    status = magnetometer.getState()
    if status == False:
        report_error("magnetometer")
    return status
def get_magnetometer_settings():
    global magnetometer
    return magnetometer.getPower(),magnetometer.getUpdate(),magnetometer.getDefl()
def get_gyroscope_status():
    global gyroscope
    status = gyroscope.getState()
    if status == False:
        report_error("gyroscope") 
    return status
def get_gyroscope_settings():
    global gyroscope
    return gyroscope.getPower(),gyroscope.getUpdate(),gyroscope.getDefl()
def get_env_status():
    global env_pressure
    status = env_pressure.getState()
    if status == False:
        report_error("BME280")
    return status
def get_temp_camera_status():
    global temp_camera
    status = temp_camera.getState()
    if status == False:
        report_error("D6T")
    return status

#sensor set methods
def set_accelerometer_settings(power,update,deflection):
    global accelerometer
    if getTuple(power,update,deflection) != get_accelerometer_settings():
        accelerometer.setParam(power,update,deflection)
def set_magnetometer_settings(power,update,deflection):
    global magnetometer
    if getTuple(power,update,deflection) != get_magnetometer_settings():
        magnetometer.setParam(power,update,deflection)
def set_gyroscope_settings(power,update,deflection):
    global gyroscope
    if getTuple(power,update,deflection) != get_gyroscope_settings():
        gyroscope.setParam(power,update,deflection)

#sensor value get methods (TRUE for all data, FALSE for only last data point)
def get_accelerometer_data(data):
    global accel_data
    global accelerometer
    xVal = accelerometer.readX()
    yVal = accelerometer.readY()
    zVal = accelerometer.readZ()
    accel_data.append([xVal, yVal, zVal, time.time()])
    add_data_3ax("accelerometer", xVal, yVal, zVal)
    if data == True:
        return accel_data
    return xVal, yVal, zVal, time.time()
def get_magnetometer_data(data):
    global magnetometer
    global mag_data
    xVal = magnetometer.readX()
    yVal = magnetometer.readY()
    zVal = magnetometer.readZ()
    mag_data.append([xVal,yVal,zVal,time.time()])
    add_data_3ax("magnetometer", xVal, yVal, zVal)
    if data == True:
        return mag_data
    return xVal, yVal, zVal, time.time()
def get_gyroscope_data(data):
    global gyroscope
    global gyro_data
    xVal = gyroscope.readX()
    yVal = gyroscope.readY()
    zVal = gyroscope.readZ()
    gyro_data.append([xVal,yVal,zVal,time.time()])
    add_data_3ax("accelerometer", xVal, yVal, zVal)
    if data == True:
        return gyro_data
    return xVal, yVal, zVal, time.time()
def get_imu_temp_data(data):
    global imu_temp
    global gyro_temp_data
    val = imu_temp.read()
    gyro_temp_data.append([val, time.time()])
    add_data("imu_temp", val)
    if data == True:
        return gyro_temp_data
    return val, time.time()
def get_env_pressure_data(data):
    global env_pressure
    global pressure_data
    val = env_pressure.read()
    pressure_data.append([val, time.time()])
    add_data("pressure", val)
    if data == True:
        return pressure_data
    return val, time.time()
def get_env_humidity_data(data):
    global env_humidity
    global humidity_data
    val = env_humidity.read()
    humidity_data.append([val, time.time()])
    add_data("humidity", val)
    if data == True:
        return humidity_data
    return val, time.time()
def get_env_temp_data(data):
    global env_temp
    global pres_temp_data
    val = env_temp.read()
    pres_temp_data.append([val, time.time()])
    add_data("env_temp", val)
    if data == True:
        return pres_temp_data
    return val, time.time()
def get_temp_array_data(data):
    global temp_camera
    global temp_array_data
    val = temp_camera.read()
    temp_array_data.append([val, time.time()])
    add_temp_matrix(val)
    if data == True:
        return temp_array_data
    return val,time.time()

#overall control and read methods
def read_all_active(): #accel, mag, gyro, imu_temp, pres, hum, temp, tarr
    all_val = get_accelerometer_data(False)[0:2],get_magnetometer_data(False)[0:2],get_gyroscope_data(False)[0:2],get_imu_temp_data(False)[0],get_env_pressure_data(False)[0],get_env_humidity_data(False)[0],get_env_temp_data(False),get_temp_array_data(False)[0],time.time()
    return all_val
def read_envir_log(): #env_temp, pressure, humidity 
    env_data = get_env_temp_data(False)[0], get_env_pressure_data(False)[0], get-env_humidity_data(False)[0], time.time()
    return env_data
def read_track_pos(): #pressure, accelerometer, magnetometer, gyroscope
    pos_data = get_env_pressure_data(False)[0],get_accelerometer_data(False)[0:2], get_magnetometer_data(False)[0:2], time.time()
    return pos_data
def read_heat_map(): #pressure, accelerometer, magnetometer, gyroscope, tarr
    heat_map_data = get_env_pressure_data(False)[0],get_accelerometer_data(False)[0:2], get_magnetometer_data(False)[0:2],get_temp_array_data(False)[0],time.time()
    return heat_map_data

def get_errors(): #accelerometer, magnetometer, gyroscope, env, temp_camera
    errors = get_accelerometer_status(),get_magnetometer_status(),get_gyroscope_status(),get_env_status(),get_temp_camera_status()
    return errors

def set_min_power():
    set_accelerometer_settings(False, False, False)
    set_gyroscope_settings(False, False, False)
    set_magnetometer_settings(False, False, False)
def set_all_active():
    set_accelerometer_settings(True,True,True)
    set_gyroscope_settings(True,True,True)
    set_magnetometer_settings(True,True,True)
def set_envir_log():
    set_min_power()
def set_track_pos():
    set_all_active()
def set_heat_map():
    set_all_active()

