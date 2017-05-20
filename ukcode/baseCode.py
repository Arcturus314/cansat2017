#imports
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
import time
import serial
import math
import numpy as np
import matplotlib.cm as cm
from matplotlib.widgets import Button


from mpltools import style
style.use('ggplot')

#serial port
#Device | Port
#CHIP   | ttyACM0
#XBEE   | ttyUSB0

#chip_ser

#data lists
temp_avr     = [] #stores temperature averaged between the bmp180, dht22, d6t, degC
temp_bmp180  = [] #stores temperature values from the bmp181, degC
temp_dht22   = [] #stores temperature values from the dht22, degC
pressure     = [] #stores pressure values from the bmp180, kPa
altitude     = [] #stores calculated altitude from the bmp180, m
humidity     = [] #stores humidity from dht22, relative humidity
gyro_x       = [] #stores x component of change in angle from LG3D20, rads^-1
gyro_y       = [] #stores y component of change in angle from LG3D20, rads^-1
gyro_z       = [] #stores z component of change in angle from LG3D20, rads^-1
accel_x      = [] #stores x component of acceleration from LSM303, ms^-2
accel_y      = [] #stores y component of acceleration from LSM303, ms^-2
accel_z      = [] #stores z component of acceleration from LSM303, ms^-2
comp_x       = [] #stores x component of magnetic field strength from LSM303, G 
comp_y       = [] #stores y component of magnetic field strength from LSM303, G 
comp_z       = [] #stores z component of magnetic field strength from LSM303, G 
comp_angle   = [] #stores calculated x-y angle East from North, degrees
d6t_temp_mat = [] #stores d6t temperature arrays as a 2x2 matrix, degC
d6t_ref_temp = [] #stores d6t reference temperature, degC

gps_long     = [] #stores gps longitude
gps_long_dir = [] #stores gps longitude direction, 0x00 E, 0xFF W
gps_lat      = [] #stores gps latitude
gps_lat_dir  = [] #stores gps latitude direction, 0x00 S, 0xFF N
gps_speed    = [] #stores gps speed, ms^-1
gps_valid    = [] #stores gps validity, valid for 0xFF, invalid for 0x00

timeMeas     = [] #stores time at each measurement

chip_received = ""

file_name = "backup.txt"
fig = plt.figure()

#true for on, false for off
gps_status = True
bmp180_status = True
dht22_status = True
sim800l_status = True

data_logging = False

response = [0,0,0,0,0,255,255]

ser_on = False

#setup methods
def ser_open(): #opens the serial port
    global chip_ser
    chip_ser = serial.Serial(
        port = '/dev/ttyUSB0', #Port will be /dev/USB0 when XBEE is used
        baudrate = 115200,
        parity = serial.PARITY_NONE, #CHECK,
        stopbits = serial.STOPBITS_ONE, #CHECK
        bytesize = serial.EIGHTBITS, #CHECK
    )

    #checking serial port
    print "Port used: ",
    print(chip_ser.name)
    chip_ser.isOpen()
    
    global ser_on
    ser_on = True

def program_start(): #starts the CHIP data logging program
    for i in xrange(5):
        chip_ser.write("ls \r\n")
    chip_ser.write("python chipCode.py \r\n") 

#test methods
def ser_test(): #just echoes serial terminal
    print 'enter commands below. \r\nInsert "exit" to leave the application.'
    input = 1
    while 1:
        key_input = raw_input(">> ")
        if key_input == 'exit':
            chip_ser.close()
            exit()
        else:
            chip_ser.write(key_input + '\r\n')
            out = ''
            time.sleep(1)
            while chip_ser.inWaiting() > 0:
            #    print "message received"
                 out += chip_ser.read()
            #    print chip_ser.read(),
            if out != '':
                print ">>" + out

#file backup methods
def append_file(): #adds data to a file
    file = open(file_name, "a")
    file.write(chip_received + '\n')
    file.close()

