package cansat;

import java.util.ArrayList;
import java.util.List;

import javafx.scene.control.Button;

public class StatusButton extends Button{

	public static List<StatusButton> statusButtons  = new ArrayList<StatusButton>();
	public Boolean status;
	
	public StatusButton(Boolean Status) {
		this.status = Status;
		
		if(status == true){
			this.setStyle("-fx-background-color: green");
		}else{
			this.setStyle("-fx-background-color: red");
		}
		
		statusButtons.add(this); 
	}
	
	public void toggle(Boolean Status){
		this.status = Status;
		
		if(status == true){
			this.setStyle("-fx-background-color: green");
		}else{
			this.setStyle("-fx-background-color: red");
		}
		
	}	
	
	
	public Boolean getStatus(){
		return this.status;
	}
		
	
	

	

}
