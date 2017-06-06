import datastore

scale_sum = 0
num = 0 
x_total = 0
y_total = 0
z_total = 0
def find_accel_scale(power, update, deflection):
    global scale_sum,num
    datastore.set_accelerometer_settings(power,update,deflection)
    adata = datastore.get_accelerometer_data(False)
    vsum = (adata[0]**2.0+adata[1]**2.0+adata[2]**2.0)**0.5
    scale = 9.81/vsum
    scale_sum = scale_sum + scale
    num = num + 1
    return vsum,scale
def find_mean_scale():
    global scale_sum,num
    return scale_sum/float(num)
def reset():
    scale_sum=0
    num=0
    x_total=0
    y_total=0
    z_total=0
def test_gyro():
    global num,x_total,y_total,z_total
    gdata = datastore.get_accelerometer_data(False)
    x_total = x_total + gdata[0]
    y_total = y_total + gdata[1]
    z_total = z_total + gdata[2]
    num = num + 1
    return gdata[0], gdata[1], gdata[2]
def find_gyro_means():
    return x_total/float(num),y_total/float(num),z_total/float(num)



def find_mag_scale(power, update, deflection):
    global scale_sum,num
    datastore.set_magnetometer_settings(power,update,deflection)
    adata = datastore.get_magnetometer_data(False)
    vsum = (adata[0]**2.0+adata[1]**2.0+adata[2]**2.0)**0.5
    return adata[0],adata[1],adata[2],vsum
   

