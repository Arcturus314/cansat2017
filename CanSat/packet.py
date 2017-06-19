import datastore
import position
import temp_map

#this module will serve to facilitate the building of packets for transmission to the base station

#Packets can also be built via type
# 1) all current sensor data
# 2) all environmental logging data
# 3) all position tracking data
# 4) all heat mat data
# 5) current stored heat map
# 6) all stored sensor data
# 7) all error data

#packet settings will be stored in the following set of variables

#indicates whether individual sensor data points should be included
#[accelerometer, magnetometer, gyroscope, imu_temp, env_pressure, env_humidity, env_temp]
inc_data = [True, True, True, True, True, True, True]
#indicates whether all sensor data points should be included
#[accelerometer, magnetometer, gyroscope, imu_temp, env_pressure, env_humidity, env_temp]
inc_all_data = [False, False, False, False, False, False, False]
#indicates whether error values should be included
inc_error = True
#indicates whether current cansat position should be included
inc_pos = True
#indicates whether current temperature matrix should be included
inc_mat = True
#indicates whether the overall temperature map should be included
inc_map = True

#Each potential data value will have an associated identifier
#stored in a dictionary
id1_dict = {'Default': 0x00, 'Accel': 0x01, 'Mag': 0x02, 'Gyro': 0x03, 'iTemp': 0x04, 'ePres': 0x05, 'eHum': 0x06, 'eTemp': 0x07, 'Error': 0x08, 'Pos': 0x09, 'Mat': 0x0A, 'Map': 0x0B}
#Secondary identifier allows for differentiation between values of the same sensor
#Ex single value has id2 = 0x00 double value has id2 = 0x01
id2_dict = {'Default': 0x00, 'Single': 0x01, 'All': 0x02}

#Name list to simplify code: tracks index vs sensor type for inc_data and inc_all_data
index_names = ['Accel', 'Mag', 'Gyro', 'iTemp', 'ePres', 'eHum', 'eTemp']
method_names = ['get_accelerometer_data','get_magnetometer_data','get_gyroscope_data','get_imu_temp_data','get_env_pressure_data','get_env_humidity_data','get_env_temp_data']

packet_type = 0
checksum_contribution = 0

temp_map.init_data() #initializing data lists
position.init_data() #initializing data lists

#Packets will be structured as follows
# --header--
# ':,(num messages in body),|'
# ---body---
# '(identifier1),(identifier2),(data1),(data2),...,;'
# '(identifier1),(identifier2),(data1),(data2),...,;' 
# ...
# '|'
# --footer--
# (checksum)


def create_message(identifier1, identifier2, data):
    global checksum_contribution
    message = id1_dict[identifier1] + ',' + id2_dict[identifier2] + ','
    checksum_contribution = checksum_contribution + int(id1_dict[identifier1]) + int(id2_dict[identifier2])
    if type(data) == tuple:
        for i in xrange(data.len()):
            message = message + data[i] + ','
            checksum_contribution = checksum_contribution + int(data[i])
    message = message + ';'
    return message

def init_packet(_inc_data,_inc_all_data,_inc_error,_inc_pos,_inc_mat,_inc_map):
    global inc_data,inc_all_data,inc_error,inc_pos,inc_mat,inc_map,checksum_contribution
    checksum_contribution = 0
    inc_data = _inc_data
    inc_all_data = _inc_all_data
    inc_error = _inc_error
    inc_pos = _inc_pos
    inc_mat = _inc_mat
    inc_map = _inc_map
def init_packet_type(_packet_type):
    global inc_data,inc_all_data,inc_error,inc_pos,inc_mat,inc_map,packet_type, checksum_contribution
    checksum_contribution = 0
    packet_type = _packet_type
    if packet_type == 1:
        inc_data  = [True, True, True, True, True, True, True]
        inc_all_data = [False, False, False, False, False, False, True]
        inc_error = False
        inc_pos = False
        inc_map = False
        inc_mat = False
    if packet_type == 2:
        inc_all_data = [False, False, False, True, True, True, True]
        inc_data = [False, False, False, False, False, False, False]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = False
    if packet_type == 3:
        inc_data = [True, True, True, False, True, False, False]
        inc_all_data = [False, False, False, False, False, False, False]
        inc_error = True
        inc_pos = True
        inc_mat = False
        inc_map = False
    if packet_type == 4:
        inc_data = [False, False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False, False]
        inc_error = False
        inc_pos = True
        inc_mat = True
        inc_map = False
    if packet_type == 5:
        inc_data = [False, False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False, False]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = True
    if packet_type == 6:
        inc_data = [False, False, False, False, False, False, False]
        inc_all_data = [True, True, True, True, True, True, False]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = False
    if packet_type == 7:
        inc_data = [False, False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False, False]
        inc_error = True
        inc_pos = False
        inc_mat = False
        inc_map = False
       
def build_header():
    header = "" #header string
    header = header + ":"
    messages = 0 #number of messages contained in body
    
    for i in xrange(6):
        if inc_data[i] == True:
            messages = messages + 1
        if inc_all_data[i] == True:
            messages = messages + 1
    if inc_error == True:
        messages = messages + 1
    if inc_pos == True:
        messages = messages + 1
    if inc_mat == True:
        messages = messages + 1
    if inc_map == True:
        messages = messages + 1        
    
    header = header + str(messages) + '|\n'
    return header
def build_body():        
    body = "" #string to hold body message
    for i in xrange(len(inc_data)):
        if inc_data[i] == True:
            body = body + create_message(id1_dict[index_names[i]],'Single',getattr(datastore,method_names[i])(False))
        body = body + ';\n'
    for i in xrange(len(inc_all_data)):
        if inc_all_data[i] == True:
            body = body + create_message(id1_dict[index_names[i]],'All',getattr(datastore,method_names[i])(True))
        body = body + ';\n'

    if inc_error == True:
        body = body + create_message(id1_dict['Error'],id2_dict['Default'],datastore.get_errors())
        body = body + ';\n'
    if inc_pos == True:
        body = body + create_message(id1_dict['Pos'],id2_dict['Default'],position.get_pos_data(False))
        body = body + ';\n'
    if inc_mat == True:
        body = body + create_message(id_dict['Mat'],id2_dict['Default'],datastore.get_temp_array_data())
        body = body + ';\n'
    if inc_map == True:
        temp_map.build_frame()
        body = body + create_message(id_dict['Map'],id2_dict['Default'],temp_map.return_frame())
        body = body + ';\n'

    body = body + '|\n'
    return body
def build_footer():
    global checksum_contribution
    return checksum_contribution % 251 #as 251 is the largest prime number less than 255

def build_packet():
    return build_header() + build_body() + build_footer() 
