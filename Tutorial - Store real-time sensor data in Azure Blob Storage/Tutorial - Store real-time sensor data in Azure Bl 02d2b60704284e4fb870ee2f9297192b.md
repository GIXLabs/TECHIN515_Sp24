# Tutorial - Store real-time sensor data in Azure Blob Storage

Created by: Padraic
Created time: May 3, 2024 11:25 AM

Resources: Azure IoT Hub

---

## Additional Learning Resources

Microsoft Learning Resources: [Azure IoT documentation - Azure IoT | Microsoft Learn](https://learn.microsoft.com/en-us/azure/iot/)

YouTube guide: [Getting Started with Microsoft Azure IoT Central using NodeMCU ESP8266 (youtube.com)](https://www.youtube.com/watch?v=jmMWel9Y3Qg)

## Prerequisites

In order to complete this exercise, you must first stream sensor data to Azure IoT Hub.  To stream ultrasonic sensor data to Azure IoT Hub from an ESP32 follow this [tutorial](https://github.com/GIXLabs/TECHIN515_Sp24/tree/main/Tutorial%20-%20ESP32%20and%20Azure%20IoT%20Hub).  To stream ultrasonic sensor data to Azure IoT Hub from a Raspberry Pi follow this [lab](https://github.com/GIXLabs/TECHIN515_Sp24/tree/main/Lab3_CloudIntro). 

## Overview

In this tutorial, you will learn how to send data from Azure IoT Hub to Azure Blob Storage. 

[Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) is a service provided by Microsoft to store unstructured data. Unstructured data is a type of data that is not structured; that is, it does not yet exist in database environment combrised of rows in a table, for example.  Users or client applications can access objects in Blob Storage via HTTP/HTTPS, from anywhere in the world. Objects in Blob Storage are accessible via the [Azure Storage REST API](https://learn.microsoft.com/en-us/rest/api/storageservices/blob-service-rest-api), [Azure PowerShell](https://learn.microsoft.com/en-us/powershell/module/az.storage), [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/storage), or an Azure Storage client library. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled.png)

Blob Storage offers three types of resources:

- The **storage account**
- A **container** in the storage account
- A **blob** in a container

The following diagram shows the relationship between these resources ([image source](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)).

![https://learn.microsoft.com/en-us/azure/storage/blobs/media/storage-blobs-introduction/blob1.png](https://learn.microsoft.com/en-us/azure/storage/blobs/media/storage-blobs-introduction/blob1.png)

[Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/#overview) is a fully managed, real-time analytics service designed to help you analyze and process fast moving streams of data that can be used to get insights, build reports or trigger alerts and actions. In order to send your sensor data to Azure Blob Storage, you’ll first need to Create a new Stream Analytics job. 

## **A. Create a new consumer group in your IoT hub**

First, navigate to your IoT Hub in your [Azure portal](https://portal.azure.com/), select Built-in Endpoints, and then create a consumer group. In this example, the consumer group has been named, “consumergroup_1”. This consumer group will be called by your Azure Stream Analytics Service. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%201.png)

## **B. Create a Blob Storage Account**

In your Azure portal, navigate to the search feature and search for “storage account.” Select the Service entitled, “Storage accounts.”

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%202.png)

Then Create a new Storage Account. Give the storage account a name, and then make a redundancy selection with the least amount of cost (locally-redundant storage), and then select *Review + Create*. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%203.png)

The Blob Storage service will take a minute before it is deployed. You can go to the resource to review the parameters of the storage account and [upgrade](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to?tabs=azure-portal) the account to an [Azure Data Lake Storage (ADLS) Gen 2](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to?tabs=azure-portal) account, for example. ADLS is a storage service with improved functionality compared to Blob Strorage. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%204.png)

Once you’ve created the Blob Storage Account, then you can select **Containers** under **Data Storage** and then create a new container. You may name this new container anything you like. This container is where your sensor data will be stored. In this example, the name of the container is “distance-container”.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%205.png)

## **C. Create a new Stream Analytics job**

Next, we need to Create, configure, and run a Stream Analytics job. Azure Stream Analytics will serve as waypoint to process the data from your IoT Hub and send it to Azure Blob Storage, where your data will be stored. To create a new job, go to the [Azure portal](https://portal.azure.com/) and select **Create a resource**. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%206.png)

Type *Stream Analytics Job* in the search box and select it from the drop-down list. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%207.png)

On the **Stream Analytics job** overview page, select **Create**

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%208.png)

In the **Basics** tab of the **New Stream Analytics job** page, enter the following information:

| Parameter | Value |
| --- | --- |
| Subscription | Select the subscription that contains your IoT hub. |
| Resource group | Select the resource group that contains your IoT hub. |
| Name | Enter the name of the job. The name must be globally unique. |
| Region | Select the region where your IoT hub is located. |

You can change the number of streaming unit details to ‘1’. The name of this Stream Analytics Job has been set to “AzureBlobStorageJob”.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%209.png)

Next, click Add storage account, then select the storage account that you ust created. In this example, the name of the storage account is “ultrasonicdata1”. Select Next.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2010.png)

