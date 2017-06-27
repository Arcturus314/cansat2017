package cansat;


import java.awt.image.BufferedImage;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import java.util.ArrayList;
import java.util.List;

import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.paint.Color;

public class Utils {
	 
	public static String newLine = "\n";
	
	public static void loopThroughGraphs(List<Graph> graphs) {
		for(int i =0; i < graphs.size(); i++){
			graphs.get(i).clear();
		}
		
	}
	
	public static Color getPixelColor(BufferedImage image, int x, int y){
		Color color;
		
	     	int clr = image.getRGB(x, y);
		    int red = (clr & 0x00ff0000) >> 16;
		    int green = (clr & 0x0000ff00) >> 8;
		    int blue = clr & 0x000000ff;
		
		    color = Color.rgb(red, green, blue);
		
		    return color;
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

	public static void crateTempRange(BufferedImage image) {
		// - 5 tp 45
		int imgI = 0;
		int startNum = -4;
		for(int i = 0; i < 50; i++){
			imgI = i;
			if(imgI > 0){
				imgI = imgI * 2;
			}
			TempColor tempColor = new TempColor(i + startNum, getPixelColor(image, imgI, 0));
		}
	}

	public static Color getColorByTemp(int temp) {
		for(int i = 0; i < TempColor.tempColors.size(); i++){
			if(temp == TempColor.tempColors.get(i).temp){
				return TempColor.tempColors.get(i).color;
			}
		}
		//add for > 45 || < -4
		return TempColor.tempColors.get(0).color;
	}

}