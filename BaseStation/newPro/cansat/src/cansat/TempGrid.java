package cansat;

import java.awt.image.BufferedImage;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;


public class TempGrid extends Canvas{
	private static GraphicsContext gc;
	private static int width, height;
	static float center;
	static BufferedImage image;
	private static float temp, xOffset, yOffset, size, newSize,newScale,
	newScaleX, newScaleY, fullHeight, fullWidth;
	
    public TempGrid(int width, int height, BufferedImage image){
	super(width, height);
	this.width = width;
	this.height = height;
	this.image = image;
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
			
		//	System.out.println("full " +(center+yOffset+size) );  
			fullWidth = center + xOffset + size;	
			fullHeight = center + yOffset + size;	
			
		//	System.out.println(height + " " + fullHeight);
			
			newScaleX = (height / fullWidth);
			newScaleY = (height / fullHeight);
			newScale = Math.min(newScaleX, newScaleY);
			newSize = Math.max(fullWidth, fullHeight);
		//	System.out.println(newScaleY);
		//	System.out.println(newScaleX); 
			gc.scale(newScale, newScale);
			height = (int) newSize;
			width = (int) newSize;
	//		   System.out.println("true");
			}
		}
		
		//System.out.println("width " + image.getWidth());
		
		for(int i = 0; i < TempValue.tempValues.size(); i++){
		
		temp = TempValue.tempValues.get(i).temp;
		xOffset = TempValue.tempValues.get(i).xOffset;
		yOffset	= TempValue.tempValues.get(i).yOffset;
		size = TempValue.tempValues.get(i).size;
		
	     gc.setFill(Utils.getColorByTemp((int)(temp)));
	     gc.fillRect(center + xOffset, center + yOffset, size, size);
		}
  }
     
	
}
