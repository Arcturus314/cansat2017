import smbus
def read_ard():
	smbus = smbus(1)
	global gps_data, ard_err, ard_data
	ard_err = False
	gps_data = []
	try:
		ard_data[i] = smbus.read_byte_data(ard_addr)
	except IOError, err:
                ard_err = True
	if (ard_data[0] == 0x00 && ard_data[1] == 0x00 && ard_data[3] = 0xFF && ard_data[4] = 0xFF):
		try:
			gpsdata[0] = char(ard_data[2])
		
        except ValueError, err:
		ard_err = True
	return none 
	if (ard_data[5] = == 0x00 && ard_data[6] == 0x00 && ard_data[12] = 0xFF && ard_data[13] = 0xFF):
      		try:
			gps_data[1] = ard_data[7]
	except ValueError, err:
		ard_err = True
	return none 
	if (ard_data[14] = == 0x00 && ard_data[15] == 0x00 && ard_data[26] = 0xFF && ard_data[27] = 0xFF):
      		try:
			gps_data[2] = char(ard_data[12])+char(ard_data[13])+char(ard_data[14])+char(ard_data[15])+char(ard_data[16])+char(ard_data[17])+char(ard_data[18])+char(ard_data[19])+char(ard_data[20])+char(ard_data[21])
	except ValueError, err:
		ard_err = True
	return none

	(ard_data[28] = == 0x00 && ard_data[29] == 0x00 && ard_data[40] = 0xFF && ard_data[41] = 0xFF):
      		try:
			gps_data[3] = char(ard_data[26])+char(ard_data[27])+char(ard_data[28])+char(ard_data[29])+char(ard_data[30])+char(ard_data[31])+char(ard_data[32])+char(ard_data[33])+char(ard_data[34])+char(ard_data[35])
	except ValueError, err:
		ard_err = True
	return none
 
	(ard_data[42] = == 0x00 && ard_data[43] == 0x00 && ard_data[54] = 0xFF && ard_data[55] = 0xFF):
      		try:
			gps_data[4] = char(ard_data[40])+char(ard_data[41])+char(ard_data[42])+char(ard_data[43])+char(ard_data[44])+char(ard_data[45])+char(ard_data[46])+char(ard_data[47])+char(ard_data[48])+char(ard_data[49])
	except ValueError, err:
		ard_err = True
	return none

def get_altitude():
	global altitude, gps_data
	altitude = gps_data[4]
	
def get_speed():
	global speed, gps_data
	speed = gps_data[1]

def get_latitude():
	global latitude, gps_data
	latitude = gps_data[2]

def get_longitude():
	global longitude, gps_data
	longitude = gps_data[3]

def get_validity():
	global validity, gps_data
	validity = gps_data[0]


