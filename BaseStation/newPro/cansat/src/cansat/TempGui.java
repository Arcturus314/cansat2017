package cansat;

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
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;


public class TempGui extends Canvas{
	private static GraphicsContext gc;
	private static int width, height;
	
	 public TempGui(int width, int height){
			super(width, height);
			this.width = width;
			this.height = height;
			gc = this.getGraphicsContext2D();
			this.clear();
			
			for(int i = 0; i < 25; i++){
				 gc.setFill(Utils.temptoRGB(i));
				 gc.fillRect(0, (height / 25) * i + 10, 20, height / 25);
				}

			gc.setFill(Color.WHITE);
			gc.fillRect(20, 10, 2, 310);
			
			for(int i = 0; i < 6; i++){
				gc.fillRect(22, i * 59 + 10, 10, 2);
				gc.setFont(Font.font(java.awt.Font.SERIF, 12));
				gc.setFill(Color.WHITE);
				gc.fillText(i * 5 + "C", 34 , i * 59 + 15);
				}
			
			
		    }
	 
	 public void clear(){
		    gc.setFill(Color.TRANSPARENT);
		    gc.fillRect(0, 0, width, height);
		} 
}