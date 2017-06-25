package cansat;

import java.awt.image.BufferedImage;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.PixelReader;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;


public class TempGui extends Canvas{
	private static GraphicsContext gc;
	private static int width, height;
	private PixelReader pixelReader;
	
	 public TempGui(int width, int height, BufferedImage image){
			super(width, height);
			this.width = width;
			this.height = height;
			gc = this.getGraphicsContext2D();
			this.clear();
			
			
			//int maxSize = 50;
			int maxSize = TempColor.tempColors.size();
			for(int i = 0; i < maxSize; i++){
				   gc.setFill(TempColor.tempColors.get(maxSize - i - 1).color);
				 gc.fillRect(0, (height / maxSize) * i + 10, 20, height / 25);
				}

			gc.setFill(Color.WHITE);
			gc.fillRect(20, 10, 2, 310);
			
			int[] nums = new int[]{45, 35, 25, 15, 5 ,-4};
			
			for(int i = 0; i < 6; i++){
				gc.fillRect(22, i * 59 + 10, 10, 2);
				gc.setFont(Font.font(java.awt.Font.SERIF, 12));
				gc.setFill(Color.WHITE);
				gc.fillText(nums[i] + "C", 34 , i * 59 + 15);
				}
			
			
		    }
	 
	 public void clear(){
		    gc.setFill(Color.TRANSPARENT);
		    gc.fillRect(0, 0, width, height);
		} 
}