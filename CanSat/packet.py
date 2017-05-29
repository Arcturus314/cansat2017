import datastore

#this module will serve to facilitate the building of packets for transmission to the base station

#several packet types are possible, which can be modularly built from:
# 1) individual sensor data points
# 2) all sensor data points
# 3) sensor error values
# 4) current cansat position
# 5) current temperature matrix
# 6) overall temperature map

#Packets can also be built via type
# 1) all current sensor data
# 2) all environmental logging data
# 3) all position tracking data
# 4) all heat map data
# 5) current stored heat map
# 6) all stored sensor data
# 7) all error data

#packet settings will be stored in the following set of variables

#indicates whether individual sensor data points should be included
#[accelerometer, magnetometer, gyroscope, imu_temp, env_pressure, env_humidity]
inc_data = [True, True, True, True, True, True]
#indicates whether all sensor data points should be included
#[accelerometer, magnetometer, gyroscope, imu_temp, env_pressure, env_humidity]
inc_all_data = [False, False, False, False, False, False]
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
#'I' denotes individual point; 'A' denotes all points
id_dict = ['AccelI': 0x00, 'MagI': 0x01, 'GyroI': 0x02, 'iTempI': 0x03, 'ePresI': 0x04, 'eHumI': 0x05, 'eTempI': 0x06]

packet_type= 0

#Packets will be structured as follows
# --header--
# ':,(num messages in body),|'
# ---body---
# '(identifier),(data1),(data2),...,;'
# '(identifier),(data1),(data2),...,;' 
# ...
# '|'
# --footer--
# (checksum)

def init_packet(_inc_data,_inc_all_data,_inc_error,_inc_pos,_inc_mat,_inc_map):
    global inc_data,inc_all_data,inc_error,inc_pos,inc_mat,inc_map
    inc_data = _inc_data
    inc_all_data = _inc_all_data
    inc_error = _inc_error
    inc_pos = _inc_pos
    inc_mat = _inc_mat
    inc_map = _inc_map
def init_packet(_packet_type):
    global inc_data,inc_all_data,inc_error,inc_pos,inc_mat,inc_map,packet_type
    packet_type = _packet_type
    if packet_type == 1:
        inc_data  = [True, True, True, True, True, True]
        inc_all_data = [False, False, False, False, False, False]
        inc_error = False
        inc_pos = False
        inc_map = False
        inc_mat = False
    if packet_type == 2:
        inc_all_data = [False, False, False, True, True, True]
        inc_data = [False, False, False, False, False, False]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = False
    if packet_type == 3:
        inc_data = [True, True, True, False, True, False]
        inc_all_data = [False, False, False, False, False, False]
        inc_error = True
        inc_pos = True
        inc_mat = False
        inc_map = False
    if packet_type == 4:
        inc_data = [False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False]
        inc_error = False
        inc_pos = True
        inc_mat = True
        inc_map = False
    if packet_type == 5:
        inc_data = [False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = True
    if packet_type == 6:
        inc_data = [False, False, False, False, False, False]
        inc_all_data = [True, True, True, True, True, True]
        inc_error = False
        inc_pos = False
        inc_mat = False
        inc_map = False
    if packet_type = 7:
        inc_data = [False, False, False, False, False, False]
        inc_all_data = [False, False, False, False, False, False]
        inc_error = True
        inc_pos = False
        inc_mat = False
        inc_map = False
       
def build_header():
    header = "" #header string
    header = header + ":"
    messages = 0 #number of messages contained in body
    
    for i in xrange(6)
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
    
    header = header + str(messages)

    return header
def build_body():        
    body = "" #string to hold body message
    
    #Now need to add all relevant data in header and message system
    if packet_type != 0:
        if packet_type = 1:
            data =  datastore.read_all_active()
