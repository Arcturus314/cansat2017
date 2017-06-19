import datastore
import timed_input
import packet
import datalogger
import multiprocessing

start_data = False
input_timeout = 3 #3 seconds to wait for response
num_packets = 0
num_failures = 0

def t_input(message):
    in_data = 0
    try:
        in_data =  timed_input.nonBlockingRawInput(message,input_timeout)
    except EOFError, err:
        pass
    return in_data

#packet takes form
#":,(id),|(message)|checksum"
#id:
#   0: custom data packet
#   1: change settings
#   2: request all current sensor data
#   3: request all env logging data
#   4: request all position tracking data
#   5: request all heat map data
#   6: request all stored heat map data
#   7: request all stored sensor data
#   8: request all error data
#message:
#   0: for id 2-7
#   sensor_id,setting,value;...: for id 1
#       sensor_id: 0 accel,1 mag,2 gyro,3, gsm
#       setting: 0 power,1 update,2 full scale deflection
#       value: 0 false, 1 true
#   _,_,_,_,_,_,_;_,_,_,_,_,_,_;_;_;_;_: for custom packet- ind_data,inc_all_data,error,pos,mat,map
#checksum: see method

def parse_packet(packet):
    global num_packets,num_failures
    num_packets = num_packets + 1
    try:
        t_packet = packet.split(":")[1] #identifying packet by initial ':'
        p_packet = t_packet.split("|")  #splitting packet into header,body,and footer, separated by '|'
        header   = int(p_packet[0].split(",")[1]) #extracting identifier int from header
        body     = p_packet[1]
        footer   = int(p_packet[2])
        return header,body,footer
    except:
        num_failures = num_failures+1
        sms_malformed_packet()
        return -1
def sms_malformed_packet(): #texts home in case of malformed packet
    return None
def parse_body(header,body): 
    global num_packets
    checksum_contribution = 0
    try:
        if header==0: #custom data packet
            packet_settings = body.split(";")
            inc_data     = packet_settings[0]
            inc_all_data = packet_settings[1]
            inc_error    = packet_settings[2]
            inc_pos      = packet_settings[3]
            inc_mat      = packet_settings[4]
            inc_map      = packet_settings[5]
            packet.init_packet(inc_data,inc_all_data,inc_error,inc_pos,inc_mat,inc_map)
            send_packet(packet.build_packet())
        if header==1:
            settings_list = body.split(";")
            for setting in settings_list:
                power      = True
                update     = True
                deflection = True
                if setting[0] == 0: #accelerometer
                    if setting[1] == 0:
                        if setting[2] == 0:
                            power = False
                    if setting[1] == 1:
                        if setting[2] == 0:
                            update = False
                    if setting[1] == 2:
                        if setting[2] ==0:
                            deflection = False
                    datastore.set_accelerometer_settings(power, update, deflection)
                if setting[0] == 1: #magnetometer
                    if setting[1] == 0:
                        if setting[2] == 0:
                            power = False
                    if setting[1] == 1:
                        if setting[2] == 0:
                            update = False
                    if setting[1] == 2:
                        if setting[2] ==0:
                            deflection = False
                    datastore.set_magnetometer_settings(power, update, deflection)
                if setting[0] == 2: #gyroscope
                    if setting[1] == 0:
                        if setting[2] == 0:
                            power = False
                    if setting[1] == 1:
                        if setting[2] == 0:
                            update = False
                    if setting[1] == 2:
                        if setting[2] ==0:
                            deflection = False
                    datastore.set_gyroscope_settings(power, update, deflection)
                if setting[0] == 3: #sim800l
                    if setting[1] == 0:
                        if setting[2] == 0:
                            power = False
            return_read()
        if header==2:
            packet.init_packet_type(1)
            send_packet(packet.build_packet())
        if header==3:
            packet.init_packet_type(2)
            send_packet(packet.build_packet())
        if header==4:
            packet.init_packet_type(3)
            send_packet(packet.build_packet())
        if header==5:
            packet.init_packet_type(4)
            send_packet(packet.build_packet())
        if header==6:
            packet.init_packet_type(5)
            send_packet(packet.build_packet())
        if header==7:
            packet.init_packet_type(6)
            send_packet(packet.build_packet())
        if header==8:
            packet.init_packet_type(7)
            send_packet(packet.build_packet())
        return 1
    except:
        num_failures = num_failures+1
        sms_malformed_packet()
        return -1
def send_packet(packet):
    print packet
def return_ready():
    print "ready"
def overall_control():
    while True:
        in_packet = t_input("")
        print in_packet
        if in_packet == -1:
            send_packet(packet.build_packet())
        parsed_packet = parse_packet(in_packet)
        if parsed_packet != -1:
            build_packet(parsed_packet[0],parsed_packet[1])


#Actual code execution
return_ready() #ready returned on startup

#Control process manages overall packetization / communicatio with the base station
#Logger process independently manages data logging and recording to files

if __name__ == '__main__':
    control = multiprocessing.Process(target=overall_control)
    logger = multiprocessing.Process(target=datalogger.add_all_inf)
    control.start()
    logger.start()








