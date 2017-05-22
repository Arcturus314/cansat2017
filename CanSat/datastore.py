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
data_fileName  = "sensor_data.txt"
error_fileName = "error_data.txt"

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

#general file handling methods
def report_error(sensor):
    file = open(error_fileName, "a")
    file.write(sensor)
    file.write(str(time.time()))
    file.write('\n')
    file.close()

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
    if status = False:
        report_error("accelerometer")
def get_accelerometer_settings(): #(power, update, deflection)
    global accelerometer
    return accelerometer.getPower(),accelerometer.getUpdate(),accelerometer.getDefl()
def get_magnetometer_status():
    global magnetometer
    status = magnetometer.getState()
    if status = False:
        report_error("magnetometer")
def get_magnetometer_settings():
    global magnetometer
    return magnetometer.getPower(),magnetometer.getUpdate(),magnetometer.getDefl()
def get_gyroscope_status():
    global gyroscope
    status = gyroscope.getState()
    if status = False:
        report_error("gyroscope") 
def get_gyroscope_settings():
    global gyroscope
    return gyroscope.getPower(),gyroscope.getUpdate(),gyroscope.getDefl()
def get_env_status
    global env_pressure
    status = env_pressure.getState()
    if status = False:
        report_error("BME280")
def get_temp_camera_status
    global temp_camera
    status = temp_camera.getStatus()
    if status = False:
        report_error("D6T")


