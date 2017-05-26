import datastore
declare checksum_function();
global sumt1, sumt2, sumt3, sumt4, sumt5	
	sumt1 = 0
	sumt2 = 0
	sumt3 = 0
	sumt4 = 0
	sumt5 = 0
	sumt1 = accel_data / 5
	sumt2 = mag_data / 5
	sumt3 = gyro_data / 6
	sumt4 = ( pressure_data + humidity_data + pres_temp_data) / 7
	sumt5 = temp_array_data / 17
