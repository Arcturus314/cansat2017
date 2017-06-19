package serial_test;

public interface Protocol {
	void onReceive(byte b);
	void onStreamClosed();
}
