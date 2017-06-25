package cansat;
import java.net.URL;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.concurrent.Worker.State;
import javafx.scene.layout.StackPane;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;

public class Map extends StackPane{
	WebView map;
	static WebEngine webEngine;
	static boolean loaded;
	
	public Map(){
		loaded = false;
		this.prefWidthProperty().bind(Gui.getPane().widthProperty());
		this.prefHeightProperty().bind(Gui.getPane().heightProperty());
		
		
    	map = new WebView();
    	map.setContextMenuEnabled(false);
    	map.prefHeightProperty().bind(Gui.getPane().heightProperty());
	          
        webEngine = map.getEngine();

        URL mapUrl = getClass().getResource("map.html");
        webEngine.load(mapUrl.toExternalForm());
        //webEngine.load("https://www.google.com/lochp");
        double lat = 55.9573845;
        double lon = -3.1860419;

         System.out.printf("%.2f %.2f%n", lat, lon);

         final String CSS = Utils.readFile("assets/mapStyles.css");              
         
         webEngine.getLoadWorker().stateProperty().addListener(
                 new ChangeListener<State>() {
                     public void changed(ObservableValue ov, State oldState, State newState) {
                        if (newState == State.SUCCEEDED) {
                        	Document doc = webEngine.getDocument();
         	                Element styleNode = doc.createElement("style");
         	                Text styleContent = doc.createTextNode(CSS);
         	                styleNode.appendChild(styleContent);
         	                doc.getDocumentElement().getElementsByTagName("head").item(0).appendChild(styleNode);
         	                loaded = true;
                         }
                     }
                 });
         
         
         this.getChildren().add(map);
         
    }
 
    public static void clear(){
	   
	}
    
	public static void update(){	
           if(loaded == true){   
			 double lat = DecodeData.lat.get(DecodeData.lat.size() - 1);
		     double lon = DecodeData.lon.get(DecodeData.lon.size() - 1);
			 webEngine.executeScript("document.goToLocation( "+lat+","+lon+");");
           }     
             
      }
                     
}