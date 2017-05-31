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
