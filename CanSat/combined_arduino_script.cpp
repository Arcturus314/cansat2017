#include <Sim800l.h>
#include <SoftwareSerial.h> //is necesary for the library!! 
#include <Wire.>
Sim800l Sim800l;  //to declare the library
char* text;
char* number;
bool error; //to catch the response of sendSms

int xbee_err;
int lsm303_err;
int l3gd20_err;
int bme280_err;
int d6t_err;

// Test code for Adafruit GPS modules using MTK3329/MTK3339 driver
//
// This code shows how to listen to the GPS module in an interrupt
// which allows the program to have more 'freedom' - just parse
// when a new NMEA sentence is available! Then access data when
// desired.
//
// Tested and works great with the Adafruit Ultimate GPS module
// using MTK33x9 chipset
//    ------> http://www.adafruit.com/products/746
// Pick one up today at the Adafruit electronics shop 
// and help support open source hardware & software! -ada

#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
#include <Wire.h>
// If you're using a GPS module:
// Connect the GPS Power pin to 5V
// Connect the GPS Ground pin to ground
// If using software serial (sketch example default):
//   Connect the GPS TX (transmit) pin to Digital 3
//   Connect the GPS RX (receive) pin to Digital 2
// If using hardware serial (e.g. Arduino Mega):
//   Connect the GPS TX (transmit) pin to Arduino RX1, RX2 or RX3
//   Connect the GPS RX (receive) pin to matching TX1, TX2 or TX3

// If you're using the Adafruit GPS shield, change 
// SoftwareSerial mySerial(3, 2); -> SoftwareSerial mySerial(8, 7);
// and make sure the switch is set to SoftSerial

// If using software serial, keep this line enabled
// (you can change the pin numbers to match your wiring):
SoftwareSerial mySerial(4, 3);

// If using hardware serial (e.g. Arduino Mega), comment out the
// above SoftwareSerial line, and enable this line instead
// (you can change the Serial number to match your wiring):

//HardwareSerial mySerial = Serial1;


Adafruit_GPS GPS(&mySerial);


// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences. 
#define GPSECHO  false

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy

void setup()  
 
Wire.begin();
Wire.onRecieve(recieveEvent);
Wire.onRequest(requestEvent);
 
{
 
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  Serial.println("Adafruit GPS library basic test!");

  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  // the nice thing about this code is you can have a timer0 interrupt go off
  // every 1 millisecond, and read data from the GPS for you. that makes the
  // loop code a heck of a lot easier!
  useInterrupt(true);

  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
}


// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;  
    // writing direct to UDR0 is much much faster than Serial.print 
    // but only one character can be written at a time. 
#endif
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

uint32_t timer = millis();
void loop()                     // run over and over again
{
  // in case you are not using the interrupt above, you'll
  // need to 'hand query' the GPS, not suggested :(
  if (! usingInterrupt) {
    // read data from the GPS in the 'main loop'
    char c = GPS.read();
    // if you want to debug, this is a good time to do it!
    if (GPSECHO)
      if (c) Serial.print(c);
  }
  
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences! 
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false
  
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }
  
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
  gpsvaliditydata[0] = 0x00
  gpsvaliditydata[1] = 0x00
  gpsvaliditydata[2] = gpsvalidity
  gpsvaliditydata[3] = 0xFF
  gpsvaliditydata[4] = 0xFF
   
  int gpsspeeddata[5]; 
  gpsvaliditydata[0] = 0x00
  gpsvaliditydata[1] = 0x00
  gpsvaliditydata[2] = gpsspeed
  gpsvaliditydata[3] = 0xFF
  gpsvaliditydata[4] = 0xFF
	  
void requestEvent() {
  
  for (int i = 0; i < 6; i++) {
  Wire.write(gpsvaliditydata);
   
  for (int i = 0; i < 6; i++) {
  Wire.write(gpsspeeddata);
   
  for (int i = 0; i < 15; i++) {

    Wire.write(gpslatdeg[i]);

  for (int i = 0; i < 15; i++) {

    Wire.write(gpslondata[i]);
   
  for (int i = 0; i < 12; i++) {

    Wire.write(gpsalt[i]);

}
 
  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis())  timer = millis();

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) { 
    timer = millis(); // reset the timer
    
    Serial.print("\nTime: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality); 
    if (GPS.fix) {
    Serial.print("Location: ");
    Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
    Serial.print(", "); 
    Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
    Serial.print("Location (in degrees, works with Google Maps): ");
    Serial.print(GPS.latitudeDegrees, 4);
    Serial.print(", "); 
    Serial.println(GPS.longitudeDegrees, 4);
      
    Serial.print("Speed (knots): "); Serial.println(GPS.speed);
    Serial.print("Angle: "); Serial.println(GPS.angle);
    Serial.print("Altitude: "); Serial.println(GPS.altitude);
    Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
    }
  }
}
	  
void setup(){
   Wire.begin(x);
   Wire.onRecieve(recieveEvent);
  
	
}
	Sim800l.begin(); // initializate the library. 
  if ( xbee_err = 1) {
	text="1";  //text for the message. 
	number="07415606808"; //change to a valid number.
	error=Sim800l.sendSms(number,text);
	// OR 
	//Sim800l.sendSms("+540111111111","the text go here")
}
  if ( lsm303_err = 2 ) {
  text="2";  //text for the message. 
  number="07415606808"; //change to a valid number.
  error=Sim800l.sendSms(number,text);
  // OR 
  //Sim800l.sendSms("+540111111111","the text go here")
}
if ( l3gd20_err = 4 ) {
  text="3";  //text for the message. 
  number="07415606808"; //change to a valid number.
  error=Sim800l.sendSms(number,text);
  // OR 
  //Sim800l.sendSms("+540111111111","the text go here")
}
if (bme280_err = 8 ) {
  text="4";  //text for the message. 
  number="07415606808"; //change to a valid number.
  error=Sim800l.sendSms(number,text);
  // OR 
  //Sim800l.sendSms("+540111111111","the text go here")
}
if ( d6t_err = 16 ) {
  text="5";  //text for the message. 
  number="07415606808"; //change to a valid number.
  error=Sim800l.sendSms(number,text);
  // OR 
  //Sim800l.sendSms("+540111111111","the text go here")
} 

void loop(){
  //do nothing
}
