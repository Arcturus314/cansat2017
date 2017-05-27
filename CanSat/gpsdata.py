import smbus
def read_ard():
	smbus = smbus(1)
	global gps_data, ard_err, ard_data
	gps_data = []
	ard_data[i] = smbus.read_byte_data(ard_addr)
	except IOError, err:
                ard_err = True
	gps_data[0]  = chr(ard_data[6])+chr(ard_data[7])+chr(ard_data[8])+chr(ard_data[9])+chr(ard_data[10])+chr(ard_data[11])+chr(ard_data[12])+chr(ard_data[13]) #longitude
        gps_data[1]  = int(str(ard_data[14])) #longitude direction
        gps_data[2]  = chr(ard_data[15])+chr(ard_data[16])+chr(ard_data[17])+chr(ard_data[18])+chr(ard_data[19])+chr(ard_data[20])+chr(ard_data[21])+chr(ard_data[22]) #latitude
        gps_data[3]  = int(str(ard_data[23])) #latitude direction
        gps_data[4]  = chr(ard_data[24])+chr(ard_data[25]) #speed
        gps_data[5]  = int(str(ard_data[26])) #validity

