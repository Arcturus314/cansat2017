import position
import time

position_data = [0,0,0] #heading,roll,pitch

position.init_data()
sample_rate = 100

while True:
    global sample_rate
    global position_data

    t1 = time.time()
    position.calc_bimu_orientation(sample_rate)
    data = position.get_last_or_pos()
    position_data[0] = data[0]
    position_data[1] = data[1]
    position_data[2] = data[2]

    print "Orientation:",
    print position_data[0],
    print position_data[1],
    print position_data[2]
    t2 = time.time()
    sample_rate = t2-t1
