# ESP32 and Azure IoT Explorer

# Overview

In this lab, you will learn how to upload ultrasonic sensor data to a Microsoft’s cloud computing sservice, Azure IoT Explorer

## Setup

Materials Required

- Jumper cables
- Ultrasonic sensor (HC-SR04) or another sensor of your choice
- ESP32-WROOM-32
- USB-C cable

### Pinout Diagram for ESP32

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled.png)

### Wiring Diagram

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%201.png)

---

## Getting Started with Azure IoT Hub

Log in to Azure, click on *IoT Hub*

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%202.png)

Create IoT hub

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%203.png)

Select the subscription affiliated with your UW account. Create a new Resource Name (IoTResourceTechin515). Create a name for your IoT Hub (hwswlab2). Select Free Tier, then Next: Networking. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%204.png)

Keep default settings and click Next: Management

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%205.png)

Seleect Role-based access control (RBAC) and click on IoT Hub Data Contributor Role (Assign me), then slect Next: Add-ons. Link to more info about RBAC. [Control access with Microsoft Entra ID - Azure IoT Hub | Microsoft Learn](https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad)

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%206.png)

You can skip Add-ons and Tags, and proceed to Review + create. Click on Create.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%207.png)

Deployment of the new IoT Hub may take a few minutes. Upon completion, click on “Add and configure IoT Devices”

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%208.png)

Select Add Device

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%209.png)

Provide a Device ID. In this example, the device ID is “ESP_WROOM_32” then click Save

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2010.png)

Then click on the Device to view the security and connection keys.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2011.png)

You now have access to the Device ID, Primary Key, Secondary Key, Primary Connection String, and Secondary Connection String. You will need the Device ID and the Primary Key later in this tutorial. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2012.png)

---

## Setting up your ESP32

Open Arduino IDE and navigate to Manage Libraries under Tools. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2013.png)

Search for “Azure SDK for C” and install the library. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2014.png)

After installing the library, navigate to File > Examples > Azure SDK for C > Azure Iot Hub ESP32

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2015.png)

A new window will open with a new sketch. Read through the “readme.md” tab and then click on the tab entitled, “iot_configs.h”.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2016.png)

In this tab, change the name of the WiFi network (line 5) and the WiFi password (line 6). If you want to connect the ESP32 to a network on campus, then you’ll have to connect to the UW MPSK network. You can register your device using [this website](https://itconnect.uw.edu/tools-services-support/networks-connectivity/uw-networks/campus-wi-fi/uw-mpsk/#connecting). In the iot_configs.h tab, change “SSID” to the name of your network (eg. “UW MPSK”) and change “PWD” to your WiFi password. 

Next, navigate down to the bottom of the tab and modify lines 56, 57, and 60 in the code (shown below) to include parameters related to your Azure IoT Hub project.  You can also change how frequently you publish messages to Azure in line 64. It’s currenlty set to publish messages every 2000 ms (2 seconds).

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2017.png)

In line 56, modify the IOT_CONFIG_IOTHUN_FQDN by locating your Hostname in the Overview section of the Azure IoT Hub that you just created. In this example the Hostname is “hwswlab2.azure-devices.net”

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2018.png)

In line 57, modify the IOT_CONFIG_DEVICE_ID to the name of your Device. In this example, the Device ID is “ESP_WROOM_32.” The Device ID can be found under the Device ID. In line 60, modify the IOT_CONFIG_DEVICE_KEY to your Primary Key. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2019.png)

Your new code may look similar to the entry below. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2020.png)

Next, return to Azure_IoT_Hub_ESP32.ino script. And make the following changes to the main script so that you can capture your sensor data and publish the data as a message through Azure. 

You’ll need to define the pins for the ultrasonic sensor, defien the speed of sound, and create two variables, *duration* and *distanceCm*. Add this code near the top of the script before any functions are created/called. 

```cpp
// Setting up the Ultrasonic Sensor
const int trigPin = 5;
const int echoPin = 18;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034

long duration;
float distanceCm;  // this value holds the distance measured by the ultrasonic sensor (in cm)
```

You’ll also need to change the void setup() and the void loop() main functions to define your INPUT and OUTPUT pins and run the cycling fucntion which calculates distance and initializes the sendTelemetry() function. You can copy and paste the entire block of code below and replace the void setup() and void loop() sections of the existing code. 

```cpp
// Arduino setup and loop main functions.

void setup() 
{
  establishConnection();
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input 
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    connectToWiFi();
  }
#ifndef IOT_CONFIG_USE_X509_CERT
  
  else if (sasToken.IsExpired())
  {
    Logger.Info("SAS token expired; reconnecting with a new one.");
    (void)esp_mqtt_client_destroy(mqtt_client);
    initializeMqttClient();
  }
#endif
  
  else if (millis() > next_telemetry_send_time_ms)
  { 
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    
    // Calculate the distance
    distanceCm = duration * SOUND_SPEED/2;

    if (isnan(distanceCm))  // Check if any reads failed and exit early (to try again).
    {
      Serial.println(F("Failed to read from Ultrasonic sensor!"));
      return;
    }
    
    // Prints the distance in the Serial Monitor
    Serial.print("Distance (cm): ");
    Serial.println(distanceCm);

    sendTelemetry();
    next_telemetry_send_time_ms = millis() + TELEMETRY_FREQUENCY_MILLISECS;
  }
}
```

Lastly, we need to modify the generateTelemetryPayload() function so that we are sending the distance data in our payload. Our payload will also contain information about how many messages have been sent (*telemetry_send_count++*)

```cpp
static void generateTelemetryPayload()
{
  // You can generate the JSON using any lib you want. Here we're showing how to do it manually, for simplicity.
  // This sample shows how to generate the payload using a syntax closer to regular delevelopment for Arduino, with
  // String type instead of az_span as it might be done in other samples. Using az_span has the advantage of reusing the 
  // same char buffer instead of dynamically allocating memory each time, as it is done by using the String type below.
  telemetry_payload = "{ \"msgCount\": " + String(telemetry_send_count++) + ", \"distance\": " + String(distanceCm) + " }";
}
```

Save and compile your new sketch then upload the program on to the ESP32. You can open a serial monitor to see if everything is working correctly. You should be connected to WiFi, printing distance data, and successfully publishing that data. 

---

## Installing and Configuring Azure IoT Explorer

To see your data streaming to the Azure IoT Hub service, we will use a software developed by Microsoft called Azure Iot Explorer.  Directions for installation from Microsoft are [here](https://learn.microsoft.com/en-us/azure/iot/howto-use-iot-explorer), but a step-by-step process is also provided below. 

Navigate to https://github.com/Azure/azure-iot-explorer/releases, and then download and install the .msi file in most recent release of the software tool. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2021.png)

After installing and opening the software tool, click on Add connection in the IoT Hub section. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/05eae5b5-e515-441a-adcc-8569a80899e8.png)

Now, open your Azure portal on your web browser and navigate to Shared access policies under Security Settings. Change the setting to Allow shared access policies then click on the iothubowner policy name. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2022.png)

Copy the Primary connection string and paste it in the Connection string entry box in Azure IoT Exmplorer.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2023.png)

Other boxes will autopopulate after you enter the Connection string. Then click on Save.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2024.png)

You should now be able to view your “ESP_WROOM_32” device in Azure IoT Hub.

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2025.png)

Click on your device, then click on Telemetry, then click on Start. Your sensor data should then begin streaming in the space below. 

![Untitled](ESP32%20and%20Azure%20IoT%20Explorer%208b50d0aa54764527b96213fdfc93b18f/Untitled%2026.png)