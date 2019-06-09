#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float celsius = -200.0;

const char* ssid = "...";
const char* password = "...";
const char* fullServiceName = "http://localhost:8888/postjson";


void setup() {
  Serial.begin(9600);
  sensors.begin();
  WiFi_Connect();
}

void loop() {
   if(WiFi.status() == WL_CONNECTED){
      StaticJsonBuffer<300> JsonBuffer; 
      JsonObject& postData = JsonBuffer.createObject();
    
      sensors.requestTemperatures(); 
      float temp = sensors.getTempCByIndex(0);

      if (temp > celsius){
        postData["title"] = "esp8266#2";
          postData["id"] = 1;
        postData["temperature"] = temp;
        postData.printTo(Serial);
      } 
      else
        Serial.println("Temperature is below -200°C.");

      char JsonMessageBuffer[300];
      postData.printTo(JsonMessageBuffer);
    
      HTTPClient http;
      http.begin(fullServiceName); 
      http.addHeader("Content-Type", "application/json");
      
      int httpCode = http.POST(JsonMessageBuffer);
  
      if(httpCode>0){
  
        String response = http.getString();
        Serial.println(httpCode);    
        Serial.println(response);
      }else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpCode);      
      }
      http.end();
      
    }else
    {
      Serial.println("Error in WiFi connection");
      WiFi_Connect();
    }
      delay(15000);
}

void WiFi_Connect()
{
  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to wifi ");
  while(WiFi.status() != WL_CONNECTED){
      delay(500);
      Serial.print(".");
    }
    Serial.println(" connected!");
}
