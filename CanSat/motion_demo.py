import position

position_data = [0,0,0] #heading,roll,pitch

position.init_data()

while True:
    global position_data
    data = position.get_pos_data(False)
    position_data[0] = data[0][0]
    position_data[1] = data[0][1]
    position_data[2] = data[0][2]

    print "Orientation:",
    print data[0],
    print data[1],
    print data[2]
