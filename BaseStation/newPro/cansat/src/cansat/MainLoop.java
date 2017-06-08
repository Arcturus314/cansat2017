package cansat;

import java.io.Console;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.scene.layout.Region;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.chart.XYChart.Series;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.concurrent.Worker.State;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;

public class MainLoop extends Application{

	private boolean running = false;
	private Thread thread;
	private Scene scene;
	private LineChart lineChart;
	private Rectangle rectangle;
	private Window window;
	private DecodeData decodeData;
	private String newFile;
	private String[] newDocSplit;
	private int newNumberOfDataSets;
	private int oldNumberOfDataSets;
	public static List<DataSet> dataSetArray;
	
	
	@Override
	public void start(Stage stage) {
		
		//Create window and g.u.i.
		window = new Window(stage);
		decodeData = new DecodeData("assets/test.txt");
		//dataSetArray = new ArrayList<DataSet>();
		scene = Gui.getGui();
		
		//System.out.println(dataSetArray.get(0).header);
		
		  //Main Loop 
	      Timer timer = new Timer();
	      
	      timer.scheduleAtFixedRate(new TimerTask() {
	       int tick = 0;
	            @Override
	            public void run() {
	                Platform.runLater(() -> {
	                
	                	//Get data
	                	try{
	                		
	                		
	                		//if(newNumberOfDataSets > newNumberOfDataSets){
	                			
	                		//}

	                		 } catch (IndexOutOfBoundsException  e) {
	                			 System.err.println(e.getMessage());
	                	   }
    	
	                	//Update lineCharts
		                for(int i = 0; i < 7; i++){ 
		                	try{
		                		  lineChart = (LineChart) scene.lookup("#Chart" + i);
		                		  XYChart.Series series1 = (Series) lineChart.getData().get(0);
			                	  XYChart.Data newData = new XYChart.Data(tick + 1,tick + 1);
			                	  series1.getData().add(newData);
			                	  	
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 }
		                				 
		                	}
		                
		                //Update temperature grid 
		                Random rand = new Random();
		    		    Color[] colors = {Color.BLACK, Color.BLUE, Color.GREEN, Color.RED};
		                
		                for(int i = 0; i < 144; i++){ 
		                	try{
		                		    rectangle = (Rectangle) scene.lookup("#rec" + i);
			                		int n = rand.nextInt(4);
			                		rectangle.setFill(colors[n]);
			                		
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 }
		                				 
		                	}
		                
		                //Update map
		                for(int i = 0; i < 7; i++){ 
		                	try{
		                		  
		                		   
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 }
		                				 
		                	}
		                
		                //Update console
		          
		                	try{
		                		   TextArea  console = Gui.getTextField();
		                		   String newLine = "\n";
		                		   console.appendText(String.valueOf(tick+ newLine));
		                		   
		                		} catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		}

		       
		                tick++;
	                });
		        }
		    }, 100, 1000); 
		
	
	}


}
