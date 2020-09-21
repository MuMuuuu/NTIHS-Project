#include <ESP8266WiFi.h>
WiFiClient Reading;

WiFiClient client;
String writeAPIkey ="BPP9MWS1MN6JMAJN";
String readAPIkey ="772Y66GKM1WDJY20";
char* SSIDname = "Kev";
char* SSIDpw = "U maniac";
/*IPAddress ip(172,16,82,34);
IPAddress gateway(172,16,82,254);
IPAddress subnet(255,255,255,0);*/
String thingSpeakValue;
String clientDataReceive(){
  uint8_t myData[256] = {0};
  int i = 0;
  while(1){
  if(client.available()) {
    char c = client.read();
    myData[i++] = c;
  }else{
    String inData((const char*)myData);
    return inData;
  }
}
  return "";
}

String thingspeakReadData(String read_key ,int channel_id, int field_id, int record_id){
  uint8_t myData[180] = {0};
  int dataIdx = 0;
  String inData = "";
  if(client.connect("api.thingspeak.com", 80)) {
    String things_request = "GET /channels/" + String(channel_id) + "/fields/" + String(field_id) + "/last?api_key=" + String(read_key) + "\r\n\r\n";
    client.print(things_request);
    delay(2000);
    inData = clientDataReceive();
    return inData;
  }


  
}




void setup() {
  /*myServo.attach(5); // 伺服馬達物件連接到接腳1
  Serial.begin(9600);
  */
    pinMode(16, OUTPUT);
//  pinMode(10, OUTPUT);
    Serial.begin(9600);
    
 // WiFi.config(ip,gateway,subnet);
  WiFi.begin(SSIDname,SSIDpw);
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());
}

void loop() {
  int X;
  thingSpeakValue = thingspeakReadData(readAPIkey , 1145974, 1, 0);
  Serial.println(thingSpeakValue);
  Reading.println(thingSpeakValue.toInt());
  X=thingSpeakValue.toInt();
  if(X==1){
    digitalWrite(16,HIGH);
    }
   if(X==0){
    digitalWrite(16,LOW);
    }
  
  /*myServo.write(thingSpeakValue.toInt);*/
  delay(1000);
  /*digitalWrite(16,HIGH);  
  digitalWrite(10,HIGH);  
  delay(200);
  digitalWrite(16,LOW); 
  digitalWrite(10,LOW); 
  delay(200);
  */
  }
