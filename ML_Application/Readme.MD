# How to Use Machine Learning to Stress Control via EEG 
Full story can be found via the next [link](https://pieeg.com/news/instruction-how-to-use-machine-learning-to-stress-or-emoinal-control-via-eeg/)    

If you want to create an EEG-based classifier for machine learning, here’s a short guide:

#### 1. Collect EEG Datasets:

Use Script [1.Save_Data.py](https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/Collected_dataset.jpg)  to collect raw EEG data with PiEEG

Data has the next Format in the Excel File (example of dataset)

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG-16/blob/main/images/Collected_dataset.jpg" alt="generals view">
</p>

You need (as an example) to gather 50 datasets (1 minute or more each) for stress and 50 datasets (1 minute or more each) for no-stress conditions.  

#### 2. Compute Power in Key Frequency Bands:

Using raw EEG data alone for machine learning to detect stress is not ideal. Instead, it’s more effective to analyze the alpha power, as it provides better insights into stress levels. We need convert our dataset from raw EEG to Power via the next script [2.Convert_to_Power_Alpha.py](https://github.com/pieeg-club/PiEEG_Kit/blob/main/ML_Application/2.Convert_to_Power_Alpha.py) 
Of course, we should ensure that our data don’t contain very strong noise artefacts that should be removed from data.

As result, you receive 
<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/alpha.png" alt="generals view">
</p>


#### 3. Prepare the Data for ML
Combine the 50 datasets for stress and not stress  into  two separate Excel files for stress and not stress. But the most important moment here is that you should add an additional column that will indicate the record number (entry number or subject number).  
It should look like that 

<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/dataset_ML.jpg" alt="generals view">
</p>


#### 4. Train the Classifier:

Use the ML script [3.ML.py](https://github.com/pieeg-club/PiEEG_Kit/blob/main/ML_Application/3.ML.py) to train a model and classify stress levels based on EEG data.

As result, you receive 
<p align="center">
  <img src="https://github.com/pieeg-club/PiEEG_Kit/blob/main/images/python_ML.jpg" alt="generals view">
</p>

🚀 Enjoy building your classifier!








