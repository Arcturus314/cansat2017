import datastore
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
