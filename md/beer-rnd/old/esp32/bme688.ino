#include "Arduino.h"
#include "bme68xLibrary.h"
#include <Wire.h>
#include <WiFi.h>
#include "PubSubClient.h"

// WiFi credentials
const char* ssid = "REDACTED"; // Define the WiFi SSID
const char* password ="REDACTED"; // Define the WiFi password

// MQTT broker information
const char* mqtt_server = "192.168.66.218"; // Define the MQTT broker IP address
const char* mqtt_topic = "/bme688/gas"; // Define the MQTT topic
const char* mqtt_user = ""; // Define the MQTT username
const char* mqtt_pass = ""; // Define the MQTT password
const char* mqtt_port = "1883"; // Define the MQTT port

int status = 0; // Initialize a variable for sensor status
int temperature = 0; // Initialize a variable for temperature readings
int pressure = 0; // Initialize a variable for pressure readings
int humidity = 0; // Initialize a variable for humidity readings
int gasresistance = 0; // Initialize a variable for gas resistance readings

#ifndef SENSOR_ADDR
#define SENSOR_ADDR 0x76 // Define the I2C address of your BME68x sensor
#endif

#ifndef I2C_SCL
#define I2C_SCL 16 // Define the pin for SCL
#endif

#ifndef I2C_SDA
#define I2C_SDA 17 // Define the pin for SDA
#endif

Bme68x bme; // Initialize the BME68x sensor object

// Create a WiFi client and a PubSubClient instance
WiFiClient espClient;
PubSubClient client(espClient);

// Function to set up WiFi connection
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi");

  // Connect to WiFi using the provided credentials
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  // Wait for the WiFi connection to be established
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// Setup function to initialize WiFi connection and set up MQTT server
void setup() {
  // Initialize I2C communication
  Wire.begin(I2C_SDA, I2C_SCL); 
  Serial.begin(115200);

  while (!Serial)
      delay(10);

  // Initializes the sensor based on I2C communication
  bme.begin(SENSOR_ADDR, Wire);

  // Check if the sensor was successfully initialized
  if (bme.status != BME68X_OK)
  {
      Serial.println("Sensor not found. Please check wiring.");
      while (1)
          ;
  }

  Serial.println("Sensor found.");

  // Set the default configuration for temperature, pressure, and humidity
  bme.setTPH();

  // Set the heater configuration to 300 deg C for 100ms for Forced mode
  bme.setHeaterProf(300, 100);

  setup_wifi();
  client.setServer(mqtt_server, atoi(mqtt_port)); // Convert mqtt_port to integer

}

// Function to reconnect to the MQTT broker if the connection is lost
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Attempt to connect to the MQTT broker with the given client ID, username, and password
    if (client.connect("ESP32Client", mqtt_user, mqtt_pass)) {
      Serial.println("connected");
    } else {
      // Print an error message and retry after 1 second if the connection attempt fails
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 second");
      delay(1000);
    }
  }
}

// Main loop
void loop() {
  bme68xData data;

  bme.setOpMode(BME68X_FORCED_MODE);

  // If the MQTT client is not connected, attempt to reconnect
  if (!client.connected()) {
    reconnect();
  }

  // Maintain the MQTT connection and handle incoming messages
  client.loop();
  char message1[50] = ""; // Initialize a buffer for MQTT messages
  char message2[50] = ""; // Initialize a buffer for MQTT messages
  // Fetch sensor data
  if (bme.fetchData()){
    bme.getData(data);
    status = (data.status);  
    if (status == 176){
      temperature = data.temperature;
      pressure = data.pressure;
      humidity = data.humidity;
      gasresistance = data.gas_resistance;
      String(gasresistance).toCharArray(message1, sizeof(message1));
      String(temperature).toCharArray(message2, sizeof(message2));
      
      // Publish a message to the specified MQTT topic
      client.publish(mqtt_topic, message1);      
      Serial.print("gas resistance: "); 
      Serial.print(message1);

      // Publish a message to the specified MQTT topic      
      client.publish(mqtt_topic, message2); 
      Serial.print(", temperature: "); 
      Serial.print(message2);
      Serial.print(", ");
    }

    Serial.print("status: ");
    Serial.println(status, HEX);
  
  }

  delay(60000);

}
