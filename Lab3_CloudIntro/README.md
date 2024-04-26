# Lab 3: Introduction to Cloud Computing

## (a) ESP32 and Amazon Web Services

## Overview
In this lab, you will learn how to upload sensor data to a cloud storage service.

## Setup
Materials Required

* Jumper cables
* Ultrasonic sensor (HC-SR04) or another sensor of your choice
* ESP32-WROOM-32
* USB-C cable
  
## Pinout Diagram for ESP32

<img width="637" alt="Untitled" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/94565a27-1d8e-44db-b8e7-74eaa0deabc3">

## Wiring Diagram

<img width="474" alt="Untitled 1" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/dd8f7c54-9559-4f31-a34a-902b25b1e31b">


## Getting Started with Amazon AWS IoT Core
### Signing In
Go to your web browser and search visit following link: [aws.amazon.com/iot-core/](https://aws.amazon.com/iot-core/). Sign in the the Console.

<img width="836" alt="Untitled 2" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/553d8d2d-a74a-4749-b56d-f921cdd6e061">

Create a new AWS account if you don’t already have one. You’ll have to use an email and a password. The account also requires a credit card, but there will be no charges. Phone number verification is also required. 

<img width="383" alt="Untitled 3" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/deadb6c7-1adc-45f7-a269-bd9927ec46ab">


## AWS IoT Core Dashboard
After you sign up, the AWS Management Console window will open. In the search tab at the top, type “IoT core” and press ‘Enter.’

![Untitled 4](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ea548dca-e5f1-494d-a9c2-b05f8e056fe7)

## Create a Thing
A “thing” resource is a digital representation of a physical device. A thing resource uses “certificates” to secure communication between your device and AWS IoT. When a device connects to AWS IoT, policies enable it to subscribe and publish MQTT messages with AWS IoT message broker. 

MQTT is a protocol used to transfer data in a network and was designed for low-bandwidth, high-latency connections with unreliable networks -  perfect for applications in connected devices. This protocol is useful when IoT devices need to communicate with each other or with a central server. 

MQTT uses a publish/subsribe messaging pattern, which means that devices (or “MQTT clients”) can publish information (or “messages” or “MQTT Packets”) to topics, and other devices (also “MQTT clients”) can subscribe to those topics to receive that same information. In this example using an ESP32 with an ultrasonic distance sensor, the topic name might be “distance” and message content (or “payload”) might be 32.12 centimeters, for example. MQTT Clients can be only publishers, only subscribers, or both publishers and subscribers. Here is a 6-minute YouTube video if you would like a brief overview of MQTT. 

In this lab, AWS IoT is the “message broker” which means that AWS IoT retains messages and then delivers the messages to topic subscribers. In this lab, your ESP32 will serve as both the publisher and the subscriber, simultaneously. 

Under the “Manage” option, click on the dropdown for the “All devices” option, then click on “Things. Click on “Create Things”

<img width="886" alt="Untitled 5" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/8d9583dc-52ff-4e73-a6fe-d6c984dc063b">

Create a single think and click next.

<img width="630" alt="Untitled 6" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/382c2d01-6e8d-4e34-86d3-f74281d6e91f">

Next we need to specify the Thing properties. First, give the Thing a name. You can name it anything, but do not use a hyphen (-) in the Thing name. In this example, the Thing is named “ESP_WROOM_32.” You will need this name at a later part of this lab, so make sure to write it down. No additional changes need to be named. Select No Shadow, then click Next. 

<img width="535" alt="Untitled 7" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ec6c5a11-5c3f-4bbe-a71e-698337381c61">

Next you need to configure the device certificate. In this section, we will auto-generate a new certificate. The certifcate verifies the identifty of a device and secures communciation between the device (”MQTT Client”) and AWS IoT (”message broker”).

## Generate Device Certificate

<img width="677" alt="Untitled 8" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/9d67146d-20db-4bbf-8f34-773a293a05e5">

Since we don’t yet have any policies granting or denying access to AWS IoT resources, we’ll need to create a policy. This policy will attach to the device certificate and allow our ESP32 to access AWS IoT. 

## Create and Attach a Policy to the Certificate
<img width="377" alt="Untitled 9" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/a335559b-1a94-4c01-9e90-ba480323b853">

After we create a policy, we have to name the policy. For the purpose of this lab, the name of the policy is “ESP_WROOM_32_Policy” (see image below). 
![361cb2a0-6b71-4379-b271-a858767e4bb6](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/1f9cccc8-2a30-4f51-81cd-9d033cc1d0b2)

Next, in the Policy document section, we can define the relationship that our ESP32 (”MQTT client”) has with AWS IoT (”message broker”). We can define the Policy in two different ways - through the Builder function or through the JSON function. Because we want our ESP32 to both publish message and subscribe to the topic, we must allow our IoT device to (1) connect with the AWS IoT message broker, (2) subscribe to a topic, (3) receive messages from AWS IoT, and (4) publish an MQTT topic (not necessarily in that order).  You can select these actions in the Policy Action section and then define the Policy resources, or you can click on the JSON function and read the instructions further below.

If you want to work in the Builder function, then you have to define the Policy resource for each action. In this case, we need to provide the Amazon Reource Name (or ARN). The  general format for ARNs for this Policy document is “arn:partition:service:region:account-id:resource-type/resource-id”. 

<img width="806" alt="Untitled 10" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ba2be620-caa4-4747-b845-e4a67cf56de6">


The resource-id will match the topic that you will assign later in your Arduino code (see example below).

```bash
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"
```

Alternatively, you can click on the JSON button and copy and paste the JavaScript code below into the text box. Whether you use the Builder or JSON function, you need to replace REGION in each of the four sections of the text with the matching AWS Region in which you’re currently operating.  You can find your Region at this AWS resource.  In Washington state, the region is “us-east-2”.  Replace ACCOUNT_ID in each section with your own account ID. Your account ID can be found in your AWS Account Settings. Replace THINGNAME in the first section of the text with the name you gave to your Thing. In this tutorial the Thing’s name was defined as “ESP_WROOM_32.” Then, click on Create. 

```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:REGION:ACCOUNT_ID:client/THINGNAME"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Subscribe",
      "Resource": "arn:aws:iot:REGION:ACCOUNT_ID:topicfilter/esp32/sub"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Receive",
      "Resource": "arn:aws:iot:REGION:ACCOUNT_ID:topic/esp32/sub"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:iot:REGION:ACCOUNT_ID:topic/esp32/pub"
    }
  ]
}
```

Next, return to the Create Single Thing tab and select the new policy that you created. Then press Create Thing.

<img width="742" alt="Untitled 11" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/450bbdfa-9cfe-4bf8-ae4a-8f3b46655748">

If you’d like to view the policy that you just created, then you cand find it by navigating to the menu on the left side of the AWS portal, find Manage, then select Security, then Policies.  

<img width="881" alt="Untitled 12" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/c793c1bc-393a-4c31-a113-45ff7462d365">


## Download Certificates and Keys
Now we need to download the required certificates from this list. 

First, download the device certificate and then rename it as “Device Certificate” for identification.

Then, download the private key and rename it as a “Private Key”.

In the Root CA Certificates, there are two certificates here. But we just need a Root CA1 certificate, so download it as well.

![Untitled 13](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/f9c85b76-c835-4d0f-9089-d1f8007c023d)


Finally, in the AWS dashboard navigate to Security then Certificates. Select the certificate that you just created for your device and choose Actions, then Attach policy. Choose the policy you just created and attach it to the certificate. In this example the policy name is “ESP_WROOM_32_Policy.”


<img width="857" alt="Untitled 14" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/cc8e219a-7849-4cbf-b67b-91934938b173">

## Installing Necessary Arduino Libraries


Now that you’ve created your Thing on AWS IoT, downloaded your certifcates, and attached policies to those certificates, we are ready to begin working in Arduino IDE or PlatformIO. The example below is shown in Arduino IDE.

## AdruinoJSON Library
In Arduino IDE or PlatformIO, navigate to the library manager and search for “JSON” in the search bar. Install the “ArduinoJson” library by Benoit Blanchon (seen below)

![Untitled 15](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/69b55cbd-303d-428d-977b-1e2eaa4767fd)

## PubSubClient
Also install the library called “PubSubClient” by Nick O’Leary. 

![Untitled 16](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ef531b60-e5b6-49ae-9a93-eb056a5550a5)


Source Code for Connecting AWS IoT Core with ESP32
The code/program that interfaces the ESP32 with the HC-SR04 ultrasonic sensor and connects to the Amazon AWS IoT Core is written in Arduino IDE. The code is divided into two sections. One is the main ino file and other is a header file named Secrets.h.

Remember, in order to connect the ESP32 to the UW MPSK WiFi network, you’ll have to register the device’s MAC address through this UW website.  You’ll want to copy the WiFi password after you register your device. The password will be needed later. Below is the code to find your ESP32’s MAC address:Source Code for Connecting AWS IoT Core with ESP32
The code/program that interfaces the ESP32 with the HC-SR04 ultrasonic sensor and connects to the Amazon AWS IoT Core is written in Arduino IDE. The code is divided into two sections. One is the main ino file and other is a header file named Secrets.h.

Remember, in order to connect the ESP32 to the UW MPSK WiFi network, you’ll have to register the device’s MAC address through this UW website.  You’ll want to copy the WiFi password after you register your device. The password will be needed later. Below is the code to find your ESP32’s MAC address:

```bash

#include <WiFi.h>
 
void setup(){
    Serial.begin(115200);  
}
 
void loop(){
  Serial.print("\nESP32 MAC Address: ");
  Serial.println(WiFi.macAddress());
  delay(7500);
}

```

## Main .ino File
Open a new sketch in Arduino IDE & paste the following code and save it.

```bash

/*********
This code uploads distance data collected by an ultrasonic distance sensor to an AWS IoT Core server.

ESP-WROOM-32 Board with Ultrasonic Distance Sensor (HC-SR04)
VCC = 5V
GND = GND
Echo = P18
Trig = P5

Helpful Links
Instructions for AWS - https://how2electronics.com/connecting-esp32-to-amazon-aws-iot-core-using-mqtt/
Additional Instructions for AWS - https://www.hackster.io/magicbit0/connect-esp-32-to-aws-iot-3cf723
Instructions for Ultrasonic Sensor - https://randomnerdtutorials.com/esp32-hc-sr04-ultrasonic-arduino/
Register ESP32 on UW MPSK Network - https://itconnect.uw.edu/tools-services-support/networks-connectivity/uw-networks/campus-wi-fi/uw-mpsk/
AWS IoT Hub: https://us-east-2.console.aws.amazon.com/iot/home?region=us-east-2#/thinghub

*********/


#include "Secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"

#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"  //the resource-id of your AWS IoT policy document
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"  //the resource-id of your AWS IoT policy document

WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

const int trigPin = 5;   //pin P5
const int echoPin = 18;  //pin P18

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;   //The variable that will be uploaded to AWS IoT Core


void connectAWS(){ 
  delay(1000);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 
  Serial.println("Connecting to Wi-Fi");
 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 

  while (!client.connect(THINGNAME)){
      Serial.print(".");
      delay(100);
}
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["distance"] = distanceCm;  //the distance is the message packet sent to the message broker
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);
 
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];
  Serial.println(message);
}

void setup() {
  Serial.begin(115200); // Starts the serial communication
  connectAWS();
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
}

void loop() {
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
  
  publishMessage();
  client.loop();
  delay(1000);
}

```

## Secrets.h header file
Open a new tab in Arduino IDE and name it Secrets.h. Paste the following code to this file. Complete each section with a “TO DO” comment then save the file. 


```bash

/*********
Header file

Instructions for AWS - https://how2electronics.com/connecting-esp32-to-amazon-aws-iot-core-using-mqtt/

*********/

#include <pgmspace.h>
 
#define SECRET
#define THINGNAME "****"                      //TO DO: type your thing name between the quotation marks
 
const char WIFI_SSID[] = "****";              //TO DO: type the WiFi network name (eg. "UW MPSK")
const char WIFI_PASSWORD[] = "****";          //TO DO: type the WiFi password in the quotes
const char AWS_IOT_ENDPOINT[] = "****";       //TO DO: type your AWS IoT endpoint, located on the Settings page of the AWS IoT Console
 
// Amazon Root CA 1                           //TO DO: copy the Amazon Root CA 1 Certificate Key below
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)EOF";
 
// Device Certificate                         //TO DO: copy and paste the Device Certificate Key below
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)KEY";
 
// Device Private Key                         //TO DO: copy and paste the Device Private Key below
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
)KEY";

```

The AWS IoT Endpoint can be found by navigating to Settings within AWS IoT Console (see below).

![Untitled 17](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/e7855205-2cf8-4e43-9387-3a8ba0bdc3bf)

The information for the Amazon Root CA 1 Key, the Device Certificate Key, and the Private Key can all be found in the certificate files that were downloaded earlier. Open each of the three files with a text editor (eg. Notepad, see below), copy the text, then insert the copied text in their appropriate sections of code in Arduino IDE.

![Untitled 18](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/e9b83e21-76e4-4e51-8cdc-07683d79aa12)

## Test if you can Publish Data to AWS IoT Core
Once all the modification is done, connect the ESP32 to your computer and select the ESP32 Board  that you are using for this project (ESP32-WROOM-DA Module). Also, select the COM port. Then click on the upload option to upload the code to the ESP32 board.

Once the code uploading is done, open the Serial Monitor. The ESP32 will try connecting to the WiFi Network. Once it gets connected to the WiFi Network, it will try connecting to the AWS IoT Server.

If the ESP32 is successfully connected to AWS IoT Core, then the distance value will appear on the Serial Monitor every second (see example below). 

![Untitled 19](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/9a802163-6592-4bd0-869c-51e97a44337c)

## Subscribing Sensor Data to AWS IoT Core
The same data should also be posted to the AWS Server. To check if this data is being successfully posted, go to the test section of AWS Dashboard. Under the Test section of the console, click on MQTT test client, then under Subscribe to a topic, enter the Topic filter which you defined in your Arduino code and in the Resources section of the Policy document that you attached to the certificate. To see the data, type “esp32/pub“ under the topic filter section. You may also look at the additional configurations to adjust settings like the number of message packets (i.e. sensor readings) that are stored at any one time on the server, among other settings. Then click on Subscribe.

<img width="403" alt="Untitled 20" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/b5651a30-dc29-4098-8579-baba852398f8">

When you hit the Subscribe button, immediately the data from ESP32 will be uploaded immediately to the AWS IoT Core Console. Thus, you have successfully sent the ultrasonic sensor data to Amazon AWS IoT Core using ESP32.

<img width="214" alt="Untitled 21" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/5fa71126-c8b8-4b81-a00c-2a3f771b7a7a">

## Tasks for you
1. Take a screenshot of your AWS console demonstrating that you have sent distance data from your ultrasonic sensor to the AWS IoT Core server via your ESP32.
2. Select one of your sensors for your final project. In addition, to changing the Arduino code to  send a string with your team number to AWS, you should also send a reading from your sensor. Take a screenshot of your AWS console and include the date and timestamp in the screenshot (see example below).

<img width="299" alt="Untitled 22" src="https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/9577d530-4bc8-491c-b058-9a5701bc114c">


## Additional Resource:
Link to GitHub describing how to submit images from ESP32 to AWS: https://github.com/0015/ThatProject/tree/master/ESP32_MQTT/1_ESP32CAM_AWSMQTT



# (b) Raspberry Pi and Azure Cloud Service
In this experiment, we will stream real time distance data from ultrasonic sensor (HC-SR04) to Microsoft Azure Cloud Service using a Raspberry Pi. 

## Setup
Materials Required

* Jumper cables
* Ultrasonic sensor (HC-SR04) or another sensor of your choice
* Raspberry Pi 4B/5
* Power adapter for Raspberry Pi (27 Watt recommended)
* HDMI cable, microHDMI to HDMI adapter, and monitor
* USB keyboard and mouse
* MicroSD card (16GB or larger recommended), and MicroSD card Adapter


## Pinout Diagram for Raspberry Pi 4B/ 5

![GPIO-Pinout-Diagram](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/02318949-f84a-401c-998b-8b259e62b689)

## Wiring Diagram

![RpiAzure](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ae384b57-15f6-47bd-9ac9-4919f00c657e)

## Prerequisites
We need to create IoT Hub and IoT Hub Device in Azure.

## Creating an IoT Hub

Go to Microsoft Azure official website: https://portal.azure.com/#home and sign in/ sign up to your Azure account.

![Screenshot_2024-04-25_013218](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/7a820528-6a3d-40d0-96a9-c33aaf347816)

Once logged in, type "IoT Hub" in the search bar and select it from the search results.

![Screenshot_2024-04-25_013301](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/9aad07fe-6ef0-4480-9651-2703b04ac6ca)

Click on "Create" to create an IoT hub.
![Screenshot_2024-04-25_014436](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/11de80e3-8cb2-48ac-ac56-4e862c9ffbca)




* Choose your Azure subscription (Free trial/ Azure subscription 1).
* Create a new resource group or select an existing one.
* IoT Hub Name: Enter a unique name for your IoT Hub.
* Choose the region where you want your IoT Hub to be located.
* Select the desired tier and Daily message limit based on your requirements (You can select Free)
* Click on the "Next: Networking>" button

![Screenshot_2024-04-25_015003](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/c9cbcfd0-075f-426c-a54a-ae23a55cfd24)

![Screenshot_2024-04-25_020016](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/845d1a2c-15db-484c-9844-180e69df37d1)

Configure the size and scale settings according to your needs. You can choose the number of partitions, units, and other options. Once done, click on the "Review + create" button.

![Screenshot_2024-04-25_020052](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/0742b42d-df1b-48ae-aa94-636d726bd7a3)


It may take a few minutes for the deployment to complete. Once complete, you will receive a notification of deployment completion. You can then navigate to your IoT Hub from the Azure portal dashboard or by searching for its name.



## Creating an IoT Hub Device

Once you create your IoT Hub, you can now create your IoT Hub Device. 

* In the Azure portal, go to your newly created IoT Hub. You can find it by searching for its name or navigating through the resource groups. The page should look like the following: 

![Screenshot_2024-04-26_005545](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/0f8d78ce-c26d-4eac-907c-53d4624ffd2d)

* Go to “Devices” and click on “Add Device"

![Screenshot_2024-04-26_010206](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/d9a6c93f-512e-4ea8-83db-2ef9d98e57e1)

* In the Device ID box, provide a name for your device and click "Save". I named my device “iotdevice-1”.

![Screenshot_2024-04-26_010817](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/3c772e0e-0693-4a37-973f-f269dc2439e4)


* You will be able to see your newly created IoT Hub Device listed in your IoT Hub. 

![Screenshot_2024-04-26_011921](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/ddb91908-e4e6-4db8-83f7-268551819387)

* Now click on your IoT Hub Device and you will find some useful information about your IoT Hub Device, like Device ID, Primary key, Secondary key, Primary connection string, Secondary connection string, etc. 
* You will need the Primary connection string in the python code of your Raspberry Pi.

## Setting Up your Raspberry Pi


For this lab, you will create a separate folder and set up a virtual environment inside the folder, just like you did in Lab 2. 



## Installing the dependencies

Power up the Raspberry Pi and connect to the WiFi/ internet.
Open the terminal on your Raspberry Pi.


Lets check for updates and upgrades first.

```bash
sudo apt update 
sudo apt upgrade 
```

* Now create a separate directory called “azure_iot” for this project and create a virtual environment.

```bash
mkdir azure_iot
cd azure_iot
python -m venv env
```

This will create a virtual environment in the “azure_iot” directory. You will use this directory to install the dependencies and upload the python codes. To activate your virtual environment, use the following command:

```bash
source env/bin/activate
```
![Screenshot_2024-04-26_021228](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/3c143e05-299c-4a5d-b3ca-464c8fd5e2c5)

The virtual environment has been activated. Now install the two dependencies:

```bash
pip3 install azure-iot-device asyncio
pip install lgpio
```

![Screenshot_2024-04-26_021856](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/91b2b6e6-9935-43d6-8fbf-4e912affdb9a)


## Writing and executing the python script

* Navigate to the “azure_iot” directory from File Manager and create a new file named azure-data-stream.py
![Screenshot_2024-04-26_022502](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/c0c1b05e-fbc3-4e77-ab8b-ea2bb0b5c2ac)
![Screenshot_2024-04-26_022741](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/903a8357-efe2-456b-a330-f10ffdad8b83)
![Screenshot_2024-04-26_022840](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/c903095d-d0d2-4b6e-bcb2-9086b63a044a)


* Double click on the azure-data-stream.py and open it in a text editor. Now copy the python script from here and paste it in the text editor. Make sure to replace the "Primary connection string" in the main() function. Save the script.


* Python Script: azure-data-stream.py

```bash
import asyncio
import time
import lgpio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# Set GPIO pin numbers for ultrasonic sensor
TRIG_PIN = 18
ECHO_PIN = 24

# Initialize the GPIO
gpio = lgpio.gpiochip_open(4)

# Set GPIO pin modes
lgpio.gpio_claim_output(gpio, TRIG_PIN)
lgpio.gpio_claim_input(gpio, ECHO_PIN)

def get_distance():
    # Send a short pulse to trigger the sensor
    lgpio.tx_pulse(gpio, TRIG_PIN, 10, 100)

    # Measure the duration of the pulse from the echo pin
    start = time.time()
    while lgpio.gpio_read(gpio, ECHO_PIN) == 0:
        if time.time() - start > 0.1:
            return None
    pulse_start_time = time.time()

    while lgpio.gpio_read(gpio, ECHO_PIN) == 1:
        if time.time() - start > 0.1:
            return None
    pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    # Calculate distance in centimeters
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

async def send_recurring_telemetry(device_client):
    # Connect the client.
    await device_client.connect()

    # Send recurring telemetry
    while True:
        distance = get_distance()
        if distance is not None:
            # Convert distance to bytes
            data = str(distance).encode('utf-8')
            msg = Message(data)
            print("Sending distance: " + str(distance))
            await device_client.send_message(msg)
        else:
            print("Measurement timeout")
        await asyncio.sleep(1)

def main():
    # Copy and paste your "Primary connection string" below.
    conn_str = "<Primary connection string>"
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    print("IoTHub Device Client Recurring Telemetry Sample")
    print("Press Ctrl+C to exit")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_recurring_telemetry(device_client))
    except KeyboardInterrupt:
        print("User initiated exit")
    except Exception:
        print("Unexpected exception!")
        raise
    finally:
        loop.run_until_complete(device_client.shutdown())
        loop.close()

if __name__ == "__main__":
    main()
```

![Screenshot_2024-04-26_023357](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/d0328c2b-b93a-4f06-b05d-c6e88030f157)


## Installing Azure IoT Explorer

Your sensor data will be streamed in real-time to Azure IoT Explorer. Get back to your Laptop/ PC and download the latest release of Azure IoT Explorer (Version 0.15.8) from the link and install: https://github.com/Azure/azure-iot-explorer/releases

* Log in to your Azure IoT Explorer using your Microsoft account credentials. You will be able to see a list of your subscriptions. If you are a new user, you will see only one subscription. Click on your subscription.


![Screenshot_2024-04-26_013842](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/452a1635-6f9d-44dc-86d9-b56cca350375)

![Screenshot_2024-04-26_014202](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/e7896154-4c8c-48bb-a98c-e27b159ec7bd)

* Click on your IoT Hub and go to your IoI Hub Device.

![Screenshot_2024-04-26_014221](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/cbd15f4b-b018-4a5b-9374-a69feb89fc4e)

![Screenshot_2024-04-26_014634](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/44d14486-3a2c-406a-ac79-f4e14d8b4b66)


* Here, you will find your device identity. Note that you can also copy your connection string from here.
![Screenshot_2024-04-26_014716](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/82c98bde-ceed-4952-95d7-2b880a3523a4)

* Now select the “Telemetry” option from the left bar menu and click “Start”. This will activate your telemetry connection between your Raspberry Pi and Azure.

![Screenshot_2024-04-26_015110](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/f267eab2-4118-4065-a855-4ac2f29cecd9)

* Now go back to your Raspberry Pi and open a new terminal. 
* From the terminal, navigate to the azure_iot directory and activate your virtual environment using:

```bash
cd azure_iot/
source env/bin/activate/
```

* Run the python script by executing the the following command:

```bash
python azure-data-stream.py
```

* You can now measure distances using your ultrasonic sensor. Real-time sensor data processed by the Raspberry Pi are displayed and updated every 1 second in the terminal.

![Screenshot_2024-04-26_025843](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/03c1d6f5-93c6-429d-8f11-9326e78d3c85)

* Go to the Azure IoT Explorer and now you will be able to stream real-time sensor data to Azure. You can login to your Azure IoT Explorer from anywhere in the world and be able to monitor your sensor data in real-time. 

![Screenshot_2024-04-26_015343](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/b3efffff-c8be-4f85-82bd-402e342025a7)

![Screenshot_2024-04-26_015452](https://github.com/mehrab-abrar/Azure-Real-Time-Data-Stream-IoT-Project/assets/42034831/faab07ec-2bad-4b6c-b184-815b89442111)


## Task for you
Take a screenshot of your Azure IoT Explorer Telemetry demonstrating that you have sent distance data from your ultrasonic sensor to the Azure server via your Raspberry Pi. 
Select one of your sensors for your final project. In addition to changing the Raspberry Pi python script to send a string with your team number to Azure, you should also send a reading from your sensor. Take a screenshot of your Azure IoT Explorer Telemetry. 
