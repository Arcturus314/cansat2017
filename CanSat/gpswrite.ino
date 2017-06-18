if (GPS.fix) {
	  
  String gpslatdeg = String(GPS.latitudeDegrees);
  String gpslongdeg = String(GPS.longitudeDegrees);
  String gpsspeed = String(GPS.speed);
  String gpsaltitude = String(GPS.altitude);
  String gpsvalidity = String(GPS.fix);
 
  int gpslatdeg[14];
  gpslatdeg[0] = 0x00
  gpslatdeg[1] = 0x00
  gpslatdeg[2] = gpslatdeg.charAt(0);
  gpslatdeg[3] = gpslatdeg.charAt(1);
  gpslatdeg[4] = gpslatdeg.charAt(2);
  gpslatdeg[5] = gpslatdeg.charAt(3);
  gpslatdeg[6] = gpslatdeg.charAt(4);
  gpslatdeg[7] = gpslatdeg.charAt(5);
  gpslatdeg[8] = gpslatdeg.charAt(6);
  gpslatdeg[9] = gpslatdeg.charAt(7);
  gpslatdeg[10] = gpslatdeg.charAt(8);
  gpslatdeg[11] = gpslatdeg.charAt(9); 
  gpslatdeg[12] = 0xFF
  gpslatdeg[13] = 0xFF
 
  int gpslondata[14];
  gpslondata[0] = 0x00
  gpslondata[1] = 0x00
  gpslondata[2] = gpslongdeg.charAt(0);
  gpslondata[3] = gpslongdeg.charAt(1);
  gpslondata[4] = gpslongdeg.charAt(2);
  gpslondata[5] = gpslongdeg.charAt(3);
  gpslondata[6] = gpslongdeg.charAt(4);
  gpslondata[7] = gpslongdeg.charAt(5);
  gpslondata[8] = gpslongdeg.charAt(6);
  gpslondata[9] = gpslongdeg.charAt(7);
  gpslondata[10] = gpslongdeg.charAt(8);
  gpslondata[11] = gpslongdeg.charAt(9);
  gpslondata[12] = 0xFF
  gpslondata[13] = 0xFF
 
  int gpsalt[14];
  gpsalt[0] = 0x00
  gpsalt[1] = 0x00
  gpsalt[2] = gpsaltitude.charAt(0);
  gpsalt[3] = gpsaltitude.charAt(1);
  gpsalt[4] = gpsaltitude.charAt(2);
  gpsalt[5] = gpsaltitude.charAt(3);
  gpsalt[6] = gpsaltitude.charAt(4);
  gpsalt[7] = gpsaltitude.charAt(5);
  gpsalt[8] = gpsaltitude.charAt(6);
  gpsalt[9] = gpsaltitude.charAt(7);
  gpsalt[10] = gpsaltitude.charAt(8);
  gpsalt[11] = gpsaltitude.charAt(9);
  gpsalt[12] = 0xFF
  gpsalt[13] = 0xFF
 
  int gpsvaliditydata[5]; 
  gpsvaliditydata[0] = 0x00;
  gpsvaliditydata[1] = 0x00;
  gpsvaliditydata[2] = gpsvalidity;
  gpsvaliditydata[3] = 0xFF;
  gpsvaliditydata[4] = 0xFF;
   
  int gpsspeeddata[5]; 
  gpsvaliditydata[0] = 0x00;
  gpsvaliditydata[1] = 0x00
  gpsvaliditydata[2] = gpsspeed
  gpsvaliditydata[3] = 0xFF
  gpsvaliditydata[4] = 0xFF
	
  int gpsdata[52]
  gpsdata[0] = 
  gpsdata[1] = 
  gpsdata[2] = 
  gpsdata[3] = 
  gpsdata[4] = 
  gpsdata[5] = 
  gpsdata[6] = 
  gpsdata[7] = 
  gpsdata[8] = 
  gpsdata[9] = 
  gpsdata[10] = 
  gpsdata[11] = 
  gpsdata[12] = 
  gpsdata[13] = 
  gpsdata[14] = 
  gpsdata[15] = 
  gpsdata[16] =
  gpsdata[17] = 
  gpsdata[18] = 
  gpsdata[19] = 
  gpsdata[20] = 
  gpsdata[21] = 
  gpsdata[22] = 
  gpsdata[23] = 
  gpsdata[24] = 
  gpsdata[25] = 
  gpsdata[26] = 
  gpsdata[27] = 
  gpsdata[28] = 
  gpsdata[29] = 
  gpsdata[30] = 
  gpsdata[31] = 
  gpsdata[32] = 
  gpsdata[33] = 
  gpsdata[34] = 
  gpsdata[35] = 
  gpsdata[36] = 
  gpsdata[37] = 
  gpsdata[38] = 
  gpsdata[39] = 
  gpsdata[40] = 
  gpsdata[41] = 
  gpsdata[42] = 
  gpsdata[43] =  
  gpsdata[44] =
  gpsdata[45] = 
  gpsdata[46] = 
  gpsdata[47] = 
  gpsdata[48] = 
  gpsdata[49] = 
  gpsdata[50] = 
  gpsdata[51] = 
}
