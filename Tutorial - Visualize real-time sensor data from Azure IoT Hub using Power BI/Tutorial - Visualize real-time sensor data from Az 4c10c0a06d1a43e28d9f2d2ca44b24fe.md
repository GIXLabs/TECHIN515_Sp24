# Tutorial - Visualize real-time sensor data from Azure IoT Hub using Power BI

Additional Microsoft resource: [Tutorial - IoT data visualization with Power BI - Azure IoT Hub | Microsoft Learn](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-power-bi)

## Prerequisites

In order to complete this exercise, you must first stream sensor data to Azure IoT Hub.  To stream ultrasonic sensor data to Azure IoT Hub from an ESP32 follow this [tutorial](https://github.com/GIXLabs/TECHIN515_Sp24/tree/main/Tutorial%20-%20ESP32%20and%20Azure%20IoT%20Hub).  To stream ultrasonic sensor data to Azure IoT Hub from a Raspberry Pi follow this [lab](https://github.com/GIXLabs/TECHIN515_Sp24/tree/main/Lab3_CloudIntro). 

## Overview

At the end of this tutorial, you’ll be able to generate a web URL to a visualization of your sensor data as well as generate html code for a graphic which you can paste into your own web application. 

You can use Microsoft Power BI to visualize real-time sensor data that your Azure IoT hub receives. To do so, configure an Azure Stream Analytics job to consume the data from IoT Hub and route it to a dataset in Power BI.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled.png)

[Microsoft Power BI](https://powerbi.microsoft.com/) is a data visualization tool developed by Microsoft. [Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/#overview) is a real-time analytics service designed to help you analyze and process streams of data that can be used to get insights, build reports or trigger alerts and actions.

## A. Create a Power BI Workspace

Navigate to [app.powerbi.com](http://app.powerbi.com), click on Workspaces then create a new workspace.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%201.png)

Give your workspace a name (eg. “TECHIN515”) and a description. We can keep the Pro license at the moment. Then click apply.  A new workspace has been created. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%202.png)

After creating your workspace, click on the *Workspaces* icon on the left side menu bar, then click on the workspace you just created. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%203.png)

Now view the URL of the workspace. See screenshot below. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%204.png)

The string of characters in the URL between groups/ and /list is your workspace’s GUID, or Global Unique IDentifier. In this example, the GUID of the workspace is “c190cffc-38c9-484e-adeb-f02c3a32bfda”. Copy this GUID, you will need it in one of the next steps.  

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%205.png)

## **B. Create a new consumer group in your IoT hub**

First, navigate to your IoT Hub in your [Azure portal](https://portal.azure.com/) and create a consumer group. In this example, the consumer group has been named, “newconsumergroup”. This consumer group will be called by your Azure Stream Analytics Service. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%206.png)

## **B. Create a new Stream Analytics job**

Next, we need to Create, configure, and run a Stream Analytics job. Azure Stream Analytics will serve as waypoint to process the data from your IoT Hub and send it to Power Bi, where your data can be visualized. To create a new job, go to the [Azure portal](https://portal.azure.com/) and select **Create a resource**. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%207.png)

Type *Stream Analytics Job* in the search box and select it from the drop-down list. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%208.png)

On the **Stream Analytics job** overview page, select **Create**

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%209.png)

In the **Basics** tab of the **New Stream Analytics job** page, enter the following information:

| Parameter | Value |
| --- | --- |
| Subscription | Select the subscription that contains your IoT hub. |
| Resource group | Select the resource group that contains your IoT hub. |
| Name | Enter the name of the job. The name must be globally unique. |
| Region | Select the region where your IoT hub is located. |

You can change the streaming unit details to the value ‘1’ so that you don’t rapidly use up your Azure credits. Leave all other fields at their defaults.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2010.png)

Select **Review + create**, then select **Create** to create the Stream Analytics job. It may take a couple minutes to deploy the new job. 

Once the job is created, select **Go to resource**.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2011.png)

## **C. Add an input to the Stream Analytics job**

The input for your Stream Analytics job will be the data sent to the Azure IoT Hub. The output of this job will be to Power BI, the tool developed by Microsoft to visualize data. You will setup the ouput in the next stem. 

Configure the Stream Analytics job to collect data from your IoT hub.

1. Open the Stream Analytics job.
2. Select **Inputs** from the **Job topology** section of the navigation menu.
3. Select **Add input**, then select **IoT Hub** from the drop-down list.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2012.png)

1. On the new input pane, enter the following information:

| Parameter | Value |
| --- | --- |
| Input alias | Enter a unique alias for the input. For example, PowerBIVisualizationInput. |
| Subscription | Select the Azure subscription you're using for this tutorial. |
| IoT Hub | Select the IoT hub you're using for this tutorial. |
| Consumer group | Select the consumer group you created previously. |
| Shared access policy name | Select the name of the shared access policy you want the Stream Analytics job to use for your IoT hub. For this tutorial, you can select service. The service policy is created by default on new IoT hubs and grants permission to send and receive on cloud-side endpoints exposed by the IoT hub. To learn more, see https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-dev-guide-sas#access-control-and-permissions. |
| Shared access policy key | This field is automatically filled, based on your selection for the shared access policy name. |
| Endpoint | Select Messaging. |

Leave all other fields at their defaults.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2013.png)

1. Select **Save**.

## **D. Add an output to the Stream Analytics job**

