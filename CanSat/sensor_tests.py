import datastore

def find_accel_scale(power, update, deflection):
    datastore.set_accelerometer_settings(power,update,deflection)
    adata = datastore.get_accelerometer_data(False)
    vsum = (adata[0]**2.0+adata[1]**2.0+adata[2]**2.0)**0.5
    scale = 9.81/vsum
    return vsum,scale

