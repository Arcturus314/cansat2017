package cansat;

import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;

public class Console extends TextArea{
	
	private StackPane pane = Gui.getPane();
	
	public Console(){
	      this.getStyleClass().add("console");
	      this.prefHeightProperty().bind(pane.heightProperty());
	      this.setEditable(false);
	      
	}

	public void update() {
		
		this.clear();
		
		//Load Data titles and values
        for(int i = 0; i < Gui.StatusButtonNames.length; i++){
  		  this.appendText(String.valueOf(Gui.StatusButtonNames[i] + " " + DecodeData.Status[i] + Utils.newLine));
        }
		
	}
	
	
}