def delete_backup(): #deletes contents of a file
    file = open(file_name, "w")
    file.write("")
    file.close()

#serial methods
def read_chip(): #reads serial data from chip, stores it in chip_received
    global data_logging
    global chip_received
    chip_received = ""
    #print "read_chip called"
    while chip_ser.inWaiting() > 0:
        #print "data waiting"
        chip_received += chip_ser.read(chip_ser.inWaiting())
        #chip_received +=chip_ser.read_line()
        #print chip_received

def send_chip(data): #sends serial data to chip
    chip_ser.write(data + '\r\n')

def empty_response(): #sends empty response to CHIP
    for i in xrange(7):
        send_chip("0")

def quit_response(): #sends quit message to CHIP, NEEDS TO BE IMPLEMENTED ON CHIP SIDE
    for i in xrange(5):
        send_chip("0")
    for i in xrange(2):
        send_chip("255")

def construct_response(device, sensor, message): 
    return None

#data parsing methods
def update_all(): #updates data in all storage lists
    global chip_received
    data = chip_received.split(": ")
    temp_list = data[1].split(" , ")
    temp_float_list = []
    try:
        for i in xrange(41):
            temp_float_list.append(0)
        count = 0
        for i in xrange(4):
            temp_float_list[i] = (float(temp_list[i]))
        for i in xrange(6):
            temp_float_list[i+3] = (temp_list[i+3])
        for i in xrange(31):
            temp_float_list[i+10] = (float(temp_list[i+10]))
        if temp_float_list[0] == 0x00 and temp_float_list[1] == 0x00 and temp_float_list[39] == 0xFF and temp_float_list[40] == 0xFF:
            global temp_dht22
            temp_dht22.append(temp_float_list[2])
            global humidity
            humidity.append(temp_float_list[3])
            global gps_long
            gps_long.append(temp_float_list[4])
            global gps_long_dir
            gps_long_dir.append(temp_float_list[5])
            global gps_lat
            gps_lat.append(temp_float_list[6])
            global gps_lat_dir
            gps_lat_dir.append(temp_float_list[7])
            global gps_speed
            gps_speed.append(temp_float_list[8])
            global gps_valid
            gps_valid.append(temp_float_list[9])     
            global temp_bmp180
            temp_bmp180.append(temp_float_list[10])
            global pressure
            pressure.append(temp_float_list[11]*0.1)
            global gyro_x
            gyro_x.append(temp_float_list[12])
            global gyro_y
            gyro_y.append(temp_float_list[13])
            global gyro_z
            gyro_z.append(temp_float_list[14])
            global comp_x
            comp_x.append(temp_float_list[15])
            global comp_y
            comp_y.append(temp_float_list[16])
            global comp_z
            comp_z.append(temp_float_list[17])
            global accel_x
            accel_x.append(temp_float_list[18])
            global accel_y
            accel_y.append(temp_float_list[19])
            global accel_z
            accel_z.append(temp_float_list[20]) 
            global d6t_ref_temp
            d6t_ref_temp.append(temp_float_list[21])
            d6t_temp_list = []
            for i in xrange(16):
                d6t_temp_list.append(temp_float_list[22+i])
        
            global d6t_temp_mat
            d6t_temp_mat.append(d6t_temp_list)

            global temp_avr
            temp_avr.append((temp_float_list[2]+temp_float_list[10]+temp_float_list[21])/3)
        
            global timeMeas
            timeMeas.append(temp_float_list[38])
    except IndexError, err:
        print "incorrect reply pattern: index"
    except ValueError, err:
        print "incorrect reply pattern: value"
    
#button on-press methods
def gps_toggle(event):
    global gps_status
    print("gps toggle button pressed")
    gps_status = not gps_status

def sim800l_toggle(event):
    global sim800l_status
    print("sim800l toggle button pressed")
    sim800l_status = not sim800l_status    

def login(event):
    print "Logging into CHIP..."
    if(ser_on == False):
        print "Opening serial port..."
        ser_open()
    send_chip("chip")
    time.sleep(1)
    send_chip("chip")
    
