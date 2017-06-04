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
			gpsdata[0] = ard_data[2]
		
        except ValueError, err:
		ard_err = True
	return none 
	if (ard_data[5] = == 0x00 && ard_data[6] == 0x00 && ard_data[8] = 0xFF && ard_data[9] = 0xFF):
      		try:
			gps_data[1] = ard_data[7]
	except ValueError, err:
		ard_err = True
	return none 
	if (ard_data[10] = == 0x00 && ard_data[11] == 0x00 && ard_data[22] = 0xFF && ard_data[23] = 0xFF):
      		try:
			gps_data[2] = 
	except ValueError, err:
		ard_err = True
	return none

	if 

