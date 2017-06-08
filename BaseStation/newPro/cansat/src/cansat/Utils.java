package cansat;


import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javafx.scene.Node;
import javafx.scene.Parent;

public class Utils {
	 
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