def clBack(event):
    print("clear CHIP data button pressed")

def _start_chip(event):
    print("start chip button pressed")
    start_chip()    
    
def _stop_chip(event):
    print("stop chip button pressed")
    stop_chip()

def _clear_data(event):
    print("clear data button pressed")
    clear_data()

def _delete_backup(event):
    print("delete backup button pressed")
    delete_backup()

#graphing methods
def add_subplot_axes(ax,rect,axisbg='w'): #GIU code to allow for subfig axes
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)    
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height],axisbg=axisbg)
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

def prep_graph(): #setting up full screen window
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    plt.ion()

def hide_graph(): #hides the graph, obviously
    plt.close()

def start_display(): #provides plots of temperature, pressure, humidity, d6t temperature matrix, and acceleration
    global fig
    global temp    
    global tempMat
    global accel
    global gyro
    global press
    global hum
    global gps

    global temp_p1
    global temp_p2
    global temp_p3
    global temp_p4

    global accel_p1
    global accel_p2
    global accel_p3

    global gyro_p1
    global gyro_p2
    global gyro_p3

    global press_p
    global hum_p

    global cb

    temp = fig.add_subplot(331) #Graph showing temperatures for BMP180, D6T, DHT22, and mean temperature against time
    temp_p1, = temp.plot(timeMeas, temp_avr, marker='o', color='r', label="average")
    temp_p2, = temp.plot(timeMeas, temp_bmp180, marker='+', color='b', label="BMP180")
    temp_p3, = temp.plot(timeMeas, temp_dht22, marker='+', color='g', label="DHT22")
    temp_p4, = temp.plot(timeMeas, d6t_ref_temp, marker='+', color='c', label="D6T")
    temp.set_ylabel("Temperature (C)")
    temp.legend()

    current_temp = []

    if len(d6t_temp_mat) > 0:
        current_temp = d6t_temp_mat[len(d6t_temp_mat)-1] #Moves most recent temperature sensor data into a numpy array
    else:
        for i in xrange(16):
            current_temp.append(0)
    temp_arr = np.array([current_temp[0], current_temp[1], current_temp[2], current_temp[3], current_temp[4], current_temp[5], current_temp[6], current_temp[7], current_temp[8], current_temp[9], current_temp[10], current_temp[11], current_temp[12], current_temp[13], current_temp[14], current_temp[15]])
    temp_grid = temp_arr.reshape(4,4) #Reshapes numpy array into a 4x4 matrix

    tempMat = fig.add_subplot(335) #Plots a 4x4 pixel grid of D6T temperatures
    tempMat.axes.get_xaxis().set_visible(False)
    tempMat.axes.get_yaxis().set_visible(False)
    im1 = tempMat.imshow(temp_grid, extent=(0, 50, 0, 50), interpolation='nearest', cmap=cm.gist_heat) #Plots 4x4 grid; gist_heat is the colorscheme
    cb = fig.colorbar(im1) #Creates colorbar illustrating temperature color scale
    cb.set_label("Temperature (C)")

    accel = fig.add_subplot(336) #Plots x, y, z acceleration componenents against time
    accel.set_ylabel("Acceleration (ms^-2)")    
    accel_p1, = accel.plot(timeMeas, accel_x, marker='+', color='r', label="X")
    accel_p2, = accel.plot(timeMeas, accel_y, marker='+', color='b', label="Y")
    accel_p3, = accel.plot(timeMeas, accel_z, marker='+', color='g', label="Z")
    accel.legend()
  
    gyro = fig.add_subplot(334) #Plots x, y, z angular acceleration components against time
    gyro.set_ylabel("Angular Acceleration (rads^-2)")
    gyro_p1, = gyro.plot(timeMeas, gyro_x, marker='+', color='r', label="X")
    gyro_p2, = gyro.plot(timeMeas, gyro_y, marker='+', color='b', label="Y")
    gyro_p3, = gyro.plot(timeMeas, gyro_z, marker='+', color='g', label="Z")
    gyro.legend()

    press = fig.add_subplot(332) #Plots pressure against time
    press.set_ylabel("Pressure (kPa)")
    press_p, = press.plot(timeMeas, pressure, marker='+', color='b')

    hum = fig.add_subplot(333) #Plots humidity against time
    hum.set_ylabel("Humidity (%)")
    hum_p, = hum.plot(timeMeas, humidity, marker='+', color='g')

    gps = fig.add_subplot(337) #Lists GPS position as a text string
    gps.set_title("CanSat Status")
    gps.axes.get_xaxis().set_visible(False)
    gps.axes.get_yaxis().set_visible(False)
    gps.spines['right'].set_visible(False)
    gps.spines['top'].set_visible(False) 
    gps.spines['left'].set_visible(False)
    gps.spines['bottom'].set_visible(False) 

    global gps_lat
    global gps_lat_dir
    global gps_long
    global gps_long_dir
    global gps_valid
    global gps_speed    
     
    gps_lat_show = -1
    if len(gps_lat) > 0:
        gps_lat_show = gps_lat[len(gps_lat)-1]    

    gps_lat_dir_show = "U"
    if len(gps_lat_dir) > 0:
        if gps_lat_dir[len(gps_lat_dir)-1] == 0:
            gps_lat_dir_show = "S"
        if gps_lat_dir[len(gps_lat_dir)-1] == 255:
            gps_lat_dir_show = "N"
    
    gps_long_show = -1
    if len(gps_long) > 0:
        gps_long_show = gps_long[len(gps_long)-1]    

    gps_long_dir_show = "U"
    if len(gps_long_dir) > 0:
        if gps_long_dir[len(gps_long_dir)-1] == 0:
            gps_long_dir_show = "E"
        if gps_long_dir[len(gps_long_dir)-1] == 255:
            gps_long_dir_show = "W"
        
    gps_valid_show = False
    if len(gps_valid) > 0:
        gps_valid_show = gps_valid[len(gps_valid)-1]    
    
    gps_speed_show = -1
    if len(gps_speed) > 0:
        gps_speed_show = gps_speed[len(gps_speed)-1]

    global ser_on
    global data_logging

    s_status_show     = str(ser_on)
    d_status_show     = str(data_logging)
    gps_lat_show_all  = str(gps_lat_show) + gps_lat_dir_show
    gps_long_show_all = str(gps_long_show) + gps_long_dir_show
    gps_valid_show    = str(gps_valid_show)
    gps_speed_show    = str(gps_speed_show) 


    gps.text(0.05,0.78,"Serial Connection:")
    gps.text(0.05,0.65,"Data Logging")
    gps.text(0.05,0.52,"Latitude:")
    gps.text(0.05,0.39,"Longitude:")
    gps.text(0.05,0.26,"GPS Validity:")
    gps.text(0.05,0.13,"GPS Speed:")

    global sertext
    global dattext
    global gpstxt1
    global gpstxt2
    global gpstxt3
    global gpstxt4

    sertext = gps.text(0.5,0.78,s_status_show)
    dattext = gps.text(0.5,0.65,d_status_show)
    gpstxt1 = gps.text(0.5,0.26,gps_valid_show)
    gpstxt2 = gps.text(0.5,0.52,gps_lat_show_all)
    gpstxt3 = gps.text(0.5,0.39,gps_long_show_all)
    gpstxt4 = gps.text(0.5,0.13,gps_speed_show)

