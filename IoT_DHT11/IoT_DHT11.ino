#include <dht11.h>
dht11 DHT11;

#define DHT11PIN 8

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 TEST PROGRAM");
  Serial.print("LIBRARY");
  Serial.println(DHT11LIB_VERSION);
  Serial.println();
}

void loop() {
  static int counter = 0;
  if (counter < 1000) {
    Serial.println("\n");
    int chk = DHT11.read(DHT11PIN);
    Serial.print("Read sensor: ");
    switch (chk) {
      case DHTLIB_OK: 
        Serial.println("OK"); 
        break;
      case DHTLIB_ERROR_CHECKSUM: 
        Serial.println("Checksum error"); 
        break;
      case DHTLIB_ERROR_TIMEOUT: 
        Serial.println("Time out error"); 
        break;
      default: 
        Serial.println("Unknown error"); 
        break;
    }

    Serial.print((float)DHT11.humidity, 2);
    Serial.print(",");
    Serial.print((float)DHT11.temperature, 2);

    delay(2000);
    counter++;
  } else {
    Serial.println("Data output completed. Stopping...");
    while (true) {
    }
  }
}

