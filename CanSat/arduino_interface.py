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
    data = ""
    try:
        data = str(unichr(bus.read_byte(ard_addr)))
        ard_status = True
    except IOError, err:
        ard_status = False
    except UnicodeEncodeError, err2:
        pass
    #print data,
    return data

def read_arduino(): #returns list [fix,speed,altitude,latitude,longitude]
    global ard_status
    gps_data = ["","","","",""]
    gps_data_floats = [-1.0,-1.0,-1.0,-1.0,-1.0]
    count = 0
    try:
        if ard_status == True:
            #need to wait for initial ':'
            in_char = ' '

            #print "waiting for initial colon..."
            while in_char != ':': #this loop will break when the initial colon is read
                in_char = read_byte()

            #print "reading data..."
            for i in xrange(5): #as there are 5 data points
                while in_char != ',': #reading the contents of each byte
                    in_char = read_byte()
                    if in_char != ',':
                        gps_data[i] = gps_data[i] + in_char
                in_char = ' '
                #print "comma found"
            #print "data start"
            #for element in gps_data:
                #print element
            #print "data end"
            #print "parsing data..."
            for i in xrange(5):
                gps_data_floats[i] = float(gps_data[i])
        else:
            read_byte() #to update arduino state
    except IOError, err:
        ard_status = False
    except ValueError, err:
        pass
    add_data(gps_data_floats)
    if gps_data_floats[0] == 1.0 and -1 in gps_data_floats: #if the GPS has a lock, rest of data must be valid for position to be returned
        return [0.0,0.0,0.0,0.0,0.0]
    return gps_data_floats

    #try:
    #    in_char = ' '
    #    while in_char != ':' and ard_status == True:
    #        for i in xrange(5):
    #            while in_char != ',' and in_char != -1:
    #                in_char = read_byte()
    #                if in_char != -1:
    #                    gps_data[i] = gps_data[i]+str(read_byte())
    #        for i in xrange(5):
    #            if ard_status == True:
    #                gps_data_ints[i] = int(gps_data[i])
    #        ard_status = True
    #except IOError, err:
    #    ard_status = False
    #add_data(gps_data_ints)
    #return gps_data_ints

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
    return convert_arduino_data(read_arduino()),time.time()

