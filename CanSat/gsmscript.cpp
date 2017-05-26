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

void setup(){
   Wire.begin(x);
   Wire.onRecieve(recieveEvent);
   serial.begin(9600);
	
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
