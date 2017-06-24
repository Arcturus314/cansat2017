package cansat;

import java.util.ArrayList;
import java.util.List;

public class TempValue {

	public static List<TempValue> tempValues  = new ArrayList<TempValue>();
	public float temp, xOffset, yOffset, size;
	
	public TempValue(float Temp, float XOffset, float YOffset, float Size){
		this.temp = Temp;
		this.xOffset = XOffset;
		this.yOffset = YOffset;
		this.size = Size;
		
		tempValues.add(this); 
	}
	
	
	

}
