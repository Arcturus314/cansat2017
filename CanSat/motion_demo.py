import MadgwickAHRS as ahrs
import time


sample_rate = 100

while True:
    global sample_rate
    
    t1 = time.time()
    data = ahrs.get_orientation(sample_rate)
    t2 = time.time()
    sample_rate = 1.0/(t2-t1)


    print "Orientation:",
    print data[0],
    print data[1],
    print data[2]
