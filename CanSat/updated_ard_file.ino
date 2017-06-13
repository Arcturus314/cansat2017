#include <Wire.h>

#include <Adafruit_GPS.h>

#include <SoftwareSerial.h>

#include <Sim800l.h>

Sim800l Sim800l;  //to declare the library
char* text;
char* number;
bool error; //to catch the response of sendSms

int xbee_err;
int lsm303_err;
int l3gd20_err;
int bme280_err;
int d6t_err;

SoftwareSerial mySerial(4, 3);

Adafruit_GPS GPS(&mySerial);

#define GPSECHO  false

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean);

void setup() {
  Wire.begin(10);               // join i2c bus with address #10
  Wire.onRequest(requestEvent); // register request event
  Wire.onReceive(receiveEvent); // register receive event
  Serial.begin(9600);           // start serial for output, ONLY FOR TESTING

  GPS.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);

  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);

  useInterrupt(true);

}

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

void loop() {
  delay(100);

  if (! usingInterrupt) {

    char c = GPS.read();

  }

  if (GPS.newNMEAreceived()) {

    if (!GPS.parse(GPS.lastNMEA()))

      return;

  }

  if (timer > millis())  timer = millis();

  if (millis() - timer > 2000) {

    timer = millis();

    if (GPS.fix) {

      String gpslatdeg = String(GPS.latitudeDegrees);
      String gpslongdeg = String(GPS.longitudeDegrees);
      String gpsspeed = String(GPS.speed);
      String gpsaltitude = String(GPS.altitude);
      String gpsvalidity = String(GPS.fix);

      int gpslatdegdata[14];
      gpslatdeg[0] = 0x00;
      gpslatdeg[1] = 0x00;
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
      gpslatdeg[12] = 0xFF;
      gpslatdeg[13] = 0xFF;

      int gpslondata[14];
      gpslondata[0] = 0x00;
      gpslondata[1] = 0x00;
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
      gpslondata[12] = 0xFF;
      gpslondata[13] = 0xFF;

      int gpsalt[14];
      gpsalt[0] = 0x00;
      gpsalt[1] = 0x00;
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
      gpsalt[12] = 0xFF;
      gpsalt[13] = 0xFF;

      int gpsvaliditydata[5];
      gpsvaliditydata[0] = 0x00;
      gpsvaliditydata[1] = 0x00;
      gpsvaliditydata[2] = gpsvalidity.charAt(0);
      gpsvaliditydata[3] = 0xFF;
      gpsvaliditydata[4] = 0xFF;

      int gpsspeeddata[9];
      gpsspeeddata[0] = 0x00;
      gpsspeeddata[1] = 0x00;
      gpsspeeddata[2] = gpsspeed.charAt(0);
      gpsspeeddata[3] = gpsspeed.charAt(1);
      gpsspeeddata[4] = gpsspeed.charAt(2);
      gpsspeeddata[5] = gpsspeed.charAt(3);
      gpsspeeddata[6] = gpsspeed.charAt(4);
      gpsspeeddata[7] = 0xFF;
      gpsspeeddata[8] = 0xFF;

    }
    void requestEvent() {

      for (int i = 0; i < 6; i++) {
        Wire.write(gpsvaliditydata[i]);

      }

      for (int i = 0; i < 10; i++) {
        Wire.write(gpsspeeddata[i]);

      }
      for (int i = 0; i < 16; i++) {

        Wire.write(gpslatdegdata[i]);

      }

      for (int i = 0; i < 16; i++) {

        Wire.write(gpslondata[i]);

      }
      for (int i = 0; i < 15; i++) {

        Wire.write(gpsalt[i]);

      }
    }
    void receiveEvent() {
      Wire.read()
      Sim800l.begin(); // initializate the library.
      if ( xbee_err = 1) {
        text = "1"; //text for the message.
        number = "07415606808"; //change to a valid number.
        error = Sim800l.sendSms(number, text);
        // OR
        //Sim800l.sendSms("+540111111111","the text go here")
      }
      if ( lsm303_err = 2 ) {
        text = "2"; //text for the message.
        number = "07415606808"; //change to a valid number.
        error = Sim800l.sendSms(number, text);
        // OR
        //Sim800l.sendSms("+540111111111","the text go here")
      }
      if ( l3gd20_err = 4 ) {
        text = "3"; //text for the message.
        number = "07415606808"; //change to a valid number.
        error = Sim800l.sendSms(number, text);
        // OR
        //Sim800l.sendSms("+540111111111","the text go here")
      }
      if (bme280_err = 8 ) {
        text = "4"; //text for the message.
        number = "07415606808"; //change to a valid number.
        error = Sim800l.sendSms(number, text);
        // OR
        //Sim800l.sendSms("+540111111111","the text go here")
      }
      if ( d6t_err = 16 ) {
        text = "5"; //text for the message.
        number = "07415606808"; //change to a valid number.
        error = Sim800l.sendSms(number, text);
        // OR
        //Sim800l.sendSms("+540111111111","the text go here")
      }
    }
