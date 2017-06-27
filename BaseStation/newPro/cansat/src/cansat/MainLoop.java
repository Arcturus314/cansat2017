package cansat;

import java.util.Timer;
import java.util.TimerTask;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.stage.Stage;


public class MainLoop extends Application{

	private Scene scene;
	private Window window;
	private DecodeData decodeData;
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
		                	
		                		Graph.graphs.get(i).update();
		                		
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 } 
		                		
		                	}
		                
		                //Update tempMap
		                	try{
		                		
		                		TempGrid.update();
		                		
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());
		                		 }
		                				 
		                	//}
		                
		                //Update map
		                	try{
		                		
                			   Map.update();
		                			
		                		 } catch (IndexOutOfBoundsException  e) {
		                			 System.err.println(e.getMessage());	 
		                	}
		                
		                //Update console
		                	try{
		                		  Console console = Gui.getConsole();
		                		  console.update();
		                		   
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
