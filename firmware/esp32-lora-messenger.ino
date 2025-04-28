// SolarSentinel - ESP32 LoRa Messenger Node

#include <SPI.h>
#include <LoRa.h>

#define SS_PIN 18
#define RST_PIN 14
#define DIO0_PIN 26

void setup() {
  Serial.begin(9600);
  while (!Serial);

  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  Serial.println("LoRa Messenger Node Ready.");
}

void loop() {
  if (Serial.available()) {
    String message = Serial.readString();
    LoRa.beginPacket();
    LoRa.print(message);
    LoRa.endPacket();
    Serial.println("Sent: " + message);
  }
}
