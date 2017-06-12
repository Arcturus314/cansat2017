package cansat;

import java.util.ArrayList;
import java.util.List;

import javafx.collections.ObservableList;
import javafx.scene.chart.Axis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;


public class Graph extends LineChart{

	public static List<Graph> graphs = new ArrayList<Graph>();
	private String[] titles = new String[] {"Temp vs Time ","press","hum","accel magnitude", "xy", "xz", "yz"};
	
	private String[][] axis = new String[][]{
	    {"time","temperature"},{"time","pressure"}, {"time","humidity"},{"time","acceleration magnitude"}, {"x","y"},{"x","z"}, {"y","z"}
	};
	
	ArrayList[][] series;
	
	XYChart.Series series1;

	float newXAxis, newYAxis;
	
	public Graph(NumberAxis xAxis, NumberAxis yAxis) {
		super(xAxis, yAxis);	
		int index = graphs.size();
		
		this.setTitle(titles[index]);
		
		xAxis.setLabel(axis[index][0]);
		yAxis.setLabel(axis[index][1]);
		
	    series1 = new XYChart.Series();
	    series1.setName("series1");
	    this.getData().add(series1);
	   // lineChart.setId("Chart"+i);
	    this.setLegendVisible(false);
 
	    
	    graphs.add(this);
	    
	    
	}
	
	public void update(int i){
	  newXAxis = DecodeData.getAxis(i, 0);
	  newYAxis = DecodeData.getAxis(i, 1);
   	  XYChart.Data newData = new XYChart.Data(newXAxis ,newYAxis);
   	  series1.getData().add(newData);
	}
	
	public void clear(){
		series1.getData().clear();
		}
	
	
}
