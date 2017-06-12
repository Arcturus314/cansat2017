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
	private static int tick;
	
	@Override
	public void start(Stage stage) {
		tick = 0;	
		
		//Create window and g.u.i.
		window = new Window(stage);		
		
		scene = Gui.getGui();
		
		  //Main Loop 
	      Timer timer = new Timer();
	      
	      timer.scheduleAtFixedRate(new TimerTask() {
	       
	            @Override
	            public void run() {
	                Platform.runLater(() -> {
	                
	                	//Get data
	                	try{
	                		
	                		decodeData = new DecodeData("assets/test.txt");
	                		
	                		 } catch (IndexOutOfBoundsException  e) {
	                			 System.err.println(e.getMessage());
	                	   }
    	
	                	//Update lineCharts
		                for(int i = 0; i < 7; i++){ 
		                	try{
		                	
		                		Graph.graphs.get(i).update(i);
		                		
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 } 
		                		
		                		
		                	
		                	}
		                
		           
		                	try{
		                		if(tick == 0){
		                		TempGrid.update();
		                		}
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 }
		                				 
		                	//}
		                
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
	
	
	//Getters and Setters	
		public static int getTick(){
			return tick;
		}
}
