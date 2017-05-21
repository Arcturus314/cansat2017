class I2C_3axis_Sensor: #OR setParam(p,u,d) readX() readY() readZ()
    #provides a simple "base" class for sensors drivers to be built on
    #classes extending I2C_Sensor must override methods:
    #   setParam
    #   readX
    #   readY
    #   readZ

    import smbus

    def __init__(self, addr, power, update, deflection):
        #Linear calibration factor
        #Of form val_new = scale*val_old + offset
        self.x_scale = 1
        self.y_scale = 1
        self.z_scale = 1
        self.x_offset = 1
        self.y_offset = 1
        self.z_offset = 1
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
            bus = smBus.SMBus(1) #smbus declared on CHIP I2C bus 1
            setParam(power, update, deflection)
            self.dev_state = True
        except IOError, err:
            self.dev_state = False

    def applyCal(val, scale, offset):
        return float(val)*float(scale)+float(offset)
    def mergeInts(low, high)
        return (low>>8) | high

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

    def getState():
        return self.dev_state
    def getPower():
        return self.p_mode
    def getUpdate():
        return self.u_mode
    def getDefl():
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

class LSM303_Accel(I2C_3axis_Sensor):

    def setParam(self, power, update, deflection):
        #setting class variables
        self.p_mode = power
        self.u_mode = update
        self.d_mode = deflection
        
        #calculating control register values
        ctrlreg1 = 0b00000111 #pwrmode | datarate | xyz enable
        if u_mode = True:
            ctrlreg1 = ctrlreg1 | 0b00001000
        if p_mode = True:
            ctrlreg1 = ctrlreg1 | 0b00100000
        ctrlreg4 = 0b00000000 #bdu | ble | fsd | st
        if d_mode = True:
            ctrlreg4 = ctrlreg4 | 0b00110000

        #Setting device register values
        write_byte_data(0x20, ctrlreg1)
        write_byte_data(0x23, ctrlreg4)     
   
    def readX(self):
        low  = read_byte_data(0x28)
        high = read_byte_data(0x29)
        return applYCal(mergeInts(low, high), self.x_scale, self.x_offset)
    def readY(self):
        low  = read_byte_data(0x2A)
        high = read_byte_data(0x2B)
        return applyCal(mergeInts(low, high), self.y_scale, self.y_offset)
    def readZ(self)
        low  = read_byte_data(0x2C)
        high = read_byte_data(0x2D)
        return applyCal(mergeInts(low, high), self.z_scale, self.z_offset)

class LSM303_Mag(I2C_3Axis_Sensor):
    #TODO: override setParam(power, update, displacement)        
    def readCompX(self):
        low  = read_byte_data(0x03)
        high = read_byte_data(0x04)
        return applyCal(mergeInts(low, high), self.x_scale, self.x_offset)
    def readCompY(self):
        low  = read_byte_data(0x05)
        high = read_byte_data(0x06)
        return applyCal(mergeInts(low, high), self.y_scale, self.y_offset)
    def readCompZ(self):A
        low  = read_byte_data(0x07)
        high = read_byte_data(0x08)
        return applyCal(mergeInts(low, high), self.z_scale, self.z_offset)

class L3GD20(I2C_3Axis_Sensor):