def update_display(): #updates data values without redrawing GUI

    global temp_p1
    global temp_p2
    global temp_p3
    global temp_p4

    global accel_p1
    global accel_p2
    global accel_p3

    global gyro_p1
    global gyro_p2
    global gyro_p3

    global press_p
    global hum_p

    global fig

    global cb

    current_time = 1

    if len(timeMeas) > 0:
        current_time =  max(timeMeas)       
    
    temp_p1.set_data(timeMeas, temp_avr)
    temp_p2.set_data(timeMeas, temp_bmp180)
    temp_p3.set_data(timeMeas, temp_dht22)
    temp_p4.set_data(timeMeas, d6t_ref_temp)
    temp.axis([0,current_time,0,50])

    #temp.draw_artist(temp_p1)
    #temp_p2.draw()
    #temp_p3.draw()
    #temp_p4.draw()

    current_temp = [0,1]

    if len(d6t_temp_mat) > 0:
        current_temp = d6t_temp_mat[len(d6t_temp_mat)-1] #Moves most recent temperature sensor data into a numpy array
    else:
        for i in xrange(16):
            current_temp.append(0)
    temp_arr = np.array([current_temp[0], current_temp[1], current_temp[2], current_temp[3], current_temp[4], current_temp[5], current_temp[6], current_temp[7], current_temp[8], current_temp[9], current_temp[10], current_temp[11], current_temp[12], current_temp[13], current_temp[14], current_temp[15]])
    temp_grid = temp_arr.reshape(4,4) #Reshapes numpy array into a 4x4 matrix

    tempMat.axes.get_xaxis().set_visible(False)
    tempMat.axes.get_yaxis().set_visible(False)
    im1 = tempMat.imshow(temp_grid, extent=(0, 50, 0, 50), interpolation='nearest', cmap=cm.gist_heat) #Plots 4x4 grid; gist_heat is the colorscheme
    #cb.set_clim(vmin = 0, vmax = 50) #Updates colorbar scale
    cb.set_clim([0,50])

    accel_p1.set_data(timeMeas, accel_x)
    accel_p2.set_data(timeMeas, accel_y)
    accel_p3.set_data(timeMeas, accel_z)
    accel.axis([0,current_time,-50,50])


    #accel_p1.draw()
    #accel_p2.draw()
    #accel_p3.draw()
  
    gyro_p1.set_data(timeMeas, gyro_x)
    gyro_p2.set_data(timeMeas, gyro_y)
    gyro_p3.set_data(timeMeas, gyro_z)
    gyro.axis([0,current_time,-50,50])

    #gyro_p1.draw()
    #gyro_p2.draw()
    #gyro_p3.draw()

    press_p.set_data(timeMeas, pressure)
    #press_p.draw()    
    press.axis([0,current_time,80,120])

    hum_p.set_data(timeMeas, humidity)
    #hum_p.draw()
    hum.axis([0,current_time,0,100])   

 
    pl_timeMeas = []
    pl_temp_avr = []
    pl_temp_bmp180 = []
    pl_temp_dht22 = []
    pl_d6t_ref_temp = []
    pl_accel_x = []
    pl_accel_y = []
    pl_accel_z = []
    pl_gyro_x = []
    pl_gyro_y = []
    pl_gyro_z = []
    pl_pressure = []
    pl_humidity = []

    
    #pl_temp_bmp180 = temp_bmp180[-10:]    
    #pl_temp_dht22 = temp_dht22[-10:]       
    #pl_d6t_ref_temp = d6t_ref_temp[-10:] 

    #temp_p1, = temp.plot(pl_timeMeas, pl_temp_avr, marker='o', color='r', label="average")
    #temp_p2, = temp.plot(pl_timeMeas, pl_temp_bmp180, marker='+', color='b', label="BMP180")
    #temp_p3, = temp.plot(pl_timeMeas, pl_temp_dht22, marker='+', color='g', label="DHT22")
    #temp_p4, = temp.plot(pl_timeMeas, pl_d6t_ref_temp, marker='+', color='c', label="D6T")

    #pl_accel_x = accel_x[-10:]
    #pl_accel_y = accel_y[-10:]
    #pl_accel_z = accel_z[-10:]

    #accel_p1, = accel.plot(pl_timeMeas, pl_accel_x, marker='+', color='r', label="X")
    #accel_p2, = accel.plot(pl_timeMeas, pl_accel_y, marker='+', color='b', label="Y")
    #accel_p3, = accel.plot(pl_timeMeas, pl_accel_z, marker='+', color='g', label="Z")

    #pl_gyro_x = gyro_x[-10:]
    #pl_gyro_y = gyro_y[-10:]
    #pl_gyro_z = gyro_z[-10:]
  
    #gyro_p1, = gyro.plot(pl_timeMeas, pl_gyro_x, marker='+', color='r', label="X")
    #gyro_p2, = gyro.plot(pl_timeMeas, pl_gyro_y, marker='+', color='b', label="Y")
    #gyro_p3, = gyro.plot(pl_timeMeas, pl_gyro_z, marker='+', color='g', label="Z")

    #pl_pressure = pressure[-10:]
    #press_p, = press.plot(pl_timeMeas, pl_pressure, marker='+', color='b')

    #pl_humidity = humidity[-10:]
    #hum_p, = hum.plot(pl_timeMeas, pl_humidity, marker='+', color='g')

    global gps_lat
    global gps_lat_dir
    global gps_long
    global gps_long_dir
    global gps_valid
    global gps_speed    
     
    gps_lat_show = -1
    if len(gps_lat) > 0:
        gps_lat_show = gps_lat[len(gps_lat)-1]    

    gps_lat_dir_show = "U"
    if len(gps_lat_dir) > 0:
        if gps_lat_dir[len(gps_lat_dir)-1] == 0:
            gps_lat_dir_show = "S"
        if gps_lat_dir[len(gps_lat_dir)-1] == 255:
            gps_lat_dir_show = "N"
    
    gps_long_show = -1
    if len(gps_long) > 0:
        gps_long_show = gps_long[len(gps_long)-1]    

    gps_long_dir_show = "U"
    if len(gps_long_dir) > 0:
        if gps_long_dir[len(gps_long_dir)-1] == 0:
            gps_long_dir_show = "E"
        if gps_long_dir[len(gps_long_dir)-1] == 255:
            gps_long_dir_show = "W"
        
    gps_valid_show = False
    if len(gps_valid) > 0:
        if(gps_valid[len(gps_valid)-1] == 0xFF):
            gps_valid_show = True
        else:
            gps_valid_show = False
    
    gps_speed_show = -1
    if len(gps_speed) > 0:
        gps_speed_show = gps_speed[len(gps_speed)-1]

    global ser_on
    global data_logging

    s_status_show     = str(ser_on)
    d_status_show     = str(data_logging)
    gps_lat_show_all  = str(gps_lat_show) + gps_lat_dir_show
    gps_long_show_all = str(gps_long_show) + gps_long_dir_show
    gps_valid_show    = str(gps_valid_show)
    gps_speed_show    = str(gps_speed_show) 


    gps.text(0.05,0.78,"Serial Connection:")
    gps.text(0.05,0.65,"Data Logging")
    gps.text(0.05,0.52,"Latitude:")
    gps.text(0.05,0.39,"Longitude:")
    gps.text(0.05,0.26,"GPS Validity:")
    gps.text(0.05,0.13,"GPS Speed:")

    global sertext
    global dattext
    global gpstxt1
    global gpstxt2
    global gpstxt3
    global gpstxt4

    sertext.set_text(s_status_show)
    dattext.set_text(d_status_show)
    gpstxt1.set_text(gps_valid_show)
    gpstxt2.set_text(gps_lat_show_all)
    gpstxt3.set_text(gps_long_show_all)
    gpstxt4.set_text(gps_speed_show)



    #sertext.set_visible(False)
    #dattext.set_visible(False)
    #gpstxt1.set_visible(False)
    #gpstxt2.set_visible(False)
    #gpstxt3.set_visible(False)
    #gpstxt4.set_visible(False)

    #sertext.set_visible(True)
    #dattext.set_visible(True)
    #gpstxt1.set_visible(True)
    #gpstxt2.set_visible(True)
    #gpstxt3.set_visible(True)
    #gpstxt4.set_visible(True)

