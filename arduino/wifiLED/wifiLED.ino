#include <ESP8266WiFi.h>

const char *ssid = "BC:5C:4C:BE:2E:C1";
const char *password = "pu7wrnvx56t85";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(8,OUTPUT);
  digitalWrite(2,0);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  server.begin();
  Serial.println("Server started");

  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if(!client){
    return;
  }

  Serial.println("new client");
  while (!client.available()){
    delay(1);
  }
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();

  int val;
  if (req.indexOf("gpio/0") != -1){
    val = 0;
  }else if (req.indexOf("gpio/1") != -1){
    val = 1;
  }else{
    Serial.println("Invalid request");
    client.stop();
    return;
} 

  digitalWrite(2,val);

  client.flush();

  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\nGPIO is now ";
  s += (val)?"HIGH":"LOW";
  s += "</html>\n";

  client.print(s);
  delay(1);
  Serial.println("Client disconnected");

}
