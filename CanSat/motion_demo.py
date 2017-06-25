import MadgwickAHRS as ahrs
import time

position_data = [0,0,0] #heading,roll,pitch

sample_rate = 100

while True:
    global sample_rate
    global position_data
    
    for i in xrange(10):
        t1 = time.time()
        data = ahrs.get_orientation(sample_rate)
        position_data[0] = data[0]
        position_data[1] = data[1]
        position_data[2] = data[2]
        t2 = time.time()
        sample_rate = t2-t1


    print "Orientation:",
    print position_data[0]/10.0,
    print position_data[1]/10.0,
    print position_data[2]/10.0