def add_buttons(): #adds sensor and cansat control buttons
    but = fig.add_subplot(339) #Serves as base axes for sensor control buttons
    but.set_title("CanSat Control")
    but.axes.get_xaxis().set_visible(False)
    but.axes.get_yaxis().set_visible(False)
    but.spines['right'].set_visible(False)
    but.spines['top'].set_visible(False) 
    but.spines['left'].set_visible(False)
    but.spines['bottom'].set_visible(False)  
    pl_gps      = add_subplot_axes(but, [0,0,0.4,0.4])      #axes for gps toggle button
    pl_sim800l   = add_subplot_axes(but, [0.6,0,0.4,0.4])    #axes for BMP180 toggle button
    pl_login  = add_subplot_axes(but, [0,0.6,0.4,0.4])    #axes for SIM800L toggle button
    pl_clBack    = add_subplot_axes(but, [0.6,0.6,0.4,0.4])  #axes for DHT22 toggle button 
    but_gps     = Button(pl_gps, "GPS Toggle")                     #Instantiates GPS button
    but_login  = Button(pl_login, "Login")               #Instantiates BMP180 button
    but_sim800l = Button(pl_sim800l, "SIM800L Toggle")             #Instantiates SIM800L button
    but_clBack   = Button(pl_clBack, "Delete Data")                 #Instantiates DHT22 button
    but_gps.on_clicked(gps_toggle)                 #gps_toggle is called when GPS button pressed
    but_login.on_clicked(login)           #bmp180_toggle is called when BMP180 button pressed
    but_sim800l.on_clicked(sim800l_toggle)         #sim800l toggle is called whn SIM800L button is pressed
    but_clBack.on_clicked(clBack)             #DHT22_toggle is called when DHT22 button is pressed

    #dummy references to stop python from being a bitch and deleting my buttons
    pl_gps.tgps = but_gps
    pl_login.tlogin = but_login
    pl_sim800l.tsim800l = but_sim800l
    pl_clBack.tclBack = but_clBack


    can = fig.add_subplot(338) #Serves as base axes for CanSat control buttons
    can.set_title("Base Station Control")
    can.axes.get_xaxis().set_visible(False)
    can.axes.get_yaxis().set_visible(False)
    can.spines['right'].set_visible(False)
    can.spines['top'].set_visible(False) 
    can.spines['left'].set_visible(False)
    can.spines['bottom'].set_visible(False)  
    pl_start_chip     = add_subplot_axes(can, [0,0,0.4,0.4])      #axes for gps toggle button
    pl_stop_chip      = add_subplot_axes(can, [0.6,0,0.4,0.4])    #axes for BMP180 toggle button
    pl_clear_data     = add_subplot_axes(can, [0,0.6,0.4,0.4])    #axes for SIM800L toggle button
    pl_delete_backup  = add_subplot_axes(can, [0.6,0.6,0.4,0.4])  #axes for DHT22 toggle button 
    can_start_chip    = Button(pl_start_chip, "Start CanSat")       #Instantiates GPS button
    can_stop_chip     = Button(pl_stop_chip, "Stop CanSat")         #Instantiates BMP180 button
    can_clear_data    = Button(pl_clear_data, "Clear Data")       #Instantiates SIM800L button
    can_delete_backup = Button(pl_delete_backup, "Delete Backup") #Instantiates DHT22 button
    can_start_chip.on_clicked(_start_chip)                #gps_toggle is called when GPS button pressed
    can_stop_chip.on_clicked(_stop_chip)              #bmp180_toggle is called when BMP180 button pressed
    can_clear_data.on_clicked(_clear_data)            #sim800l toggle is called whn SIM800L button is pressed
    can_delete_backup.on_clicked(_delete_backup)           #DHT22_toggle is called when DHT22 button is pressed

    #mo dummy references
    pl_start_chip.stachip = can_start_chip
    pl_stop_chip.stochip = can_stop_chip
    pl_clear_data.cldata = can_clear_data
    pl_delete_backup.delback = can_delete_backup

    
