package cansat;

import java.util.ArrayList;
import java.util.List;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;



public class Graph extends LineChart{

	public static List<Graph> graphs = new ArrayList<Graph>();
	private String[] titles = new String[] {"Temp vs Time ","press","hum","accel magnitude", "xy", "xz", "yz"};
	
	private String[][] axis = new String[][]{
	    {"time(S)","temperature (C)"},{"time (S)","pressure (Pa)"}, {"time (S)","humidity (RH)"},{"time (S)","acceleration magnitude"}, {"x","y"},{"x","z"}, {"y","z"}
	};
	
	private String[] seriesNames = new String[]{"Averag", "Imu", "D6t", "Env"};
	
	
	XYChart.Series series;
	
	public int numOfSeries, index;
	public float newXAxis, newYAxis;
	
	public Graph(NumberAxis xAxis, NumberAxis yAxis, int numOfSeries) {
		super(xAxis, yAxis);	
		this.numOfSeries = numOfSeries;
		this.index = graphs.size();
		
		this.setTitle(titles[index]);
		xAxis.setLabel(axis[index][0]);
		yAxis.setLabel(axis[index][1]);
		
		for(int i = 0; i < this.numOfSeries; i++){
			series = new XYChart.Series();
			
			 if(this.numOfSeries > 1){
				 series.setName(seriesNames[i]);
			 }else{
				 series.setName("series");
			 }
			 
			 this.getData().add(series);
		}
		
	    
	   if(this.numOfSeries > 1){
		   this.setLegendVisible(true);
	   }else{
		   this.setLegendVisible(false);
	   }
	    
	    graphs.add(this);
	    
	    
	}
		
	public void update(){ 
		  for(int i = 0; i < this.numOfSeries; i++){
		  newXAxis = DecodeData.getAxis(this.index, 0, i);
		  newYAxis = DecodeData.getAxis(this.index, 1, i);
		  XYChart.Data newData = new XYChart.Data(newXAxis ,newYAxis);
		  series = (Series) this.getData().get(i);
		  series.getData().add(newData);
		  	}
		  } 
	
	public void clear(){
		this.getData().clear();
		}
	
	
}
