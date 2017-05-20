#I2C address table
#address  |device
#0x0Bh    |Arduino
#0x77h    |BMP180
#0x0Ah    |D6T

#program structure
#every 1000ms will:
#   read any new commands from XBEE
#       execute commands if necessary
#   poll sensors for data
#   request data and commands from Arduino
#       execute commands if necessary
#   assemble data into required packet sequence
#   print data to terminal in specified sequence

#setup
import smbus
import time
import sys
import math
import os
from multiprocessing import Process, Manager
from ctypes import c_short
from select import select

#data storage setup
manager = Manager()

data = manager.list()
ard_data = []

#Error setup
lsm303_err = False
bmp180_err = False
ard_err = False
d6t_err = False
l3gd20_err = False

#sensor setup
import Adafruit_LSM303
lsm303 = Adafruit_LSM303.LSM303()
BMP180 = 0x77
bus = smbus.SMBus(1) #on i2c bus 1
ard_addr = 0x0B
sim_data = 0x00
d6t_addr = 0x0A
l3gd20_addr = 0x6B

timeout = 1 #timeout in seconds for input command

filename = "data.txt" #file name to back up data

start_time = time.time()

#input methods
#def time_input(): #raw_input with a timeout #WILL NOT RUN ON WINDOWS
    #rlist, _, = select([sys.stdin], [], [], timeout)
    #if rlist:
    #    s = sys.stdin.readline()
    #    msg = s
    #else:
    #    msg = "null"
    #return msg

def update_time(): #adds elapsed time to list
    global start_time
    t_d = time.time()-start_time
    data[36] = t_d

def time_input(stdin): #REMOVE AFTER YOU FIX ACTUAL METHOD YA DINGUS
    return stdin.readline()

#arduino control methods
def read_arduino(): #requests and reads data from Arduino
    global ard_err
    global ard_data
    #print "starting arduino read"
    for i in xrange(30):
        try:
            ard_data[i] = bus.read_byte(ard_addr)
            #print "byte received, ",
            #print ard_data[i]
        except IOError, err:
            ard_err = True
            #print "arduino failure"

    #print "checking validity"
    #checking validity
    if (ard_data[0] == 0x00 and ard_data[1] == 0x00 and ard_data[28] == 0xFF and ard_data[29] == 0xFF and ard_err == False):
        #DHT22 value
        #print "valid"
        try:
        #print "trying..."
            data[0] = int(chr(ard_data[2])+chr(ard_data[3])) #temperature
            data[1] = int(chr(ard_data[4])+chr(ard_data[5])) #humidity
            #GPS value
            data[2]  = chr(ard_data[6])+chr(ard_data[7])+chr(ard_data[8])+chr(ard_data[9])+chr(ard_data[10])+chr(ard_data[11])+chr(ard_data[12])+chr(ard_data[13]) #longitude
            data[3]  = int(str(ard_data[14])) #longitude direction
            data[4]  = chr(ard_data[15])+chr(ard_data[16])+chr(ard_data[17])+chr(ard_data[18])+chr(ard_data[19])+chr(ard_data[20])+chr(ard_data[21])+chr(ard_data[22]) #latitude
            data[5]  = int(str(ard_data[23])) #latitude direction
            data[6]  = chr(ard_data[24])+chr(ard_data[25]) #speed
            data[7]  = int(str(ard_data[26])) #validity
            sim_data = int(str(ard_data[27])) #sim800l commands
            interpret_sim_commands(sim_data)
        except ValueError, err:
            ard_err = True
    return None

def send_arduino_command(command, text): #sends a specified command to the Arduino
    try:
        bus.write_byte(ard_addr, 0x00)
        bus.write_byte(ard_addr, 0x00)
        bus.write_byte(ard_addr, command)
        bus.write_byte(ard_addr, text)
        bus.write_byte(ard_addr, 0xFF)
        bus.write_byte(ard_addr, 0xFF)
    except IOError, err:
        ard_err = True
    return None

#general data conversion methods
def convertToString(data): #converts binary data into a string
    return str((data[1] + (256*data[0])) / 1.2)

def getShort(data, index): #returns two bytes from data as a signed 16 bit value
    return c_short((data[index] << 8) + data[index + 1]).value

def getUShort(data, index): #returns two bytes from data as an unsigned 16 bit value
    return (data[index] << 8) + data[index+1]

