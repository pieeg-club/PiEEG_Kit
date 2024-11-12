# PiEEG_Kit
PiEEG_Kit is all in one kit to easily measure and learn bioscience   
Measure EEG, EMG and body and env sensors all in one box  
![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/pieeg_kit_2.png "General View")


Content
- [Application](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#potential-application)
- [Connection](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#connection)
-  [SDK](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#sdk)
-  [Software](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#software)
-  [Pinout between Pi and PiEEG](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#pinout-between-pi-and-pieeg)  
-  [General view of the PiEEG device](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#general-view-of-the-pieeg-device)  
-  [Box Dimension](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#box-dimension)  
-  [Warnings](https://github.com/pieeg-club/PiEEG_Kit?tab=readme-ov-file#warnings)  


## Potential Application   

![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/application.png "Application")

## Connection
![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/connection.jpeg "Connection")
Two power cables one for the RaspberryPi and one for the Screen.   
10 ch for EEG measurements.   
4 ch for EOG, ECG, EMG.  
SPI, GPIO (6 ch), serial, and 3 buttons are available for user applications.   


## SDK 
The SDK is located on GitHub at https://github.com/pieeg-club/PiEEG_Kit/tree/main/SDK. We provide Python scripts for data visualization and data saving.  
These scripts can be easily adapted for users' specific scenarios.  

## Software 

## Signal test
#### Alpha 
<img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/alpha.bmp" alt="alt tag" title="aloha" width="1200">

#### Artefacts (chewing and bkinking)

<img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/artefacts.bmp" alt="alt tag" title="artefacts" width="1200">


#### EMG
![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/EMG.jpeg "emg")

#### EKG
<img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/heart1.bmp" alt="alt tag" title="artefacts" width="1200">



## Pinout between Pi and PiEEG  
Connection beetwen Pi and PiEEG via SPI protocol and Power(5V and GND)  
![alt tag](https://github.com/pieeg-club/PiEEG/blob/main/images/pins2.bmp "spi")


#### General view of the PiEEG device  
PiEEG is one of the main component of the Kit responsible for converts analog signals to digital signals via 24 bit resolution analog-digital converter ADS1299 from TI   
![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/pieeg.jpg "PiEEG")

#### Box Dimension
Box is primarily made of ABS plastic. This material is noted for its durability and strength, making it suitable for protecting the contents during shipping and use. The overall design aims to be robust enough to withstand rough handling, ensuring that the device remains safe inside the packaging. The development board is made of hasl lead free FR-4. 
![alt tag](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/pieeg_size.jpg "Size")

#### Citing 
In Progress 

## Warnings
>[!WARNING]
> PiEEG kit (PiEEG) is not a medical device. You are fully responsible for your personal decision to purchase this device and, ultimately, for its safe use. PiEEG is not a medical device and has not been certified by any government regulatory agency for use with the human body. Use it at your own risk.  

>[!CAUTION]
> The device must operate only from a battery - 5 V. Complete isolation from the mains power is required.! The device MUST not be connected to any kind of mains power, via USB or otherwise.   
> Power supply - only battery 5V, please read the [liability](https://pieeg.com/liability/)


