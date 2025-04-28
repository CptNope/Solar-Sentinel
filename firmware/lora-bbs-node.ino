// SolarSentinel - ESP32 LoRa BBS Node (Starter Sketch)

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

  Serial.println("SolarSentinel BBS Node Initialized.");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String incoming = "";
    while (LoRa.available()) {
      incoming += (char)LoRa.read();
    }
    Serial.println("Received: " + incoming);

    if (incoming.startsWith("LOGIN:")) {
      // Handle authentication (LoRa private only)
      LoRa.beginPacket();
      LoRa.print("Welcome to SolarSentinel BBS\n1. Status\n2. Waypoints\n3. Logout");
      LoRa.endPacket();
    } else if (incoming.startsWith("CMD:STATUS")) {
      LoRa.beginPacket();
      LoRa.print("Solar Voltage: 12.8V | Battery: OK");
      LoRa.endPacket();
    } else {
      LoRa.beginPacket();
      LoRa.print("Invalid Command.");
      LoRa.endPacket();
    }
  }
}
