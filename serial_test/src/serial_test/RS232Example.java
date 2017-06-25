package serial_test;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;


public class RS232Example extends Thread{
	int checksumContribution = 0;
	
	public void connect(String portName) throws Exception {
		CommPortIdentifier portIdentifier = CommPortIdentifier.getPortIdentifier(portName);
		
		if (portIdentifier.isCurrentlyOwned()) {
			System.out.println("Port in use");
		} else {
			SerialPort serialPort = (SerialPort) portIdentifier.open("RS232Example", 2000);
			serialPort.setSerialPortParams(115200, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
			CommPortSender.setWriterStream(serialPort.getOutputStream());
			new CommPortReceiver(serialPort.getInputStream()).start();
		}
	}
	
	public static void main(String[] args) throws Exception {
		new RS232Example().connect("COM11");
		while(true) {
			if(Container.getInstance().read == false && Container.getInstance().message != null) {
				//System.out.println("New message received: " + Container.getInstance().message) ;
				String[] processed_message = {" "," "," "};
				processed_message = processMessage(Container.getInstance().message);
				//for(int i = 0; i < 3; i++) {
					//System.out.println(i + " " + processed_message[i]);
				//}
				processBody(processed_message[1]);
				Container.getInstance().read = true;
				
			}
			Thread.sleep(100);
		}
	}
	
	public static String[] processMessage(String message) { //returns [header, body, footer]
		String[] returnArray = {" "," "," "};
		try {
			String[] withoutStart = message.split("\\:");
			//System.out.println("message body: " + withoutStart[1]);
			String[] separated = withoutStart[1].split("\\|");
			for(int i = 0; i < 3; i++) { //the definition of bad code
				String temp = separated[i];
			}
			returnArray =  separated;
			
		}
		catch (Exception e) {
			System.out.println("PARSING ERROR");
		} 
		finally {
			return returnArray;
		}
	}
	
	public static void processBody(String bodyString) {
		try {
			bodyString = bodyString.replace("(", ""); //removing unnecessary characters
			bodyString = bodyString.replace(")", "");
			bodyString = bodyString.replace("[", "");
			bodyString = bodyString.replace("]", "");
			String[] messages = bodyString.split("\\;");
			
			for(int i = 0; i < messages.length-1; i++) {
				String[] messageComponents = messages[i].split(",");
				//going through individual packet types
				if(tf(messageComponents[0]) == 1 && tf(messageComponents[1]) == 1) {
					//single accelerometer value
					float accel_x = tf(messageComponents[2]);
					float accel_y = tf(messageComponents[3]);
					float accel_z = tf(messageComponents[4]);
					float accel_time = tf(messageComponents[5]);
					System.out.println("Accel_X: " + accel_x + " Accel_Y: " + accel_y + " Accel_Z: " + accel_z + " Accel_Time: " + accel_time);
				}
				if(tf(messageComponents[0]) == 2 && tf(messageComponents[1]) == 1) {
					//single magnetometer value
					float mag_x = tf(messageComponents[2]);
					float mag_y = tf(messageComponents[3]);
					float mag_z = tf(messageComponents[4]);
					float mag_time = tf(messageComponents[5]);
					System.out.println("Mag_X: " + mag_x + " Mag_Y: " + mag_y + "Mag_Z: " + mag_z + " Mag_Time: " + mag_time);
				}
				if(tf(messageComponents[0]) == 3 && tf(messageComponents[1]) == 1) {
					//single gyroscope value
					float gyro_x = tf(messageComponents[2]);
					float gyro_y = tf(messageComponents[3]);
					float gyro_z = tf(messageComponents[4]);
					float gyro_time = tf(messageComponents[5]);
					System.out.println("Gyro_X: " + gyro_x + " Gyro_Y: " + gyro_y + " Gyro_Z: " + gyro_z + " Gyro_Time: " + gyro_time);
				}	
				if(tf(messageComponents[0]) == 4 && tf(messageComponents[1]) == 1) {
					//single imu temperature value
					float imu_temp = tf(messageComponents[2]);
					float imu_time = tf(messageComponents[3]);
					System.out.println("IMU_temp: " + imu_temp + " IMU_time: " + imu_time);
				}
				if(tf(messageComponents[0]) == 5 && tf(messageComponents[1]) == 1) {
					//single pressure value
					float env_pres = tf(messageComponents[2]);
					float env_time = tf(messageComponents[3]);
					System.out.println("env_pres: " + env_pres + " env_time: " + env_time);
				}
				if(tf(messageComponents[0]) == 6 && tf(messageComponents[1]) == 1) {
					//single humidity value
					float env_hum = tf(messageComponents[2]);
					float env_time = tf(messageComponents[3]);
					System.out.println("env_hum: " + env_hum + " env_time: " + env_time);
				}
				if(tf(messageComponents[0]) == 7 && tf(messageComponents[1]) == 1) {
					//single env temp value
					float env_temp = tf(messageComponents[2]);
					float env_time = tf(messageComponents[3]);
					System.out.println("env_temp: " + env_temp + " env_time: " + env_time);
				}
				if(tf(messageComponents[0]) == 8 && tf(messageComponents[1]) == 0) {
					//single set of error values
					boolean accel_error = false;
					boolean mag_error   = false;
					boolean gyro_error  = false;
					boolean env_error   = false;
					boolean cam_error   = false;
					
					//for(i=0;i<5;i++) {
						//System.out.println(messageComponents[2+i]);
					//}
					
					if(messageComponents[2] == "False" || messageComponents[2] == " False")
						accel_error = true;
					if(messageComponents[3] == "False" || messageComponents[2] == " False")
						mag_error = true;
					if(messageComponents[4] == "False" || messageComponents[2] == " False")
						gyro_error = true;
					if(messageComponents[5] == "False" || messageComponents[2] == " False")
						env_error = true;
					if(messageComponents[6] == "False" || messageComponents[2] == " False")
						cam_error = true;
					System.out.println("ERRORS: Accel " + accel_error + " Mag " + mag_error + " Gyro " + gyro_error + " Env " + env_error + " Cam " + cam_error);
				}
				if(tf(messageComponents[0]) == 9 && tf(messageComponents[1]) == 0) {
					//single position value
					float trans_x    = tf(messageComponents[2]);
					float trans_y    = tf(messageComponents[3]);
					float trans_alt  = tf(messageComponents[4]);
					float trans_time = tf(messageComponents[5]);
					float or_head    = tf(messageComponents[6]);
					float or_x       = tf(messageComponents[7]);
					float or_y       = tf(messageComponents[8]);
					float or_time    = tf(messageComponents[9]);
					float gps_fix    = tf(messageComponents[10]);
					float gps_spd    = tf(messageComponents[11]);
					float gps_alt    = tf(messageComponents[12]);
					float gps_x      = tf(messageComponents[13]);
					float gps_y      = tf(messageComponents[14]);
					float gps_time   = tf(messageComponents[15]);
				}
				if(tf(messageComponents[0]) == 10 && tf(messageComponents[1]) == 0) {
					//single thermal camera value
					float[] pixels = new float[16];
					for(int j = 0; i < 16; i++) {
						pixels[j] = tf(messageComponents[j+2]);
					}
					float d6t_temp = tf(messageComponents[18]);
					float d6t_time = tf(messageComponents[19]);
				}
				if(tf(messageComponents[0]) == 11 && tf(messageComponents[1]) == 0) {
					//single thermal map pixel value
					float pix_temp[] = new float[16];
					float pix_x[] = new float[16];
					float pix_y[] = new float[16];
					float size[] = new float[16];
					for(i=0; i<16; i++) {
						pix_temp[i] = tf(messageComponents[2+i]);
						pix_x[i]    = tf(messageComponents[3+i]);
						pix_y[i]    = tf(messageComponents[4+i]);
						size[i]     = tf(messageComponents[5+i]);
					}
				}
			}
			
			
		}
		catch (Exception e) {
			System.out.println("BODY PROCESSING ERROR");
		} 
		finally {
		}
	}
	
	public static float tf(String str) {
		return Float.parseFloat(str);
			
	}
}


