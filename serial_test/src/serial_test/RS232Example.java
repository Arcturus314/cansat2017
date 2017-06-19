package serial_test;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;


public class RS232Example extends Thread{
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
		new RS232Example().connect("COM6");
		CommPortSender.send(new ProtocolImpl().getMessage("\n"));
		CommPortSender.send(new ProtocolImpl().getMessage("chip"));
		sleep(2000);
		CommPortSender.send(new ProtocolImpl().getMessage("chip"));
		sleep(2000);
		CommPortSender.send(new ProtocolImpl().getMessage("python test.py"));
	}
}


