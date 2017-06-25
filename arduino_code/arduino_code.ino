
#include <Wire.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

int GPSRX = 3;
int GPSTX = 4;

String returnList = "";
int count;

//GPS setup
#define GPSECHO false
SoftwareSerial mySerial(GPSTX, GPSRX);
Adafruit_GPS GPS(&mySerial);
boolean usingInterrupt = false;
void useInterrupt(boolean);

/*
   Message allocation
   0: ':'
   1: Fix (1 byte)      + ','
   2: Speed             + ','
   3: Altitude          + ','
   4: Latitude          + ','
   5: Longitude         + ','
   6: 
*/



int receiveData[6];

void setup()
{
  count = 0;
  
  //Serial.begin(115200);
  Wire.begin(75);               // join i2c bus with address #75
  Wire.onRequest(requestEvent); // register request event
  Wire.onReceive(receiveEvent); // register receive event

  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  useInterrupt(true);

  delay(1000);

  //Serial.println("setup complete"); //ONLY FOR TESTING

  pinMode(13, OUTPUT);
}


//GPS shit
// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;
  // writing direct to UDR0 is much much faster than //Serial.print
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

void loop()
{

  //GPS
  if (! usingInterrupt) {
    char c = GPS.read();
    if (GPSECHO)
      if (c) Serial.print(c);
  }
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
  if (timer > millis())  timer = millis();
  if (millis() - timer > 2000) {
    timer = millis();
    
    //Serial.print("Fix: ");      //Serial.println((int)GPS.fix);
    //Serial.print("Latitude ");  //Serial.println(String(GPS.latitudeDegrees));
    //Serial.print("Longitude "); //Serial.println(String(GPS.longitudeDegrees));
  }
}

String buildList() {
  int list_length = 7; // length with only seperators and fix byte
  int index = 0;
  String   fix     = String(GPS.fix);
  //Serial.println(fix);
  String in_speed  = String(GPS.speed);
  //Serial.println(in_speed);
  String altitude  = String(GPS.altitude);
  //Serial.println(altitude);
  String latitude  = String(GPS.latitudeDegrees);
  //Serial.println(latitude);
  String longitude = String(GPS.longitudeDegrees);
  //Serial.println(longitude);

  list_length += (in_speed.length()+altitude.length()+latitude.length()+longitude.length());
  //Serial.print("list length: ");
  //Serial.println(list_length);
  
  char list[list_length];

  list[0] = ':';
  //Fix
  list[1] = fix.charAt(0);
  list[2] = ',';
  index = 3;
  //Speed
  //Serial.println("filling speed...");
  //Serial.print("speed length: ");
  //Serial.println(in_speed.length());
  for(int i=0;i<in_speed.length();i++) {
    //Serial.print(i);
    //Serial.print(" ");
    //Serial.print(in_speed.charAt(i));
    //Serial.print(" ");
    //Serial.println(index);
    list[index] = in_speed.charAt(i);
    index++;
  }
  //Serial.println("speed filled");
  //Serial.print("0 , ");
  //Serial.println(index);
  list[index] = ',';
  index++;
  //Altitude
  //Serial.println("filling altitude...");
  //Serial.print("altitude length: ");
  //Serial.println(altitude.length());
  for(int i=0;i<altitude.length();i++) {
    //Serial.print(i);
    //Serial.print(" ");
    //Serial.print(altitude.charAt(i));
    //Serial.print(" ");
    //Serial.println(index);
    list[index] = altitude.charAt(i);
    index++;
  }
  //Serial.println("Altitude filled");
  //Serial.print("0 , ");
  //Serial.println(index);
  list[index] = ',';
  index++;
  //Latitide
  //Serial.println("filling latitude...");
  //Serial.print("latitude length: ");
  //Serial.println(latitude.length());
  for(int i=0;i<latitude.length();i++) {
    //Serial.print(i);
    //Serial.print(" ");
    //Serial.print(latitude.charAt(i));
    //Serial.print(" ");
    //Serial.println(index);
    list[index] = latitude.charAt(i);
    index++;
  }
  //Serial.println("latitude filled");
  //Serial.print("0 , ");
  //Serial.println(index);
  list[index] = ',';
  index++;
  //Longitude
  //Serial.println("filling longitude...");
  //Serial.print("longitude length: ");
  //Serial.println(longitude.length());
  for(int i=0;i<longitude.length();i++) {
    //Serial.print(i);
    //Serial.print(" ");
    //Serial.print(longitude.charAt(i));
    //Serial.print(" ");
    //Serial.println(index);
    list[index] = longitude.charAt(i);
    index++;
  }
  //Serial.println("Longitude filled");
  //Serial.print("0 , ");
  //Serial.println(index);
  list[index]=',';
  //Serial.print("full list: ");
  //Serial.println(list);
  return String(list);
}

void requestEvent() {
  //Serial.println("requestEvent");
  digitalWrite(13, HIGH);
  if(0 == returnList.length()) { //to initialize the list
    //Serial.print("initializing list... List length: ");
    //Serial.println(returnList.length());
    returnList = buildList();
  }
  if(count == returnList.length()-1) { //to fill the list after one complete send
    //Serial.print("filling list... List length: ");
    //Serial.println(returnList.length());
    returnList = buildList();
    count = 0;
  }

  if(returnList.charAt(count) != '\x12' && returnList.charAt(count) != '\x06')
    Wire.write(returnList.charAt(count));
  //Serial.print("Count: ");
  //Serial.print(count);
  //Serial.print(" character: ");
  //Serial.println(returnList.charAt(count));
  //Serial.print(" Length: ");
  //Serial.println(returnList.length());
  count++;
  
  digitalWrite(13, LOW);
}

void receiveEvent(int howMany) {
  //Serial.println("receiveEvent");
  int count = 0;
  for (int i = 0; i < howMany; i++) {
    receiveData[i] = Wire.read();
  }
}

