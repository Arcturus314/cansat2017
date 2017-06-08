package cansat;

public class DecodeData {
	private String newFile;
	private String[] newDocSplit;
	private int newNumberOfDataSets;
	private int oldNumberOfDataSets;
	private String header, body, footer;

	public DecodeData(String path){	
		newFile = Utils.readFile("assets/test.txt");
		newDocSplit = newFile.split(":");
		newDocSplit = Utils.removeArrayFirstElement(newDocSplit);
		newNumberOfDataSets = newDocSplit.length;
		
		header = "test"; 
		body = "test";
		footer = "test";
		
		for(int i = 0; i < newNumberOfDataSets; i++){
			//DataSet dataSet = new DataSet(header, body, footer);
			//MainLoop.dataSetArray.add(dataSet); 
		}
	}
	
	
	
}