1. Select **Outputs** from the **Job simulation** section of the navigation menu.
2. Select **Add output**, and then select **Power BI** from the drop-down list.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2014.png)

1. After you've signed in to Power BI, enter the following information to create a Power BI output. Your Group workspace is the Global Unique IDentifier (GUID) that is affiliated with your Power BI workspace (see previous step). 

| Parameter | Value |
| --- | --- |
| Output alias | A unique alias for the output. For example, PowerBIVisualizationOutput. |
| Group workspace | Select your target group workspace. |
| Authentication mode | The portal warns you if you don't have the correct permissions to use managed identities for authentication. If that's the case, select User token instead. |
| Dataset name | Enter a dataset name. |
| Table name | Enter a table name. |

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2015.png)

1. Select **Authorize** and sign in to your Power BI account.
2. Select **Save**.

You have now created an output to your analytics service (Azure Stream Analytics). 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2016.png)

## E. **Configure the query of the Stream Analytics job**

Next, we’ll return to our Azure Portal. Our goal in this step is to select which data from our sensor we would like to send through the Stream Analytics job to visualize through Power BI. On your Azure Portal, click on the new Stream Analytics job you created (”PowerBiVisualizationJob”).

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2017.png)

1. Select **Query** from the **Job topology** section of the navigation menu or in the **Properties** section.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2018.png)

1. In the query editor, replace `[YourOutputAlias]` with the output alias of the job. In this example, we named our OutputAlias “PowerBIVisualizationOutput”. See step D above.
2. Replace `[YourInputAlias]` with the input alias of the job. In this example, we named our OutputAlias “PowerBIVisualizationInput”. See step C above.
3. Add the following `WHERE` clause as the last line of the query. This line ensures that only messages with a **distance** property will be forwarded to Power BI. You can also add other filters to your SQL query in order to filter out errant sensor readings (eg. unreasonably high or low readings). 

```sql
SELECT
    *
INTO
    PowerBIVisualizationOutput
FROM
    PowerBIVisualizationInput

WHERE distance IS NOT NULL
AND distance < 100
AND distance > 1
```

The value “distance” is defined in the generateTelemetryPayload() function in your Arduino code (see below). 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/1d19ee53-8f3e-4d07-bc19-939d72873898.png)

The “distance” value is also represented in your Azure IoT Explorer (see below):

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2019.png)

1. Your query should look similar to the following screenshot. Select **Save query**.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/e7780da7-9bba-4c31-acb8-e3309ad5073a.png)

## **F. Run the Stream Analytics job**

After setting up the Stream Analytics query, you can start the Stream Analytics job by following the two steps below.

1. In the Stream Analytics job, select **Overview**.
2. Select **Start Job** > **Now** > **Start**. Once the job successfully starts, the job status changes from **Created** to **Starting** to **Running** (after a minute or two).

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2020.png)

## **G. Create and publish a Power BI report to visualize the data**

The following steps show you how to create and publish a report using the Power BI service.

1. Make sure that your IoT device is running and sending distance data to IoT hub. You can verify that your device is sending data by viewing it through Azure IoT Explorer.
2. Sign in to your [Power BI](https://powerbi.microsoft.com/) account.
3. Select **Workspaces** from the side menu, then select the group workspace you chose in the Stream Analytics job output. In this example, the Workspace is “TECHIN515”.
4. On your workspace view, you should see the dataset that you specified when you created the output for the Stream Analytics job.
5. Hover over the dataset you created, select **More options** menu (the three dots to the right of the dataset name), and then select **Create report**. Every time you create a report, data from your sensor will begin to be stored permanently in Power BI for historic analysis. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2021.png)

1. Create a line chart to show real-time temperature over time.
    1. On the **Visualizations** pane of the report creation page, select the line chart icon to add a line chart. Use the guides located on the sides and corners of the chart to adjust its size and position.
    2. On the **Fields** pane, expand the table that you specified when you created the output for the Stream Analytics job.
    3. Drag **EventEnqueuedUtcTime** to **X Axis** on the **Visualizations** pane.
    4. Drag **distance** to **Y Axis**.
        
        A line chart is created. The x-axis displays date and time in the UTC time zone. The y-axis displays temperature from the sensor. You can refresh the chart by click the circular arrow button in the top right panel. 
        

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2022.png)

1. Select **File** > **Save** to save the report. When prompted, enter a name for your report. 
2. Still on the report pane, select **File** > **Embed report** > **Website or portal**.

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2023.png)

1. You're provided the report link that you can share with anyone for report access and a code snippet that you can use to integrate the report into a blog or website. Copy the link in the **Secure embed code** window and then close the window. You can also copy and paste the HTML code into a website. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2024.png)

1. Open a web browser and paste the link into the address bar to view your report in the browser.

For additional resources on how to visualize streaming data, visit this [website](https://learn.microsoft.com/en-us/power-bi/connect-data/service-real-time-streaming).

## G. Stopping the Stream Analytics Job

When you are done with the exercise, it’s good practice to stop the Stream Analytics job (PowerBiVisualizationJob) so that you don’t use your Azure credits. To stop the job, navigate to the [home page](https://portal.azure.com/) of your Azure portal, then  and click on Stop job. When the job has ended, you won’t be charged any further credits for this exercise. 

![Untitled](Tutorial%20-%20Visualize%20real-time%20sensor%20data%20from%20Az%204c10c0a06d1a43e28d9f2d2ca44b24fe/Untitled%2025.png)