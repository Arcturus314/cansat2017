package cansat;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class DecodeData {
	private String newFile;
	private String[] newDocSplit;
	private int newNumberOfDataSets;
	private int oldNumberOfDataSets;
	private String header, body, footer;
	
	private String[][] axis = new String[][]{
	    {"time","temperature"},{"time","pressure"}, {"time","humidity"},{"time","acceleration magnitude"}, {"x","y"},{"x","z"}, {"y","z"}
	};
	
	static Float[][][] axisValues = new Float[7][2][1];
	//private static List<List<List<Float>>> axisValues = new ArrayList<List<List<Float>>>();  
	private static List<Float> temperature = new ArrayList<Float>();
	public static List<Float> pressure = new ArrayList<Float>();
	public static List<Float> humidity = new ArrayList<Float>();
	public static List<Float> acceleration_magnitude = new ArrayList<Float>();
	public static List<Float> x = new ArrayList<Float>();
	public static List<Float> y = new ArrayList<Float>();
	public static List<Float> z = new ArrayList<Float>();
	public static List<Float> time = new ArrayList<Float>();
	private int tick;

	public DecodeData(String path){
		//split doc
		newFile = Utils.readFile("assets/test.txt");
		newDocSplit = newFile.split(":");
		newDocSplit = Utils.removeArrayFirstElement(newDocSplit);
		newNumberOfDataSets = newDocSplit.length;
		
		//Change status of status 0
		//StatusButton.statusButtons.get(0).toggle(true);
		
		//add data set
		DataSet dataSet1 = new DataSet("header1", "body1", "footer1");
		DataSet dataSet2 = new DataSet("header2", "body2", "footer2");

		//add vales
		for(int i = 0; i < 100000; i++){
			Random rn = new Random();
			float answer1 = (float)rn.nextInt(300+300) -300  ;
			float answer2 = (float)rn.nextInt(300+300) -300  ;
			float answer3 = (float)rn.nextInt(300+300) -300  ;
			TempValue TempValue1 = new TempValue(0.0f, answer1, answer2, answer3);
		}
		
		tick = MainLoop.getTick();
	
		//Add to main values 
		time.add((float) tick);
		float timeLastValue = time.get(time.size() - 1);
		temperature.add(timeLastValue);
		pressure.add(timeLastValue);
		humidity.add(timeLastValue);
		acceleration_magnitude.add(timeLastValue);
		x.add(timeLastValue);
		y.add(timeLastValue);
		z.add(timeLastValue);
		
		//Update 3D array lists 
		axisValues[0][1][0] = time.get(time.size() - 1);
		axisValues[0][0][0] = temperature.get(temperature.size() - 1);
		axisValues[1][1][0] = time.get(time.size() - 1);
		axisValues[1][0][0] = pressure.get(pressure.size() - 1);
		axisValues[2][1][0] = time.get(time.size() - 1);
		axisValues[2][0][0] = humidity.get(humidity.size() - 1);
		axisValues[3][1][0] = time.get(time.size() - 1);
		axisValues[3][0][0] = acceleration_magnitude.get(acceleration_magnitude.size() - 1);
		axisValues[4][1][0] = x.get(x.size() - 1);
		axisValues[4][0][0] = y.get(y.size() - 1);
		axisValues[5][1][0] = x.get(x.size() - 1);
		axisValues[5][0][0] = z.get(z.size() - 1);
		axisValues[6][1][0] = y.get(y.size() - 1);
		axisValues[6][0][0] = z.get(z.size() - 1);

	}
		
		public static float getAxis(int graphIndex, int axisIndex ){
			return axisValues[graphIndex][axisIndex][0];
		}
			
}
