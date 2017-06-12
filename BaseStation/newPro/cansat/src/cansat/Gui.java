package cansat;


import java.net.URL;
import java.util.List;
import java.util.Random;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.Tooltip;
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
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
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
	private HBox tempRow;
	private VBox tempCol0;
	private VBox tempCol1;
	private static Scene scene;
	private static StackPane pane;
	private GridPane grid;
	private WebView Map; 
	private static TextArea console;
	private static Button Btn;
	private static StatusButton statusBtn;
	private static WebEngine webEngine;
	
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
		    TempGrid tempGrid = new TempGrid(300, 300);
		    TempGui colorGui = new TempGui(60, 310);
		    
		    tempCol0 = new VBox();
		    tempCol1 = new VBox();
		    tempCol0.setPadding(new Insets(10, 0, 40, 0));
		    tempCol0.prefWidthProperty().bind(pane.widthProperty());
		    tempCol0.prefHeightProperty().bind(pane.heightProperty().divide(48));
		    
		    tempCol1.setPadding(new Insets(0, 0, 40, 0));
		    tempCol1.prefWidthProperty().bind(pane.widthProperty());
		    tempCol1.prefHeightProperty().bind(pane.heightProperty().divide(48));
		    
	        tempRow = new HBox();
	        tempRow.prefWidthProperty().bind(pane.widthProperty());
	        tempRow.prefHeightProperty().bind(pane.heightProperty().divide(48));
	       
	        tempCol0.getChildren().add(tempGrid);
	        tempCol1.getChildren().add(colorGui);
	        
		    tempRow.getChildren().addAll(tempCol0, tempCol1);
		    
	    	vBox2.getChildren().addAll(tempRow);
	    	
		    //Set up Graphs
	          for(int i = 0; i < 7; i++){
	        	  
        	    final NumberAxis xAxis = new NumberAxis();
		        final NumberAxis yAxis = new NumberAxis();
        	  
        	    Graph lineChart =  new Graph(xAxis, yAxis);
		        
		        if(i < 4){ vBox0.getChildren().add(lineChart); }
		        
		        if(i < 5 && i > 3 ){ vBox2.getChildren().add(lineChart); }
		       
		        if(i < 7 && i > 4 ){ vBox2.getChildren().add(lineChart); }
	        	  	  
	          }
	       
	        final String CSS = Utils.readFile("assets/mapStyles.css");              
	        
		    //Map
		    Map = new WebView();
	        Map.setContextMenuEnabled(false);
	        Map.prefHeightProperty().bind(pane.heightProperty());
	        
	        
	        //Load google Maps (Lite mode)
	        webEngine = Map.getEngine();
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
	        
	        
	        //image
	         StackPane stackPane = new StackPane();
	         stackPane.prefWidthProperty().bind(pane.widthProperty());
	         stackPane.prefHeightProperty().bind(pane.heightProperty());
		     
	         ImageView imageView = new ImageView();
	         Image logo = new Image("logoFilled2.png");
	         imageView.fitWidthProperty().bind(pane.heightProperty().divide(5));
	         imageView.fitHeightProperty().bind(pane.heightProperty().divide(5));
	         imageView.setImage(logo);
	         imageView.setPreserveRatio(true);
	         stackPane.setAlignment(imageView,Pos.CENTER_LEFT);
      
	        //Console
	        console = new TextArea();
	        console.getStyleClass().add("console");
	        console.prefHeightProperty().bind(pane.heightProperty());
	        console.setEditable(false);
	        
	        //Column 2
		    vBox1.getChildren().addAll(imageView, Map, console); 
		  
		    //Add VBoxs 
		    for(int i = 0; i < 3; i++){
		    	row = new HBox();
		    	row.setId("row"+i);
		    	row.prefWidthProperty().bind(pane.widthProperty());
		    	vBox1.getChildren().addAll(row);
		    }
		    
		    HBox tempRow = null;
		    
		    //Status btn
		    for(int i = 0; i < 5; i++){
		    	statusBtn = new StatusButton(false);
		    	statusBtn.setText("status"+i);
		    	statusBtn.getStyleClass().add("Btn"); 
		    	
		    	
		    	
		    	statusBtn.prefWidthProperty().bind(pane.widthProperty());
		        
		        tempRow = (HBox) pane.lookup("#row"+0);
		        
		        tempRow.getChildren().add(statusBtn);
		    }
		    
		    
		    
		    //Add Buttons 
		    for(int i = 0; i < 10; i++){
		        Btn = new Button("Click Me");
		        Btn.setId("btn"+i);
		        Btn.setText("btn"+i);
		        Btn.getStyleClass().add("Btn"); 
		        Btn.prefWidthProperty().bind(pane.widthProperty());
		        
		        if(i < 5){ tempRow = (HBox) pane.lookup("#row"+1);}
			       
		        if(i > 4){ tempRow = (HBox) pane.lookup("#row"+2);}
		       
		        tempRow.getChildren().add(Btn);
		    }
		    
		    Button btn0 = (Button) pane.lookup("#btn0");
		    btn0.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    
		  //  Tooltip customTooltip = new Tooltip();
		  //  customTooltip.setText("tooltipText");
		  //  customTooltip.setAutoHide(false);
		  //  btn0.setTooltip(customTooltip);
		  
		    Button btn1 = (Button) pane.lookup("#btn1");
		    btn1.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn2 = (Button) pane.lookup("#btn2");
		    btn2.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn3 = (Button) pane.lookup("#btn3");
		    btn3.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn4 = (Button) pane.lookup("#btn4");
		    btn4.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	            /*	clear all graphs
	            	Utils.loopThroughGraphs(Graph.graphs);
	               */
	            /*	clear temp grid 
	            	TempGrid.clear();
	               */
	            	
	            	
	            }
	        });
		    
		    Button btn5 = (Button) pane.lookup("#btn5");
		    btn5.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn6 = (Button) pane.lookup("#btn6");
		    btn6.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn7 = (Button) pane.lookup("#btn7");
		    btn7.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn8 = (Button) pane.lookup("#btn8");
		    btn8.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    
		    Button btn9 = (Button) pane.lookup("#btn9");
		    btn9.setOnAction(new EventHandler<ActionEvent>() {
	            public void handle(ActionEvent event) {
	               
	            }
	        });
		    //Padding
		    vBox1.setPadding(new Insets(0, 0, 0, 0));
		    vBox1.setPadding(new Insets(15, 0, 40, 0));
		    vBox2.setPadding(new Insets(5, 0, 0, 0));
		    
		    scene = new Scene(pane , width, height);
		    
		    
	}
	


	//Getters and Setters	
	public static Scene getGui(){
		return scene;
	}
	
	public static WebEngine getWebEngine(){
		return webEngine;
	}
	
	public static StackPane getPane(){
		return pane;
	}
	
	public static TextArea getTextField(){
		return console;
	}
}
