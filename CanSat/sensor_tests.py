import datastore

scale_sum
num

def find_accel_scale(power, update, deflection):
    global scale_sum,num
    datastore.set_accelerometer_settings(power,update,deflection)
    adata = datastore.get_accelerometer_data(False)
    vsum = (adata[0]**2.0+adata[1]**2.0+adata[2]**2.0)**0.5
    scale = 9.81/vsum
    scale_sum = scale_sum + scale
    num = num + 1
    return vsum,scale

def find_mean_scale()
    global scale_sum,num
    return scale_sum/float(num)



