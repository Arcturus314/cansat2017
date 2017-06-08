package cansat;


import java.net.URL;
import java.util.Random;
import javafx.geometry.Insets;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.concurrent.Worker.State;

import javafx.scene.Scene;
import javafx.scene.layout.VBox;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;


public class Gui {
	private int width;
	private int height;
	private VBox vBox0;
	private VBox vBox1;
	private VBox vBox2;
	private HBox row;
	private static Scene scene;
	private StackPane pane;
	private GridPane grid;
	private WebView Map; 
	private static TextArea console;
	private static Button Btn;
	
	public Gui(int width, int height){
		this.width = width;
		this.height = height;
		
		pane = new StackPane();
	    grid = new GridPane();
	    pane.getChildren().add(grid);
		    
		    //Set up 3 Columns
		    for(int i = 0; i < 3; i++){
		    
			    VBox vBox = new VBox();
			    vBox.setId("hBox"+i);
			    vBox.getStyleClass().add("column");
			    vBox.prefWidthProperty().bind(pane.widthProperty());
			    vBox.prefHeightProperty().bind(pane.heightProperty());
			    grid.addColumn(i, vBox);
		    }
		    
		    //Get columns by id (css id not fx:id)
		    vBox0 = (VBox) pane.lookup("#hBox0");
		    vBox1 = (VBox) pane.lookup("#hBox1");
		    vBox2 = (VBox) pane.lookup("#hBox2");

		    //Temperature grid 
		    int rowNum = 12;
			int colNum = 12;
			
			 Random rand = new Random();
			  Color[] colors = {Color.BLACK, Color.BLUE, Color.GREEN, Color.RED};
			    
	          GridPane gridPane = new GridPane();
	          gridPane.prefWidthProperty().bind(pane.heightProperty().divide(48));
	          gridPane.prefHeightProperty().bind(pane.heightProperty().divide(48));
	         // gridPane.layoutXProperty().bind(pane.widthProperty().divide(2));
	          //gridPane.maxHeightProperty().bind(pane.heightProperty().divide(4));
	          gridPane.setPadding(new Insets(0, 15, 0, 40));
	          
	          int id = 0;
	          for (int row = 0; row < rowNum; row++) {
	        	    for (int col = 0; col < colNum; col++) {
	        	        int n = rand.nextInt(4);
	        	        Rectangle rec = new Rectangle();
	        	        rec.widthProperty().bind(pane.heightProperty().divide(48));
	        	        rec.heightProperty().bind(pane.heightProperty().divide(48));
	        	        rec.heightProperty().addListener((obs, oldVal, newVal) -> {
	        	        	
	        	        	//if(rec.getHeight() > (pane.getHeight() / 4 )){
	    	        	    //    rec.heightProperty().bind(pane.heightProperty().divide(4));
	    	        	    //    }
	        	       });
	        	        
	        	        rec.setFill(colors[n]);
	        	        rec.setId("rec"+id);
	        	        GridPane.setRowIndex(rec, row);
	        	        GridPane.setColumnIndex(rec, col);
	        	        gridPane.getChildren().add(rec);
	        	        id++;
	        	    }
	        	}
	          
	          
	          gridPane.getStyleClass().add("grid");
	          vBox2.getChildren().add(gridPane);

		    //Set up Graphs
	          for(int i = 0; i < 7; i++){
		  
				    XYChart.Series series1;
				    final NumberAxis xAxis1 = new NumberAxis();
			        final NumberAxis yAxis1 = new NumberAxis();
			        final LineChart<Number,Number> lineChart =   new LineChart<>(xAxis1,yAxis1);
			        series1 = new XYChart.Series();
			        series1.setName("series1");
			        lineChart.getData().add(series1);
			        lineChart.setId("Chart"+i);
			        lineChart.setLegendVisible(false);
			        
			        if(i < 4){ vBox0.getChildren().add(lineChart); }
			        
			        if(i < 5 && i > 3 ){ vBox2.getChildren().add(lineChart); }
			       
			        if(i < 7 && i > 4 ){ vBox2.getChildren().add(lineChart); }
			 
	          }
	       
	        final String CSS = Utils.readFile("assets/mapStyles.css");               
	        
	        //
	        
		    //Map
		    Map = new WebView();
	        Map.setContextMenuEnabled(false);
	        Map.prefHeightProperty().bind(pane.heightProperty());
	        
	        //Load google Maps (Lite mode)
	        WebEngine webEngine = Map.getEngine();
	        webEngine.load("https://www.google.com/lochp");
	    
	        //Remove google maps G.u.i.
	        webEngine.getLoadWorker().stateProperty().addListener((obs, oldState, newState) -> {
	            if (newState == State.SUCCEEDED) {
	                Document doc = webEngine.getDocument();
	                Element styleNode = doc.createElement("style");
	                Text styleContent = doc.createTextNode(CSS);
	                styleNode.appendChild(styleContent);
	                doc.getDocumentElement().getElementsByTagName("head").item(0).appendChild(styleNode);
	           }
	        }); 
	        
	         ImageView imageView = new ImageView(); 
	         Image logo = new Image("logoFilled.tiff");
	         imageView.setImage(logo);
	         imageView.setFitHeight(100);
	         imageView.setFitWidth(100);
	     //    iv2.fitWidthProperty().bind(pane.widthProperty());
	         imageView.setPreserveRatio(true);
	       //  imageView.setSmooth(true);
	       //  imageView.setCache(true);
	         
	       
	        //Console
	        console = new TextArea();
	        console.getStyleClass().add("console");
	        console.prefHeightProperty().bind(pane.heightProperty());
	        console.setEditable(false);
	        
	        //Columns 2
		    vBox1.getChildren().addAll(imageView, Map, console); 
		  
		    //Add VBoxs 
		    for(int i = 0; i < 2; i++){
		    	row = new HBox();
		    	row.setId("row"+i);
		    	row.prefWidthProperty().bind(pane.widthProperty());
		    	vBox1.getChildren().addAll(row);
		    	
		    }
		    
		    HBox tempRow = null;
		    
		    //Add Buttons 
		    for(int i = 0; i < 10; i++){
		        Btn = new Button("Click Me");
		        Btn.setId("btn"+i);
		        Btn.setText("btn"+i);
		        Btn.getStyleClass().add("Btn"); 
		        Btn.prefWidthProperty().bind(pane.widthProperty());
		        
		        if(i < 5){ tempRow = (HBox) pane.lookup("#row"+0);}
			       
		        if(i > 4){ tempRow = (HBox) pane.lookup("#row"+1);}
		       
		        tempRow.getChildren().add(Btn);
		    }
		    
		    //Padding
		    vBox1.setPadding(new Insets(0, 0, 0, 0));
		    vBox1.setPadding(new Insets(15, 0, 40, 0));
		    vBox2.setPadding(new Insets(15, 0, 0, 0));
		    
		    scene = new Scene(pane , width, height);
		    
		    
	}
	
	//Getters and Setters	
	public static Scene getGui(){
		return scene;
	}
	
	public static TextArea getTextField(){
		return console;
	}
}
