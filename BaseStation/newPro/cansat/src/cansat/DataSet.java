package cansat;

import java.util.ArrayList;
import java.util.List;

public class DataSet {

	public static List<DataSet> dataSets  = new ArrayList<DataSet>();
	public String header;
	public String body;
	public String footer;
	
	
	public DataSet(String Header, String Body, String Footer) {
		this.header = Header;
		this.body = Body;
		this.footer = Footer;
		
		dataSets.add(this); 
	}
	
	
	

}
