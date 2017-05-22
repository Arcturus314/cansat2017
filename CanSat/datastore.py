import i2c_sensors

#This class will:
#   Serve to store sensor data values in independent arrays
#   Serve to back up sensor data values to a file
#   Serve to refresh sensor data values
#   Serve to provide overall control over sensor power saving and update modes
#   Serve to track and report sensor status

#Power saving and update:
#Is sorted into several "modes", each for a specific CanSat purpose, optimized for power and performance
#   1) min_power: all sensors at minimum update rates and minimum power
#   2) all_active: all sensors active at max update rates
#   3) envir_log: only humidity, pressure, and temperature sensors active
#   4) track_pos: only GPS, IMU, and barometer active
#   5) heat_map: only sensors required for heat map creation are active

#Sensor | Address | Function
#LSM303 |         | Magnetometer and Accelerometer
#L3GD20 |         | Gyroscope and Temperature
#BME280 |         | Pressure and Humidity and Temperature
#D6T    |         | 4x4 Thermal Camera
#GPS    | via ard | Provides GPS position and velocity information

#File information:
#All sensor data and timestamps will be logged in "sensor_data.txt"


