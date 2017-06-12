package cansat;


import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.paint.Color;

public class Utils {
	 
	public static void loopThroughGraphs(List<Graph> graphs) {
		for(int i =0; i < graphs.size(); i++){
			graphs.get(i).clear();
		}
		
	}
	

    public static Color temptoRGB(double Temperature){
    	 Temperature = Temperature * 10;

    	// System.out.println(Temperature);
    	 
    	 			double Red;
    	 			double Green;
    	 			double Blue;
    			    //Calculate Red:

    			    if(Temperature <= 66){

    			        Red = 255;

    				}else{

    			        Red = Temperature - 60;

    			        Red = 329.698727446 * (Red  -0.1332047592);

    			        if(Red < 0) Red = 0;

    			        if(Red > 255) Red = 255;

    				}

    			    

    			    //Calculate Green:



    			    if(Temperature <= 66){

    			        Green = Temperature;

    			        Green = 99.4708025861 * Math.log(Green) - 161.1195681661;

    			        if(Green < 0) Green = 0;

    			        if(Green > 255) Green = 255;

    			   }else{

    			        Green = Temperature - 60;

    			        Green = 288.1221695283 * Math.pow(Green, -0.0755148492);

    			        if(Green < 0) Green = 0;

    			        if(Green > 255) Green = 255;

    				}

    			    

    			    //Calculate Blue:



    			    if(Temperature >= 66){

    			        Blue = 255;

    			    }else{



    			     if(Temperature <= 19){

    			     Blue = 0;

    			}else{

    			            Blue = Temperature - 10;

    			            Blue = 138.5177312231 * Math.log(Blue) - 305.0447927307;

    			            if(Blue < 0) Blue = 0;

    			            if(Blue > 255) Blue = 255;

    			    }
    			        	    
    			 }
    			  
    			   // System.out.println(Red + " " + Green + " " + Blue + " " + Temperature);
    		
    			    return Color.rgb((int)Red, (int)Green, (int)Blue);
    }
    
	
	//Get all child nodes of Parent
    public static ArrayList<Node> getAllNodes(Parent root) {
        ArrayList<Node> nodes = new ArrayList<Node>();
        addAllDescendents(root, nodes);
        return nodes;
    }
    
    private static void addAllDescendents(Parent parent, ArrayList<Node> nodes) {
        for (Node node : parent.getChildrenUnmodifiable()) {
            nodes.add(node);
            if (node instanceof Parent)
                addAllDescendents((Parent)node, nodes);
        }
    }
    
    //Load File(String)
    public static String readFile(String file){
    try(BufferedReader br = new BufferedReader(new FileReader(file))){
        StringBuilder sb = new StringBuilder();
        String line = null;
		try {
			line = br.readLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

        while (line != null) {
            sb.append(line);
            sb.append(System.lineSeparator());
            line = br.readLine();
        }
        String everything = sb.toString();
        return everything;
    	}catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    return null;
    }

   
    public static String[] removeArrayFirstElement(String[] array){
    String[] temp = new String[array.length - 1];
	   for (int i = 0; i < array.length - 1; i++) {
	     temp[i] = array[i+1];
	   }
	   return temp;
    }


}