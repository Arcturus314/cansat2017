#include <Wire.h>

#include <Adafruit_GPS.h>

#include <SoftwareSerial.h>

#include <dht.h>

#define GPSECHO true

int transmitData[30]; //See docs for byte allocation

int receiveData[6]; //See docs for byte allocation

//pin allocation

int DHT22Data = 2;

int GPSRX = 3;

int GPSTX = 4;

int SIM800LRX = 7;

int SIM800LTX = 8;

//GPS setup

SoftwareSerial mySerial(GPSTX, GPSRX);

Adafruit_GPS GPS(&mySerial);

boolean usingInterrupt = false;

void useInterrupt(boolean);

//DHT22 setup

dht DHT;

#define DHT22_PIN 2

//SIM800L setup

SoftwareSerial serialSIM800(SIM800LTX, SIM800LRX);

void setup() {

  Wire.begin(10);               // join i2c bus with address #10

  Wire.onRequest(requestEvent); // register request event

  Wire.onReceive(receiveEvent); // register receive event

  Serial.begin(9600);           // start serial for output, ONLY FOR TESTING

  //filling array with 0s

  for (int i = 0; i < 30; i++) {

    transmitData[i] = 0;

  }

  //start bytes

  transmitData[0] = 0x00;

  transmitData[1] = 0x00;

  //end bytes

  transmitData[28] = 0xFF;

  transmitData[29] = 0xFF;

  //GPS setup cont

  GPS.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);

  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);

  useInterrupt(true);

  //SIM800L

  serialSIM800.begin(9600);

  serialSIM800.write("AT+CMGF=1\r\n");

  

  Serial.println("setup complete"); //ONLY FOR TESTING

  

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

void loop() {

  delay(100);

  //Data logging from sensors should go here

  //DHT22

  int chk = DHT.read22(DHT22_PIN);

  String hum = String(DHT.humidity);

  String temp = String(DHT.temperature);

  transmitData[2] = temp.charAt(0);

  transmitData[3] = temp.charAt(1);

  transmitData[4] = hum.charAt(0);

  transmitData[5] = hum.charAt(1);

  //GPS

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

    if(GPS.fix) {

      transmitData[26] = 0xFF; 

      String lat = String(GPS.latitude);

      String lon = String(GPS.longitude);

      for(int i = 0; i < 9; i++)

        transmitData[i+6] = lat.charAt(i);

      for(int i = 0; i < 9; i++)

        transmitData[i+15] = lon.charAt(i);      

      if(GPS.lon == 'W') transmitData[14] = 0xFF;

      if(GPS.lon == 'E') transmitData[14] = 0x00;

      if(GPS.lat == 'N') transmitData[23] = 0xFF;

      if(GPS.lat == 'S') transmitData[23] = 0x00;

      String spd = String(GPS.speed);

      transmitData[24] = spd.charAt(0);

      transmitData[25] = spd.charAt(1);

    }

    else {

      transmitData[26] = 0x00; 

      for(int i = 0; i < 20; i++) {

        transmitData[i+6] = 0x00;

      }

    }

  }

  

  //SIM800L

}

void requestEvent() {

  for (int i = 0; i < 30; i++) {

    Wire.write(transmitData[i]);

  }

  Serial.println("Data sent"); //ONLY FOR TESTING

}

void receiveEvent(int howMany) {

  int count = 0;

  while(Wire.available()) {

    receiveData[count] = Wire.read();

  }

  Serial.println("Data received"); //ONLY FOR TESTING

  interpretReceived(receiveData);

}

void sim_send(String toSend) {

  Serial.println("Texting...");

}

void interpretReceived(int data[]) {

  if(data[0] == 0x00 && data[1] == 0x00 && data[5] == 0xFF && data[6] == 0xFF) { //checking validity of sent data

    Serial.println("Data received is valid"); //ONLY FOR TESTING

    //Sensor control

    Serial.println("Sensor Control"); //ONLY FOR TESTING

    if(bitRead(data[2],7) == 0 && bitRead(data[2],6) == 0) {Serial.println("GPS off");} 

    else {Serial.println("GPS on");}

    if(bitRead(data[2],5) == 0 && bitRead(data[2],4) == 0) {Serial.println("SIM800L off");}

    else {Serial.println("SIM800L on");}

    if(bitRead(data[2],3) == 0 && bitRead(data[2],2) == 0) {Serial.println("DHT22 off");}

    else {Serial.println("DHT22 on");}

    //SIM800L to send

    Serial.println("SIM800L to send"); //ONLY FOR TESTING

    String toText = "";

    if(bitRead(data[3],6) == 0 && bitRead(data[3],7) == 1) {Serial.println("XBEE issues"); toText = toText + "XBEE FAIL; ";}

    if(bitRead(data[3],5) == 0 && bitRead(data[3],7) == 1) {Serial.println("6DOF issues"); toText = toText + "6DOF FAIL; ";}

    if(bitRead(data[3],4) == 0 && bitRead(data[3],7) == 1) {Serial.println("6DOF out-of-range"); toText = toText + "6DOF OOR; ";}

    if(bitRead(data[3],3) == 0 && bitRead(data[3],7) == 1) {Serial.println("Boot success"); toText = toText + "BOOT SUCCESS; ";}

    if(bitRead(data[3],2) == 0 && bitRead(data[3],7) == 1) {Serial.println("BMP issues"); toText = toText + "BMP FAIL";}

    Serial.println(toText); //ONLY FOR TESTING

    if(bitRead(data[3],7) == 1) {sim_send(toText);}

  }

}