Proceed to **Review + create**, then select **Create** to create the Stream Analytics job. It may take a couple minutes to deploy the new job. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2011.png)

Once the job is created, select **Go to resource**.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2012.png)

## **C. Add an input to the Stream Analytics job**

The input for your Stream Analytics job will be the data sent to the Azure IoT Hub. The output of this job will be Azure Blob Storage, the tool developed by Microsoft to store data. You will setup the ouput in the next step. 

Configure the Stream Analytics job to collect data from your IoT hub.

1. Open the Stream Analytics job.
2. Select **Inputs** from the **Job topology** section of the navigation menu.
3. Select **Add input**, then select **IoT Hub** from the drop-down list.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2013.png)

When the input pops up on the right hand side of the screen, many of the fields will autopopulate, but you can rename your Input alias if you would like. For this lab, the Input alias has been defined as “ultrasonicdata-input”. The consumer group that you just created is “consumergroup_1”. Press Save.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2014.png)

## **D. Add an output to the Stream Analytics job**

1. Select **Outputs** from the **Job simulation** section of the navigation menu.
2. Select **Add output**, and then select **Blob Storage/ADLS Gen2** from the drop-down list.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2015.png)

1. Create a new Output Alias name. In this example, the name is ultrasonicdata-output. Select the Blob Storage Account you created earlier (ultrasonicdata1) and the Container that you created (distance-container). You can also create a new container. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2016.png)

Scroll down to select the minimum number of rows that you would like aggregated as a batch before they are appended to your Blob Storage. You can also select the maximum amount of time before batches are appended. In this example, the minimum rows is 20 and the maximum time is 2 minutes. Press Save.

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2017.png)

You can then modify what type of sensor data gets stored in your Blob Storage. Sometimes sensors are a bit erratic and return unreliable values which are unreasonably high or unreasonably low. You can filter out these values in the **Query** section of the Stream Analytics job. To do so, select **Query**, then edit the SQL script to your liking. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2018.png)

Here is a [SQL Basics Cheat Sheet](https://www.datacamp.com/cheat-sheet/sql-basics-cheat-sheet) so that you can further manipulate your data. 

```sql
/*
Here are links to help you get started with Stream Analytics Query Language:
Common query patterns - https://go.microsoft.com/fwLink/?LinkID=619153
Query language - https://docs.microsoft.com/stream-analytics-query/query-language-elements-azure-stream-analytics
*/
SELECT
    *
INTO
    [ultrasonicdata-output]
FROM
    [ultrasonicdata-input]
WHERE distance < 100
AND distance > 1
```

In the example above, only data with a distance value of greater than 1 and less than 100 will be stored in the Blob Storage container.  If you have followed the previous tutorial on streaming ultrasonic sensor data from an ESP32 to Azure IoT Hub, then the value 'distance' is sent as a message in the generateTelemetryPayload() function in your Arduino code. 

Next, start the Stream Analytics job that you just created by returning to the Overview pafe and pressing **Start job**. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2019.png)

## E. Verify that your sensor data is being stored in your Blob Storage Container

In order to very that your sensor data is being stored in your Blob Storage container, return to your Azure Home portal. From your home portal, click on the Storage Account that you created for this exercise (eg. ultrasonicdata1). Next click on **Containers** and then the container you created for this exercise (eg. distance-container). 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2020.png)

Next click on the JSON file. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2021.png)

Then click on the **Edit** tab to view your data. You can press the refresh button to see when new entries are appended to your JSON file. You will also notice how none of the distance entries that are saved in the JSON file are above 100 or below 1. A URL link to the JSON file can be found in the **Overview** tab. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2022.png)

## F. Stopping the Stream Analytics Job

At the end of the exercise, return to your Stream Analytics job (eg. AzureBlobStorageJob) from the home page of your Azure portal and click on Stop job. When the job has ended, you won’t be charged any further credits for this exercise. 

![Untitled](Tutorial%20-%20Store%20real-time%20sensor%20data%20in%20Azure%20Bl%2002d2b60704284e4fb870ee2f9297192b/Untitled%2023.png)