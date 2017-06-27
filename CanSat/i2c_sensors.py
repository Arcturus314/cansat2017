import smbus
import bme280
bus = smbus.SMBus(1) #smbus declared on CHIP I2C bus 1
dec_places = 3 #number of decimal places for data points

class I2C_Sensor: #OR read()
    #Provides a "base" class for 1d sensors to build on
    #override read()
    global smbus
    global bus
    global dec_places

    def __init__(self, addr):
        self.scale = 1
        self.offset = 0
        self.dev_addr = addr
        self.dev_state = True #True if no comms error, false if comms error

        try:
            #smbus declaration
            self.dev_state = True
        except IOError, err:
            self.dev_state = False

    def read_byte_data(self, command):
        data = 0
        try:
            data = bus.read_byte_data(self.dev_addr, command)
            self.dev_state = True
        except IOError, err:
            self.dev_state = False 
        return data

    def write_byte_data(self, command, value):
       try:
            bus.write_byte_data(self,dev_addr, command, value)
            self.dev_state = True
       except IOError, err:
            self.dev_state = False 

    def mergeInts(self, low, high):
        val = (high << 8) | low
        if val >= 2**15:
            val = -1*(2**16 - val)
        return val

    def applyCal(self, val):
        return round(float(val)*float(self.scale)+float(self.offset),dec_places)

    def getState(self):
        return self.dev_state

    def setCal(self, s, o):
        self.scale = s
        self.offset = o 
    def read():
        return None    

class I2C_3Axis_Sensor: #OR setParam(p,u,d) readX() readY() readZ()
    #provides a simple "base" class for sensors drivers to be built on
    #classes extending I2C_Sensor must override methods:
    #   setParam
    #   readX
    #   readY
    #   readZ

    global smbus
    global bus
    global dec_places
    def applyCal(self, val, scale, offset):
        return round(float(val)*float(scale)+float(offset),dec_places)

    def mergeInts(self, low, high):
        val = (high << 8) | low
        if val >= 2**15:
            val = -1*(2**16 - (val))
        return val

    def read_byte_data(self, command):
        data = 0
        try:
            data = bus.read_byte_data(self.dev_addr, command) 
            self.dev_state = True
        except IOError, err:
            self.dev_state = False
        return data
    def write_byte_data(self, command, value):
        try:
            bus.write_byte_data(self.dev_addr, command, value)
            self.dev_state = True
        except IOError, err:
            self.dev_state = False

    def getState(self):
        return self.dev_state
    def getPower(self):
        return self.p_mode
    def getUpdate(self):
        return self.u_mode
    def getDefl(self):
        return self.d_mode

    def setParam(self, power, update, deflection):
        return None
    def setCal(self, xs, ys, zs, xo, yo, zo):
        self.x_scale = xs
        self.y_scale = ys
        self.z_scale = zs
        self.x_offset = xo
        self.y_offset = yo
        self.z_offset = zo    

    def readX():
        return None
    def readY():
        return None
    def readZ():
        return None

    def __init__(self, addr, power, update, deflection):
        #Linear calibration factor
        #Of form val_new = scale*val_old + offset
        self.x_scale = 1
        self.y_scale = 1
        self.z_scale = 1
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        #i2c device adress
        self.dev_addr = addr
        #Device parameters
        self.p_mode = True #Power mode; True = high power, False = low power
        self.u_mode = True #Update mode; True = fast update, False = slow update
        self.d_mode = True #fsd mode; True = high max fsd, False = low max fsd
        #Device State
        self.dev_state = True #True if no comms error, false if comms error

        try:
            #smbus declaration
            self.setParam(power, update, deflection)
            self.dev_state = True
        except IOError, err:
            self.dev_state = False

class LSM303_Accel(I2C_3Axis_Sensor):

    def setParam(self, power, update, deflection):
        #setting class variables
        self.p_mode = power
        self.u_mode = update
        self.d_mode = deflection
        
        #calculating control register values
        ctrlreg1 = 0b00000111 #pwrmode | datarate | xyz enable
        if self.u_mode == True:
            ctrlreg1 = ctrlreg1 | 0b00001000
        if self.p_mode == True:
            ctrlreg1 = ctrlreg1 | 0b00100000
        ctrlreg4 = 0b00000000 #bdu | ble | fsd | st
        if self.d_mode == True:
            ctrlreg4 = ctrlreg4 | 0b00110000

        #Setting device register values
        self.write_byte_data(0x20, ctrlreg1)
        self.write_byte_data(0x23, ctrlreg4)     
   
    def readX(self):
        scale = 0.1217612729
        if self.getDefl() == False:
            scale = 0.0097113970
        low  = self.read_byte_data(0x28)
        high = self.read_byte_data(0x29)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.x_scale, self.x_offset)
    def readY(self):
        scale = 0.1217612729
        if self.getDefl() == False:
            scale = 0.0097113970
        low  = self.read_byte_data(0x2A)
        high = self.read_byte_data(0x2B)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.y_scale, self.y_offset)
    def readZ(self):
        scale = 0.1217612729
        if self.getDefl() == False:
            scale = 0.0097113970
        low  = self.read_byte_data(0x2C)
        high = self.read_byte_data(0x2D)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.z_scale, self.z_offset)

