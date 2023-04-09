#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <SoftwareSerial.h>
#include <DHT.h>

const char* ssid = SSID
const char* password = "Network password";
const char* server_url = "Server Url"; //

SoftwareSerial arduinoSerial(9, 10); // RX, TX

void setup() {
   Serial.begin(9600);
  arduinoSerial.begin(9600);
  delay(1000);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    WiFiClient client;
    HTTPClient http;
    http.begin(client, server_url);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpCode = http.POST("data=" + data);
    if (httpCode == 200) {
      Serial.println("Data sent successfully!");
    } else {
      Serial.println("Error sending data!");
    }
    http.end();
  }
}