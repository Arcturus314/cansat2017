import gsm
import smbus
def send_errs_arduino();
	smbus = SmBus(1)
	ard_addr = 0x0B
	try:
		smbus.write_byte_data(ard_addr, 0x00)
		smbus.write_byte_data(ard_addr, 0x00)
		smbus.write_byte_data(ard_addr, xbee_err)
		smbus.write_byte_data(ard_addr, 0xff)
		smbus.write_byte_data(ard_addr, 0xff)
		smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, lsm303_err)
        	smbus.write_byte_data(ard_addr, 0xff)
        	smbus.write_byte_data(ard_addr, 0xff)
		smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, l3gd20_err)
        	smbus.write_byte_data(ard_addr, 0xff)
        	smbus.write_byte_data(ard_addr, 0xff)
		smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, bme280_err)
        	smbus.write_byte_data(ard_addr, 0xff)
        	smbus.write_byte_data(ard_addr, 0xff)
		smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, 0x00)
        	smbus.write_byte_data(ard_addr, d6t_err)
        	smbus.write_byte_data(ard_addr, 0xff)
        	smbus.write_byte_data(ard_addr, 0xff)	
	Except IOError, err:
