import position
import datastore
import math

dtr = 0.0174532925199 #degrees to radians scaling factor

#Looking from the CanSat down packets are arranged as such
#P00  P01  P02  P03
#P04  P05  P06  P07
#P08  P09  P10  P11
#P12  P13  P14  P15

#We also need to quantify (in degrees) the offset between pixels
#Given in a dictionary, with the key giving the name of the pixel, and with offsets given in the tuple (x,y)

offsets = {0:(-22.5,22.5), 1:(-7.5,22.5), 2:(7.5,22.5), 3:(22.5,22.5), 4:(-22.5,7.5), 5:(-7.5,7.5), 6:(7.5,7.5), 7:(22.5,7.5), 8:(-22.5,-7.5), 9:(-7.5,-7.5), 10:(7.5,-7.5), 11:(22.5,-7.5), 12:(-22.5,-22.5), 13:(-7.5,-22.5), 14:(7.5,-22.5), 15:(22.5,22.5)}

#four values will be returned as a part of each pixel
#   1. Temperature
#   2. x-coordinate of the pixel center
#   3. y-coordinate of the pixel center
#   4. scale factor: side length of a square representing the pixel#      area, with the center of the square being the pixel center

#Pixel data will be stored in this list, as raw tuple values
map_raw = []

position_data = [(0,0,0,0),(0,0,0,0),(0,0,0,0,0,0)] 
temp_matrix = []

dec_places = 3

def init_data():
    position.init_data()

def get_position():
    global position_data
    position_data = position.get_pos_data(False)

def get_temp_matrix():
    global temp_matrix
    temp_matrix = datastore.get_temp_array_data(False)[0][0] #will return only the temperature matrix, not time or internal D6T temperature

def calc_size(height,x_tilt,y_tilt,pixel):
    global offsets
    size = height*math.sqrt(abs((math.tan(dtr*(x_tilt+offsets[pixel][0])))**2.0 + math.tan((math.tan(dtr*(x_tilt+offsets[pixel][1]))))))
    return round(size,dec_places)

def calc_coordinate(height,x_pos,y_pos,x_tilt,y_tilt,heading,pixel):
    global offsets,position_data
    x = height*math.tan(dtr*(y_tilt*math.cos(dtr*heading)+x_tilt*math.cos(dtr*(90.0-heading))+offsets[pixel][0]*math.cos(dtr*heading)-offsets[pixel][1]*math.sin(dtr*heading))) + x_pos
    y = height*math.tan(dtr*(y_tilt*math.sin(dtr*heading)+x_tilt*math.sin(dtr*(90.0-heading))+offsets[pixel][0]*math.sin(dtr*heading)+offsets[pixel][1]*math.cos(dtr*heading))) + y_pos
    return round(x,dec_places),round(y,dec_places)

def build_frame(): 
    get_position()
    get_temp_matrix()
    for i in xrange(16):
        height  = position_data[0][2]
        x_pos   = position_data[0][0]
        y_pos   = position_data[0][1]
        heading = position_data[1][0]
        x_tilt  = position_data[1][1]
        y_tilt  = position_data[1][2]
        size = calc_size(height,x_tilt,y_tilt,i)
        coordinates = calc_coordinate(height,x_pos,y_pos,x_tilt,y_tilt,heading,i)
        temp = temp_matrix[i]
        map_raw.append((temp,coordinates[0],coordinates[1],size))

def return_frame(type):
    if type == True:
        return map_raw
    else:
        return_vals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if len(map_raw) > 15:
            for i in xrange(16):
                return_vals[i] = map_raw[len(map_raw)-1-i]
        return return_vals

