int gpsdata[53];
gpsdata[0] = 0x00
gpsdata[1] = 0x00	
gpsdata[3] = 0xFF
gpsdata[4] = 0xFF
gpsdata[5] = 0x00
gpsdata[6] = 0x00
gpsdata[12] = 0xFF
gpsdata[13] = 0xFF
gpsdata[14] = 0x00
gpsdata[15] = 0x00
gpsdata[26] = 0xFF
gpsdata[27] = 0xFF
gpsdata[28] = 0x00
gpsdata[29] = 0x00
gpsdata[40] = 0xFF
gpsdata[41] = 0xFF
gpsdata[42] = 0x00
gpsdata[43] = 0x00
gpsdata[54] = 0xFF
gpsdata[55] = 0xFF
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
	
  int gpsdata[54];
  gpsdata[2] = gpsvaliditydata[2];
  gpsdata[7] = gpsspeeddata[2];
  gpsdata[8] = gpsspeeddata[3];
  gpsdata[9] = gpsspeeddata[4];
  gpsdata[10] = gpsspeeddata[5]; 
  gpsdata[11] = gpsspeeddata[6];
  gpsdata[16] = gpslatdegdata[2];
  gpsdata[17] = gpslatdegdata[3];
  gpsdata[18] = gpslatdegdata[4];
  gpsdata[19] = gpslatdegdata[5];
  gpsdata[20] = gpslatdegdata[6];
  gpsdata[21] = gpslatdegdata[7];
  gpsdata[22] = gpslatdegdata[8];
  gpsdata[23] = gpslatdegdata[9];
  gpsdata[24] = gpslatdegdata[10];
  gpsdata[25] = gpslatdegdata[11];
  gpsdata[30] = gpslondata[2];
  gpsdata[31] = gpslondata[3];
  gpsdata[32] = gpslondata[4];
  gpsdata[33] = gpslondata[5];
  gpsdata[34] = gpslondata[6];	
  gpsdata[35] = gpslondata[7];
  gpsdata[36] = gpslondata[8];
  gpsdata[37] = gpslondata[9];
  gpsdata[38] = gpslondata[10];	
  gpsdata[39] = gpslondata[11];	
  gpsdata[44] =  gpsalt[2];
  gpsdata[45] =  gpsalt[3];
  gpsdata[46] =  gpsalt[4];
  gpsdata[47] =  gpsalt[5];
  gpsdata[48] =  gpsalt[6]; 
  gpsdata[49] =  gpsalt[7]; 
  gpsdata[50] =  gpsalt[8];
  gpsdata[51] =  gpsalt[9];
  gpsdata[52] =  gpsalt[10];
  gpsdata[53] =  gpsalt[11];
}
