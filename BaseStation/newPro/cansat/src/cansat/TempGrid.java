package cansat;

import java.text.DecimalFormat;
import java.util.Random;

import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.chart.XYChart;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.ArcType;
import javafx.scene.shape.Rectangle;

public class TempGrid extends Canvas{
	private static GraphicsContext gc;
	private static int width, height;
	static float center;
	private static float temp, xOffset, yOffset, size, newSize,newScale,
	newScaleX, newScaleY, fullHeight, fullWidth;
	
    public TempGrid(int width, int height){
	super(width, height);
	this.width = width;
	this.height = height;
	gc = this.getGraphicsContext2D();
	this.clear();
    }
    
    public static void clear(){
	    gc.setFill(Color.WHITE);
	    gc.fillRect(0, 0, width, height);
	}
    
	public static void update(){
		
		center = (width / 2 ); 
		
		//resize of element is out of bounds
		for(int i = 0; i < TempValue.tempValues.size(); i++){
			temp = TempValue.tempValues.get(i).temp;
			xOffset = TempValue.tempValues.get(i).xOffset;
			yOffset	= TempValue.tempValues.get(i).yOffset;
			size = TempValue.tempValues.get(i).size;
			
			if(center + xOffset + size  > width || center + yOffset + size > height){
			
			System.out.println("full " +(center+yOffset+size) );  
			fullWidth = center + xOffset + size;	
			fullHeight = center + yOffset + size;	
			
			System.out.println(height + " " + fullHeight);
			
			newScaleX = (height / fullWidth);
			newScaleY = (height / fullHeight);
			newScale = Math.min(newScaleX, newScaleY);
			newSize = Math.max(fullWidth, fullHeight);
			System.out.println(newScaleY);
			System.out.println(newScaleX); 
			gc.scale(newScale, newScale);
			height = (int) newSize;
			width = (int) newSize;
			   System.out.println("true");
			}
		}
		
		for(int i = 0; i < TempValue.tempValues.size(); i++){
		
		temp = TempValue.tempValues.get(i).temp;
		xOffset = TempValue.tempValues.get(i).xOffset;
		yOffset	= TempValue.tempValues.get(i).yOffset;
		size = TempValue.tempValues.get(i).size;
		
		Random rn = new Random();
		int answer = rn.nextInt(10) ;
		System.out.println(answer);
	     gc.setFill(Utils.temptoRGB(answer));
	     gc.fillRect(center + xOffset, center + yOffset, size, size);
		}
  }
     
	
}
