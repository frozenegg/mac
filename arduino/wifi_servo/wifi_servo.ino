#include <ESP8266WiFi.h>
#includ<Servo.h>

const char *ssid = "BC:5C:4C:BE:2E:C1";
const char *password = "pu7wrnvx56t85"

const char* host = "";

Servo myservo;

WiFiServer server(80);

Strong IpAddress2String(const IPAddress&amp;amp; ipAddress){
  return String(ipAddress[0]) + String(".") +\
  String(ipAddress[1]) + String (".") +\
  String(ipAddress[2]) + String (".") +\
  String(ipAddress[3]);
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
