#import datastore
#import position
#import temp_map
#import timed_input

start_data = False
input_timeout = 3 #3 seconds to wait for response
num_packets = 0
num_failures = 0

def t_input(message):
    return timed_input(message,input_timeout)

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
        return -1

def sms_malformed_packet(): #texts home in case of malformed packet
    return None

def parse_body(header,body): 
    global num_packets
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
            settings = body.split(";")
            
    except:
        num_failures = num_failures+1
        return -1

def send_packet(packet):
    print packet
