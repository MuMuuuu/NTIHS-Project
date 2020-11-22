#include <ESP8266WiFi.h>
#include <MQTT.h>

WiFiClient client;
MQTTClient mqtt;

char* SSIDname = "Kev";
char* SSIDpw = "U maniac";

int stat = 0;
/*IPAddress ip(172,16,82,34);
IPAddress gateway(172,16,82,254);
IPAddress subnet(255,255,255,0);*/

void connect() {
  Serial.print("checking wifi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.print("\nconnecting...");
  while (!mqtt.connect("arduino", "try", "try")) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\nconnected!");
  /***************************************************************************************
   * change dis*
   **************************************************************************************/
  mqtt.subscribe("4_writein", 2);
  

}

void message_received(String &topic, String &payload) {
  Serial.println("get: " + topic + " : " + payload);
  
  stat = char(payload[0])-'0';
  digitalWrite(16, stat);

}



void setup() {
  /*myServo.attach(5); // 伺服馬達物件連接到接腳1
  Serial.begin(9600);
  */
  pinMode(16, OUTPUT);
//   pinMode(10, OUTPUT);
  Serial.begin(9600);
    
//   WiFi.config(ip,gateway,subnet);
  WiFi.begin(SSIDname,SSIDpw);
  mqtt.begin("219.68.154.148", client);
  mqtt.onMessage(message_received);
  
  connect();
}

void loop() {
  
  mqtt.loop();
  
  while (!mqtt.connected()) {
    connect();
  }



  /***************************************************************************************
   * change dis*
   **************************************************************************************/

  mqtt.publish("4_feedback", String(stat), 10, 2);
  
  

  
  /*myServo.write(thingSpeakValue.toInt);*/
  delay(500);
  /*digitalWrite(16,HIGH);  
  digitalWrite(10,HIGH);  
  delay(200);
  digitalWrite(16,LOW); 
  digitalWrite(10,LOW); 
  delay(200);
  */
  }
