import smbus
import time
bus = smbus.SMBus(1) #starting smbus on hardware bus 1
ard_addr = 75 #Arduino i2c address is 75. Coincidentally, this is also the ascii code for the first letter of my first name

#The arduino transmits data to the cansat as a series of characters in this order:
#:(fix),(speed),(altitude),(latitude),(longitude):

ard_status = False
ard_file_name = "ard_data.txt"
ard_file_error = False #True when there is an arduino data logging file related error

def add_data(data):
    try:
        file = open(ard_file_name, "a")
        file.write(str(data))
        file.write('\n')
        file.close()
        ard_file_error = False
    except IOError, err:
        ard_file_error = True


def read_byte():
    global ard_status
    data = 0
    try:
        print "reading ard byte"
        data = bus.read_byte(ard_addr)
        ard_status = True
    except IOError, err:
        ard_status = False
    return data

def read_arduino(): #returns list [fix,speed,altitude,latitude,longitude]
    print "read_arduino"
    global ard_status
    gps_data = ["","","","",""]
    gps_data_ints = [0,0,0,0,0]
    try:
        in_char = ' '
        while in_char != ':' and ard_status == True:
            in_char = read_byte()
        for i in xrange(5):
            while in_char != ',':
                in_char = read_byte()
                gps_data[i].append(read_byte())
        for i in xrange(5):
            gps_data_ints[i] = int(gps_data[i])
        ard_status = True
    except IOError, err:
        ard_status = False
    add_data(gps_data_ints)
    return gps_data_ints

def convert_arduino_data(data_list): #returns list in SI units
    convert_list = [0,0,0,0,0]
    convert_list[0] = data_list[0]       #as fix remains constant
    convert_list[1] = data_list[1]*0.514 #knots to ms-1
    convert_list[2] = data_list[2]       #as alt remains constant
    convert_list[3] = data_list[3]       #position will convert degrees to eters offset
    convert_list[4] = data_list[4]
    return convert_list

def get_arduino_status():
    global ard_status
    return ard_status
def get_file_status():
    global ard_file_error
    return ard_file_error
def get_gps_data(): #returns tuple fix, speed, altitude, latitude, longitude, time
    print "get gps data"
    return convert_arduino_data(read_arduino()),time.time()