#control methods
def start_chip(): #Opens serial port, starts CHIP code
    if(ser_on == False):
        print "Opening serial port..."
        ser_open()
    print "Starting CHIP code..."
    program_start()

    time.sleep(1)

    #ser_test() #TESTING ONLY

    #On first boot

    chip_state = False
    while chip_state == False:
        read_chip()
        if "Boot Successful" in chip_received:
            print "CHIP code successfully started"
            send_chip("ack")
            chip_state = True
        else:
            print "CHIP error. Expected: 'Boot Successful' Received: '",
            print chip_received,
            print "'"
            send_chip("ls")
        time.sleep(1)
    
    global data_logging
    data_logging = True
    global start_time
    start_time = time.time()

def stop_chip(): #Stops CHIP code, closes serial port
    global data_logging
    data_logging = False
    print "Stopping CHIP code..."
    for i in xrange(5):
       quit_response() 
    chip_ser.close()
    global ser_on
    ser_on = False

def standard_update(): #Goes through process of ONE standard update
    read_chip()
    if chip_received != '':
        update_all()
        empty_response() #CHANGE AFTER UPDATE CODE FINISHED
        append_file()
    
def clear_data(): #Clears all data lists
    global temp_dht22
    temp_dht22 = []
    global humidity
    humidity = []
    global gps_long
    gps_long = []
    global gps_long_dir
    gps_long_dir = []
    global gps_lat
    gps_lat = []
    global gps_lat_dir
    gps_lat_dir = []
    global gps_speed
    gps_speed = []
    global gps_valid
    gps_valid = []
    global temp_bmp180
    temp_bmp180 = []
    global pressure
    pressure = []
    global gyro_x
    gyro_x = []
    global gyro_y
    gyro_y = []
    global gyro_z
    gyro_z = []
    global comp_x
    comp_x = []
    global comp_y
    comp_y = []
    global comp_z
    comp_z = []
    global accel_x
    accel_x = []
    global accel_y
    accel_y = []
    global accel_z
    accel_z = []
    global d6t_ref_temp
    d6t_ref_temp = []
    global d6t_temp_mat
    d6t_temp_mat = []
    global temp_avr
    temp_avr = []
    global cTime
    cTime = 0
    global timeMeas
    timeMeas = []

    temp.clear()
    temp.set_ylabel("Temperature (C)")
    temp.legend()

    accel.clear()
    accel.set_ylabel("Acceleration (ms^-2)")
    accel.legend()

    gyro.clear()
    gyro.set_ylabel("Angular Acceleration (rads^-2)")
    gyro.legend()

    press.clear()
    press.set_ylabel("Pressure (kPa)")

    hum.clear()
    hum.set_ylabel("Humidity (%)")

    global start_time
    start_time = time.time()

def draw_graph(type_of_draw): #Draws GUI, True = show / pause, False = update only
    prep_graph()
    t1 = time.time()
    update_display()
    t2 = time.time()
    #print "update display = ",
    #print t2-t1
    fig.tight_layout()
    if type_of_draw == True:
        t3 = time.time()
        fig.show()
        #fig.canvas.draw_idle()
        plt.pause(0.000000001)
        t4 = time.time()
        #print "show = ",
        #print t4-t3
        #time.sleep(0.3)
    if type_of_draw == False:
        #plt.draw()
        fig.canvas.update()
        fig.canvas.flush_events()
        fig.canvas.draw_idle()


prep_graph()
start_display()
for i in xrange(5):
    draw_graph(True)
    time.sleep(1)
add_buttons()
draw_graph(True)

while True:
    if data_logging == True:
        t1 = time.time()
        standard_update()
        t2 = time.time()
        #print "data fetch time = ",
        #print t2-t1
    t3 = time.time()
    draw_graph(False)
    t4 = time.time()
    #print "draw time = ",
    #print t4-t3
