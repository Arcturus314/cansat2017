package cansat;

import javafx.scene.Scene;
import javafx.stage.Stage;

public class Window {
	private int width, height;
	private String title;
	private Scene scene;
	
	public Window(Stage window) {
	
		//Window properties 
		title = "canSat";
		width = 900;
		height = 900;
		window.setMinWidth(900);
		window.setMinHeight(820);
		window.setFullScreen(false);
		
		//G.u.i. constructor
		Gui gui = new Gui(width, height);
		
		//Loads G.u.i.
		scene = Gui.getGui();
		try{
			scene.getStylesheets().add("/style.css");
			 } catch (IndexOutOfBoundsException  e) {
				 System.err.println(e.getMessage());
			 }
		
	    window.setScene(scene);
	    
	    //Set window title to window size + title
	    window.titleProperty().bind(
			window.widthProperty().asString().concat(" : ").
				concat(window.heightProperty().asString()).concat(" "+title));
	    window.show(); 
	}
    
}
