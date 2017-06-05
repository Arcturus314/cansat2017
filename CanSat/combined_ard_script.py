import datastore
import smbus
import senddata

def error_status():
global xbee_err, l3gd20_err, lsm303_err, bme280_err, d6t_err
xbee_err = 0x00	
l3gd20_err = 0x00
lsm303_err = 0x00
bme280_err = 0x00
d6t_err = 0x00
	if comm_err = true:
		xbee_err = xbee_err|0x01
	if datastore.get_errors()[0] = true:
		lsm303_err = lsm303_err|0x02
	if datastore.get_errors()[1] = true:
		lsm303_err = lsm303_err|0x03
	if datastore.get_errors()[2] = true:
		l3gd20_err = l3gd20_err|0x04
	if datastore.get_errors()[3] = true:
		bme280_err= bme280_err|0x05
	if datastore.get_errors()[4] = true:
		d6t_err = d6t_err|0x06

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
			gps_data[2] = char(ard_data[12])+char(ard_data[13])+char(ard_data[14])+char(ard_data[15])+char(ard_data[16])+char(ard_data[17])+char(ard_data[18])+char(ard_data[19])+char(ard_data[20])+char(ard_data[21])
	except ValueError, err:
		ard_err = True
	return none

	(ard_data[24] = == 0x00 && ard_data[25] == 0x00 && ard_data[36] = 0xFF && ard_data[37] = 0xFF):
      		try:
			gps_data[3] = char(ard_data[26])+char(ard_data[27])+char(ard_data[28])+char(ard_data[29])+char(ard_data[30])+char(ard_data[31])+char(ard_data[32])+char(ard_data[33])+char(ard_data[34])+char(ard_data[35])
	except ValueError, err:
		ard_err = True
	return none
 
	(ard_data[38] = == 0x00 && ard_data[39] == 0x00 && ard_data[50] = 0xFF && ard_data[51] = 0xFF):
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

