
#include <LiquidCrystal.h>

#include "DHT.h"
#include <SoftwareSerial.h>
#define DHTPIN 6     

#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const char BUTTON_PIN = 7;
enum TempScale {Celsius, Fahrenheit};
TempScale tempScale = Celsius;
SoftwareSerial espSerial(9, 10); // RX, TX
void setup() {
   Serial.begin(9600);
  espSerial.begin(9600);
  delay(1000);
  Serial.println(F("DHTxx test!"));

  dht.begin();
  lcd.begin(16, 2);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  
  pinMode(RELAY_PIN, OUTPUT);
  // Print a message to the LCD.
}

void loop() {

      delay(1250);
        digitalWrite(RELAY_PIN, HIGH); // turn on the relay
  bool currentState = digitalRead(BUTTON_PIN);
    static bool previousState = HIGH; // initialize the previous state to HIGH
  
  if (previousState == HIGH && currentState == LOW) {
    // swap the temperature scale
    if (tempScale == Celsius) {
      tempScale = Fahrenheit;
    } else {
      tempScale = Celsius;
    }
  }
  previousState = currentState;
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }


  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);
  lcd.clear();
  lcd.print(F("Temp: "));
    lcd.print(t);
    lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print(F("Humidity: "));
  lcd.print(h);
  lcd.print(" %");
  String data = "serial_number=serial_number&temp=" + String(t) + "&humidity=" + String(h);
   espSerial.println(data);
  

}