import datastore
def checksum_function():
global sumt1, sumt2, sumt3, sumt4, sumt5	
	sumt1 = 0
	sumt2 = 0
	sumt3 = 0
	sumt4 = 0
	sumt5 = 0
	sumt1 = get_accelerometer_data(False) / 5
	sumt2 = get_magnetometer_data(False) / 5
	sumt3 = get_gyroscope_data(False) / 6
	sumt4 = ( get_env_pressure_data(False) + get_env_humidity_data(False) + get_env_temp_data(False)) / 7
	sumt5 = get_temp_array_data(False) / 17
