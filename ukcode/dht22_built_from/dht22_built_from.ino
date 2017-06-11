
#include <Wire.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

int GPSRX = 3;
int GPSTX = 4;

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
*/



int receiveData[6];

void setup()
{
  Serial.begin(115200);
  Wire.begin(75);               // join i2c bus with address #75
  Wire.onRequest(requestEvent); // register request event
  Wire.onReceive(receiveEvent); // register receive event

  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  useInterrupt(true);

  delay(1000);

  Serial.println("setup complete"); //ONLY FOR TESTING

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
    
    Serial.print("Fix: ");      Serial.println((int)GPS.fix);
    Serial.print("Latitude ");  Serial.println(String(GPS.latitudeDegrees));
    Serial.print("Longitude "); Serial.println(String(GPS.longitudeDegrees));
  }
}


void requestEvent() {
  digitalWrite(13, HIGH);
  Wire.write(':');
  //Fix
  Wire.write(char(GPS.fix));
  Wire.write(',');
  //Speed
  for(int i=0;i<String(GPS.speed).length();i++) {
    Wire.write(String(GPS.speed).charAt(i));
  }
  Wire.write(',');
  //Altitude
  for(int i=0;i<String(GPS.altitude).length();i++) {
    Wire.write(String(GPS.altitude).charAt(i));
  }
  Wire.write(',');
  //Latitide
  for(int i=0;i<String(GPS.latitudeDegrees).length();i++) {
    Wire.write(String(GPS.latitudeDegrees).charAt(i));
  }
  Wire.write(',');
  //Longitude
  for(int i=0;i<String(GPS.longitudeDegrees).length();i++) {
    Wire.write(String(GPS.longitudeDegrees).charAt(i));
  }

  digitalWrite(13, LOW);
}

void receiveEvent(int howMany) {
  int count = 0;
  for (int i = 0; i < howMany; i++) {
    receiveData[i] = Wire.read();
  }
}

