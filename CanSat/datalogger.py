import datastore
import position
import temp_map

#filenames
all_data_fileName = "sensor_data_all.txt"
position_fileName = "position_data.txt"
temp_map_fileName = "temp_map_data.txt"



#file instantiation
all_data_file_error = False #True when file cannot be opened
position_file_error = False #True when file cannot be opened
temp_map_file_error = False #True when file cannot be opened

try:
    file = open(all_data_fileName, "a")
    file.close()
    all_data_file_error = False 
except IOError, err:
    data_file_error = True

try:
    file = open(position_fileName, "a")
    file.close()
    position_file_error = False 
except IOError, err:
    position_file_error = True

try:
    file = open(temp_map_fileName, "a")
    file.close()
    temp_map_file_error = False 
except IOError, err:
    temp_map_file_error = True

def add_data():
    global all_data_fileName,all_data_file_error
    try:
        file = open(all_data_fileName, "a")
        data = datastore.read_all_active()
        sensor_list = ["accel","mag","gyro","imu_temp","env_pres","env_hum","env_temp","temp_array","temp"]
        for element in data:
            print element
        for i in xrange(len(data)):
            file.write(sensor_list[i])
            file.write(",")
            file.write(str(data[i]))
            file.write('\n')
        errors = datastore.get_errors()
        error_list = ["accel_error","mag_error","gyro_error","env_error","temp_camera_error"]
        for i in xrange(len(errors)):
            file.write(error_list[i])
            file.write(",")
            file.write(str(errors[i]))
            file.write('\n')
        file.close()
    except IOError, err:
        all_data_file_error = True
def add_pos():
    global position_fileName, position_file_error
    try:
        file = open(position_fileName, "a")
        data = position.get_pos_data(False)
        data_list = ["translational position", "orientation"]
        for i in xrange(len(data)):
            file.write(data_list[i])
            file.write(",")
            file.write(str(data[i]))
            file.write(",")
            file.write(time.time())
            file.write('/n')
        file.close()
    except IOError, err:
        position_file_error = True
def add_temp_map():
    global temp_map_fileName,temp_map_file_error
    try:
        file = open(temp_map_fileName, "a")
        temp_map.build_frame()
        file.write(str(temp_map.return_frame()))
        file.write('\n')
        file.close()
    except IOError, err:
        temp_map_file_error = True

def add_all_single():
    add_data()
    add_pos()
    add_temp_map()

def add_all_inf():
    while True:
        add_data()
        add_pos()
        add_temp_map()
