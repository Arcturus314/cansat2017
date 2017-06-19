package serial_test;

import java.io.IOException;
import java.io.InputStream;

public class CommPortReceiver extends Thread {

	InputStream in;
	Protocol protocol = new ProtocolImpl();
	
	public CommPortReceiver(InputStream in) {
		this.in = in;
	}
	
	public void run() {
		try {
			int b;
			while(true) {
				while ((b = in.read()) != -1) {
					protocol.onReceive((byte) b);
				}
				protocol.onStreamClosed();
				sleep(10);
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
}

