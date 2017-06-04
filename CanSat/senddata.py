import datastore
import gpsdata
import threading
import time

def send_data():
	print ":",
	print 0x00,
	print ",",
	print 0x00,
	print datastore.get_accelerometer_data(False),
	print 0xff,
	print ",",
	print 0xff,
	print ":",
	print 0x01,
	print ",",
	print 0x01,
	print ",",
	print datastore.magnetometer(False),
	print 0xff,
	print ",",
	print 0xff,
	print ":",
	print 0x02,
	print ",",
	print 0x02,
	print ",",
	print datastore.get_gyroscope_data(False),
	print 0xff,
	print ",",
	print 0xff,
	print ":",
	print 0x03,
	print ",",
	print 0x03,
	print ",",
	print datastore.get_env_pressure__data(False),
	print 0xff,
	print ",",
	print 0xff,
	print ":"
	print 0x04,
	print ",",
	print 0x04,
	print datastore.get_env_humidity_data(False),
        print 0xff,
        print ",",
        print 0xff,
        print":"
        print 0x05,
        print ",",
        print 0x05,
        print ",",
        print datastore.get_env_temp_data(False),
        print ",",
        print 0xff,
        print ",",
        print 0xff,
        print":"
        print 0x06,
        print ",",
        print 0x06,
        print ",",
        print datastore.get_temp_array_data(False),
        print ",",
        print 0xff,
        print ",",
        print 0xff,
	print ":"
	print 0x07,
	print ",",
	print 0x07,
	for i in xrange(5):
		print gpsdata.gps_data,
		print ",",
	print 0xff,
	print ",",
	print 0xff
	
t2 = treading.Thread(name ='send_data', target=send_data)
t2.start()