#sensor control methods
def readBmp180Id(addr=BMP180):
    #Chip ID Register Address
    REG_ID = 0xD0
    try:
        (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
        return (chip_id, chip_version)
    except IOError, err:
        bmp180_err = True

def readBmp180(addr=BMP180):
    #Register addresses
    REG_CALIB = 0xAA
    REG_MEAS  = 0xF4
    REG_MSB   = 0xF6
    REG_LSB   = 0xF7
    #Control register addresses
    CRV_TEMP  = 0x2E
    CRV_PRES  = 0x34
    #Oversample setting
    OVERSAMPLE = 3
    
    bmp180_err = False    

    #Read calibration data from EEPROM
    try:
        cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)
    except IOError, err:
        bmp180_err = True

    if bmp180_err == False:
        #Convert byte data to word values
        AC1 = getShort(cal, 0)
        AC2 = getShort(cal, 2)
        AC3 = getShort(cal, 4)
        AC4 = getUShort(cal, 6)
        AC5 = getUShort(cal, 8)
        AC6 = getUShort(cal, 10)
        B1 = getShort(cal, 12)
        B2 = getShort(cal, 14)
        MB = getShort(cal, 16)
        MC = getShort(cal, 18)
        MD = getShort(cal, 20)

        #read temperature
        bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
        time.sleep(0.005)
        (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
        UT = (msb << 8) + lsb

        #read pressure
        bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
        time.sleep(0.04)
        (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
        UP = ((msb << 16) + (lsb << 8) + xsb) >> (8-OVERSAMPLE)

        #refine temperature
        X1 = ((UT - AC6) * AC5) >> 15
        X2 = (MC << 11) / (X1 + MD)
        B5 = X1 + X2
        temperature = (B5 + 8) >> 4

        #refine pressure
        B6 = B5 - 4000
        B62 = B6 * B6 >> 12
        X1 = (B2 * B62) >> 11
        X2 = AC2 * B6 >> 11
        X3 = X1 + X2
        B3 = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

        X1 = AC3 * B6 >> 13
        X2 = (B1 * B62) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> OVERSAMPLE)

        P = (B7 * 2) / B4

        X1 = (P >> 8) * (P >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * P) >> 16
        pressure = P + ((X1 + X2 + 3791) >> 4)

        data[8] = temperature / 10.0
        data[9] = pressure / 100.0
        
    return None

def read_D6T(): #requests and reads data from D6T
    D6T_data = []
    for i in xrange(40):
        D6T_data.append(0)
    d6t_err = False
    try:
        D6T_data = bus.read_i2c_block_data(d6t_addr, 0x4C)
        #D6T_data.append(bus.read_byte_data(d6t_addr, 0x5C))
        #D6T_data.append(bus.read_byte_data(d6t_addr, 0x5D))
    except IOError,err:
        d6t_err = True
    if d6t_err == False:
        data[19] = (D6T_data[0] + 256*D6T_data[1])/10.0
        data[20] = (D6T_data[2] + 256*D6T_data[3])/10.0
        data[21] = (D6T_data[4] + 256*D6T_data[5])/10.0
        data[22] = (D6T_data[6] + 256*D6T_data[7])/10.0
        data[23] = (D6T_data[8] + 256*D6T_data[9])/10.0
        data[24] = (D6T_data[10]+ 256*D6T_data[11])/10.0
        data[25] = (D6T_data[12]+ 256*D6T_data[13])/10.0
        data[26] = (D6T_data[14]+ 256*D6T_data[15])/10.0
        data[27] = (D6T_data[16]+ 256*D6T_data[17])/10.0
        data[28] = (D6T_data[18]+ 256*D6T_data[19])/10.0
        data[29] = (D6T_data[20]+ 256*D6T_data[21])/10.0
        data[30] = (D6T_data[22]+ 256*D6T_data[23])/10.0
        data[31] = (D6T_data[24]+ 256*D6T_data[25])/10.0
        data[32] = (D6T_data[26]+ 256*D6T_data[27])/10.0
        data[33] = (D6T_data[28]+ 256*D6T_data[29])/10.0
        data[34] = (D6T_data[30]+ 256*D6T_data[31])/10.0
        #data[35] = (D6T_data[32]+ 256*D6T_data[33])/10.0
        sumt = 0
        for i in xrange(16):
            sumt = sumt+data[19+i]
        data[35] = sumt / 16.0
    return None

def read_LSM303(): #requests and reads data from LSM303
    lsm303_err = False
    try:
        accel, mag = lsm303.read()
    except IOError,err:
        lsm303_err = True
    if lsm303_err == False:
        accel_x, accel_y, accel_z = accel
        mag_x, mag_z, mag_y = mag
        data[16] = accel_x / 1000.0 * 9.81
        data[17] = accel_y / 1000.0 * 9.81
        data[18] = accel_z / 1000.0 * 9.81
        data[13] = mag_x / 1000.0
        data[14] = mag_y / 1000.0
        data[15] = mag_z / 1000.0
    return None

def read_L3GD20(): #requests and reads data from L3GD20
    l3gd20_err = False
    ares = 0.00875
    try:
        bus.write_byte_data(l3gd20_addr, 0x20, 0x2F)
        bus.write_byte_data(l3gd20_addr, 0x23, 0x40)
        axh = bus.read_byte_data(l3gd20_addr, 0x28)
        axl = bus.read_byte_data(l3gd20_addr, 0x29)
        ayh = bus.read_byte_data(l3gd20_addr, 0x2A)
        ayl = bus.read_byte_data(l3gd20_addr, 0x2B)
        azh = bus.read_byte_data(l3gd20_addr, 0x2C)
        azl = bus.read_byte_data(l3gd20_addr, 0x2D)
    except IOError,err:
        l3gd20_err = True
    
    if l3gd20_err == False:
        ax = (axh << 8 | axl) >> 4
        ay = (ayh << 8 | ayl) >> 4
        az = (azh << 8 | azl) >> 4

        if ax > 2047: ax = ax - 4096
        if ay > 2047: ay = ay - 4096
        if az > 2047: az = az - 4096

        data[10] = ax*ares
        data[11] = ay*ares
        data[12] = az*ares

    return None

def BMP180_state(mode): #if mode == True, turn on power-save, if mode == False, turn off power-save
    return None

def D6T_state(mode): #if mode == True, turn on power-save, if mode == False, turn off power-save
    return None

def LSM303_state(mode): #if mode == True, turn on power-save, if mode == False, turn off power-save
    return None

def L3GD20_state(mode): #if mode == True, turn on power-save, if mode == False, turn off power-save
    return None

#overall control methods
def on_start(): #executed when the program is first launched
    #1. Sends message to base station that requires confirmation
    #2. Confirms communication with sensors
    #3. Sends command to Arduino
        #a) Turn sensors on
        #b) Send status message via SMS
    
    #Establishing communication with base station
    print "Boot Successful"
    conf = raw_input()
    while(conf != "ack"):
        print "Boot Successful"
        conf = raw_input()
    
    #Confirming communication with sensors
    BMP180_state(True)
    D6T_state(True)
    LSM303_state(True)
    L3GD20_state(True)

    #Sending commands to Arduino
    ard_command = 0xFC #11111100
    sim_message = 0x88 #10001000
    #send_arduino_command(ard_command, sim_message) 
   
    return None

def update_data(): #updates data lists
    read_arduino()
    readBmp180()
    read_D6T()
    read_LSM303()
    read_L3GD20()
    update_time()
    #print "data",
    #print data[38]

def send_standard_update(): #send standard update 
    print ":",
    print 0x00,
    print ",",
    print 0x00,
    print ",",

    for i in xrange(37):
        print data[i],
        print",",

    print 0xFF,
    print ",",
    print 0xFF,

    return None

def save_in_file(): #save in file 'data.txt'
    file = open(filename, "a")
    for i in xrange(37):
        file.write(str(data[i]))
        file.write(",")
    file.write('\n')
    file.close() 
    return None

def receive_command(stdin): #receive command from base station
    command_list = [0,0,0,0,0,0,0]
    for i in xrange(7):
        command_list[i] = time_input(stdin)

    if(command_list[0] == 0x00 and command_list[1] == 0x00 and command_list[6] == 0xFF and command_list[7] == 0xFF): #checking validity
        send_arduino_command(command_list[2], 0x00)

        #checking chip command bytes
        #BMP180 control
        if(command_list[3]&(2**0)==2**0 and command_list[3]&(2**1)==2**1):
            BMP180_state(True)
        if(command_list[3]&(2**0)==0 and command_list[3]&(2**1)==0):
            BMP180_state(False)
        #L3GD20 control
        if(command_list[3]&(2**2)==2**2 and command_list[3]&(2**3)==2**3):
            L3GD20_state(True)
        if(command_list[3]&(2**2)==0 and command_list[3]&(2**3)==0):
            L3GD20_state(False)
        #LSM303 control
        if(command_list[3]&(2**4)==2**4 and command_list[3]&(2**5)==2**5):
            LSM303_state(True)
        if(command_list[3]&(2**4)==0 and command_list[3]&(2**5)==0):
            LSM303_state(False)
        #D6T control
        if(command_list[3]&(2**6)==2**6 and command_list[3]&(2**6)==2**6):
            D6T_state(True)
        if(command_list[3]&(2**6)==0 and command_list[3]&(2**6)==0):
            D6T_state(False)
        #quitting program
        if(command_list[4]==0 and command_list[5]==0):
            quit()

    return None

def interpret_sim_commands(command): #interpret and execute commands from SIM800L
    return None

def init_data(): #fills list data with 0
    for i in xrange(45):
        data.append(0.0)
        ard_data.append(0)

#Program flow and structure
def start(): #tasks to run on program start
    init_data()
    on_start()
    update_data()

def log(): #tasks to run to log data
    while True:
        #print "log taken"
        update_data()
        save_in_file()
        time.sleep(0.1)

def send(stdin): #tasks to communicate with base station
    while True:
        send_standard_update()
        receive_command(stdin)

#Stuff to run 
newstdin = os.fdopen(os.dup(sys.stdin.fileno()))

p1 = Process(target=log)
p2 = Process(target=send, args = (newstdin, ))
   
start()
if __name__ == '__main__':
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
if p1.is_alive() == False:
    p1.start()
    p1.join()

if p2.is_alive() == False:
    p2.start()
    p2.join()
