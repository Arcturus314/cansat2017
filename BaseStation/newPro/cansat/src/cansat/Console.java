package cansat;

import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;

public class Console extends TextArea{
	
	private StackPane pane = Gui.getPane();
	
	public Console(){
	      this.getStyleClass().add("console");
	      this.prefHeightProperty().bind(pane.heightProperty());
	      this.setEditable(false);
	      
	}

	public void update() {
		
		this.clear();
		
        for(int i = 0; i < Gui.StatusButtonNames.length; i++){
  		  this.appendText(String.valueOf(Gui.StatusButtonNames[i] + " " + DecodeData.Status[i] + Utils.newLine));
        }
		
	}
	
	
}