class LSM303_Mag(I2C_3Axis_Sensor):
    def setParam(self, power, update, deflection):  
        reg1 = 0b00010000 #data update rate
        reg2 = 0b00100000 #fsd
        reg3 = 0b00000011 #sleep mode
        if power == True:
            reg3 = 0b00000000
        if update == True:
            reg1 = 0b00011000
        if deflection == True:
            reg2 = 0b11100000
        self.write_byte_data(0x02,reg3)
        self.write_byte_data(0x00,reg1)
        self.write_byte_data(0x01,reg2)
        
    def readX(self):
        scale = 1.0/1055.0
        if self.getDefl() == True:
            scale = 1.0/230.0
        low  = self.read_byte_data(0x03)
        high = self.read_byte_data(0x04)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.x_scale, self.x_offset)
    def readY(self):
        scale = 1.0/1055.0
        if self.getDefl() == True:
            scale = 1.0/230.0
        low  = self.read_byte_data(0x05)
        high = self.read_byte_data(0x06)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.y_scale, self.y_offset)
    def readZ(self):
        scale = 1.0/1055.0
        if self.getDefl() == True:
            scale = 1.0/230.0
        low  = self.read_byte_data(0x07)
        high = self.read_byte_data(0x08)
        return self.applyCal(scale*self.mergeInts(low, high)/16, self.z_scale, self.z_offset)

class L3GD20_Gyro(I2C_3Axis_Sensor):
    def setParam(self, power, update, deflection):
        #Setting class variables
        self.p_mode = power
        self.u_mode = update
        self.d_mode = deflection
        
        #Calculating control register values
        ctrlreg1 = 0b00000111
        if self.u_mode == True:
            ctrlreg1 = ctrlreg1 | 0b11110111
        if self.p_mode == True:
            ctrlreg1 = ctrlreg1 | 0b00001000

        #Setting device register values
        self.write_byte_data(0x20, ctrlreg1)

    def readX(self):
        low  = self.read_byte_data(0x28)
        high = self.read_byte_data(0x29)
        val = self.mergeInts(low,high)
        if val > 2047: val = val - 4096
        val = float(val)*0.00875
        return self.applyCal(val, self.x_scale, self.x_offset)
    def readY(self):
        low  = self.read_byte_data(0x2A)
        high = self.read_byte_data(0x2B)
        val = self.mergeInts(low,high)
        if val > 2047: val = val - 4096
        val = float(val)*0.00875
        return self.applyCal(val, self.y_scale, self.y_offset)
    def readZ(self):
        low  = self.read_byte_data(0x2C)
        high = self.read_byte_data(0x2D)
        val = self.mergeInts(low,high)
        if val > 2047: val = val - 4096
        val = float(val)*0.00875
        return self.applyCal(val, self.z_scale, self.z_offset)

class L3GD20_Temp(I2C_Sensor):
    def read(self):
        temp = self.read_byte_data(0x26)
        #if temp > 255:
        #    temp = 25 + (255-temp)
        #else:
        #    temp = 25 - temp
        #if temp < 0:
        #    temp = 255 - temp
        #else:
        #    temp = 25 - temp
        if temp > 200:
            temp = 25 + (255-temp)
        return self.applyCal(temp) 
        #print bin(self.read_byte_data(0x26))

class BME280_Pressure(I2C_Sensor):
    def read(self):
        global bme280
        return self.applyCal(bme280.getPressure())

class BME280_Humidity(I2C_Sensor):
    def read(self):
        global bme280
        return self.applyCal(bme280.getHumidity())

class BME280_Temp(I2C_Sensor):
    def read(self):
        global bme280
        return self.applyCal(bme280.getTemp())

class D6T_Temp_Array(I2C_Sensor):
    def read(self):
        D6T_data = []
        return_data = []
        for i in xrange(40):
            D6T_data.append(0)
        for i in xrange(17):
            return_data.append(0)
        self.dev_state = True
        try:
            D6T_data = bus.read_i2c_block_data(self.dev_addr, 0x4C)
        except IOError,err:
            self.dev_state = False
        if self.dev_state == True:
            sumt = 0 #sum of temperatures for 16th element calc
            for i in xrange(16):
                return_data[i] = self.applyCal((float(D6T_data[2*i]) + 256.0*float(D6T_data[2*i+1]))/10.0)
                if i>0:
                    sumt = sumt + return_data[i]
            return_data[16] = sumt / 15.0
        return return_data[1:17], return_data[0]


        
