package cansat;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class DecodeData {
	public static String[] Status;
	
	private String[][] axis = new String[][]{
	    {"time","temperature"},{"time","pressure"}, {"time","humidity"},{"time","acceleration magnitude"}, {"x","y"},{"x","z"}, {"y","z"}
	};
	
	public static Float[][][] axisValues = new Float[7][2][4];
	private static List<Float> tempAverageTime = new ArrayList<Float>();
	private static List<Float> tempImuTime = new ArrayList<Float>();
	private static List<Float> tempD6tTime = new ArrayList<Float>();
	private static List<Float> tempEnvTime = new ArrayList<Float>();
	private static List<Float> tempAverage = new ArrayList<Float>();
	private static List<Float> tempImu = new ArrayList<Float>();
	private static List<Float> tempD6t = new ArrayList<Float>();
	private static List<Float> tempEnv = new ArrayList<Float>();
	
	private static List<Float> pressureTime = new ArrayList<Float>();
	public static List<Float> pressure = new ArrayList<Float>();
	private static List<Float> humidityTime = new ArrayList<Float>();
	public static List<Float> humidity = new ArrayList<Float>();
	public static List<Float> acceleration_magnitudeTime = new ArrayList<Float>();
    public static List<Float> acceleration_magnitude = new ArrayList<Float>();
	
	public static List<Float> x = new ArrayList<Float>();
	public static List<Float> y = new ArrayList<Float>();
	public static List<Float> z = new ArrayList<Float>();
	public static List<Float> time = new ArrayList<Float>();
	
	public static List<Double> lat = new ArrayList<Double>();
	public static List<Double> lon = new ArrayList<Double>();
	private int tick;

	public DecodeData(String path){
		

		//Change status of status 0
		//StatusButton.statusButtons.get(0).toggle(true);
		
		//Add data set
		DataSet dataSet1 = new DataSet("header1", "body1", "footer1");
		DataSet dataSet2 = new DataSet("header2", "body2", "footer2");
		
		//Add vales to TempMap
		for(int i = 0; i < 5; i++){
			Random rn = new Random();
			float answer0 = (float)rn.nextInt(50) -5  ;
			float answer1 = (float)rn.nextInt(300+300) -300  ;
			float answer2 = (float)rn.nextInt(300+300) -300  ;
			float answer3 = (float)rn.nextInt(300+300) -300  ;
			TempValue tempValue = new TempValue(answer0, answer1, answer2, answer3);
		}
		
		//TempValue tempValue = new TempValue(5.5f, -150, -20, 100);
		
		tick = MainLoop.getTick();
		
		//Status Values 
		Status = new String[]{"True","True","100%", "True", "?"};
		
		//Gps
		lat.add((55.9573845 + (tick / 1000.0)));
		lon.add((-3.1860419 + (tick / 1000.0)));
		
		time.add((float) tick);
		float timeLastValue = time.get(time.size() - 1);

		//Graph
		tempAverageTime.add(timeLastValue);
		tempImuTime.add(timeLastValue);
		tempD6tTime.add(timeLastValue);
		tempEnvTime.add(timeLastValue);
		tempAverage.add(timeLastValue);
		tempImu.add(timeLastValue);
		tempD6t.add(timeLastValue);
		tempEnv.add(timeLastValue);
		pressureTime.add(timeLastValue);
		pressure.add(timeLastValue);
		humidityTime.add(timeLastValue);
		humidity.add(timeLastValue);
		acceleration_magnitudeTime.add(timeLastValue);
		acceleration_magnitude.add(timeLastValue);
		x.add(timeLastValue);
		y.add(timeLastValue);
		z.add(timeLastValue);
		
		//Update 3D array lists for Graphs
		// [Graph] [Axis] [Series]
		axisValues[0][1][0] = tempAverageTime.get(tempAverageTime.size() - 1);
		axisValues[0][1][1] = tempImuTime.get(tempImuTime.size() - 1);
		axisValues[0][1][2] = tempD6tTime.get(tempD6tTime.size() - 1);
		axisValues[0][1][3] = tempAverage.get(tempAverage.size() - 1);
		axisValues[0][0][0] = tempAverage.get(tempAverage.size() - 1);
		axisValues[0][0][1] = tempImu.get(tempImu.size() - 1) + 5;
		axisValues[0][0][2] = tempD6t.get(tempD6t.size() - 1) + 10;
		axisValues[0][0][3] = tempEnv.get(tempEnv.size() - 1) + 15;
		axisValues[1][1][0] = pressureTime.get(pressureTime.size() - 1);
		axisValues[1][0][0] = pressure.get(pressure.size() - 1);
		axisValues[2][1][0] = humidityTime.get(humidityTime.size() - 1);
		axisValues[2][0][0] = humidity.get(humidity.size() - 1);
		axisValues[3][1][0] = acceleration_magnitudeTime.get(acceleration_magnitudeTime.size() - 1);
		axisValues[3][0][0] = acceleration_magnitude.get(acceleration_magnitude.size() - 1);
		axisValues[4][1][0] = x.get(x.size() - 1);
		axisValues[4][0][0] = y.get(y.size() - 1);
		axisValues[5][1][0] = x.get(x.size() - 1);
		axisValues[5][0][0] = z.get(z.size() - 1);
		axisValues[6][1][0] = y.get(y.size() - 1);
		axisValues[6][0][0] = z.get(z.size() - 1);

	}
		
		public static float getAxis(int graphIndex, int axisIndex, int seriesIndex){
			return axisValues[graphIndex][axisIndex][seriesIndex];
		}

		public static int getNnumOfSeries(int index) {
			/*for(int i = 0; i < 3; i++){
				if(axisValues[index][0][i] == null){
					return i + 1;
					}
				}
				return 0; */
			if(axisValues[index][0][2] != null){
				return 4;
			}
				return 1;
			
			}
			
}
