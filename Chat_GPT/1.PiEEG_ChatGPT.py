import spidev
import time
from RPi import GPIO
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal
import gpiod
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal
#from scipy.integrate import simps #for another version of python IDLE
from scipy.integrate import simpson as simps
import openai

openai.api_key = 'put here you key'

# GPIO setup GPIO inputs 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)

button_pin = 26
#chip = gpiod.Chip("gpiochip4")  #for gpiod version 1.6.3
chip = gpiod.chip("/dev/gpiochip4")
line = chip.get_line(button_pin)
#button_line.request(consumer = "Button", type = gpiod.DIRECTION_INPUT) #for gpiod version 1.6.3

# Create a request configuration for ADS1299 ready signal
button_line = gpiod.line_request()
button_line.consumer = "Button"
button_line.request_type = gpiod.line_request.DIRECTION_INPUT
line.request(button_line)

#  setup SPI protocol
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=600000
spi.lsbfirst=False
spi.mode=0b01
spi.bits_per_word = 8

# Registers for ADS1299 
who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def send_to_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 5,
        temperature=0  # Set temperature to 0 for deterministic responses
    )
    #print (response)
    return response.choices[0].message['content']
        
def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 print ("data", read_reg)
 
def send_command(command):
 send_data = [command]
 com_reg=spi.xfer(send_data)
 
def write_byte(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)

# command to ADS1299
send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

# write registers to ADS1299
write_byte (0x14, 0x80) #GPIO
write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xFF)
write_byte (0x04, 0x00)
write_byte (0x0D, 0x00)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)
send_command (rdatac)
send_command (start)
DRDY=1

# set up  8 ch for read data 
result=[0]*27
data_1ch_test = []

# Set up Graph
axis_x=0
y_minus_graph=250
y_plus_graph=250
x_minux_graph=5000
x_plus_graph=250
sample_len = 250
fig, ax = plt.subplots()  # Single subplot
#ax.set_xlabel('Time')
#fig, axis = plt.subplots(1, 1, figsize=(5, 5))
plt.subplots_adjust(hspace=1)
ch_name = 0
ch_name_title = [1]

ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Data after pass filter Ch1')
 
    
test_DRDY = 5 ## ready singla from ADS1299
data_power = []

#1.2 Band-pass filter
data_before = []
data_after =  []
just_one_time = 0


sample_len = 250
sample_lens = 250
#for band-pass filter
fps = 250
highcut = 1
lowcut = 10
data_before_1 = [0]*250

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

while 1:
    button_state = line.get_value()
    if button_state == 1:
        test_DRDY = 10
    if test_DRDY == 10 and button_state == 0:
        test_DRDY = 0 

        output=spi.readbytes(27)
        for a in range (3,25,3):
            voltage_1=(output[a]<<8)| output[a+1]
            voltage_1=(voltage_1<<8)| output[a+2]
            convert_voktage=voltage_1|data_test
            if convert_voktage==data_check:
                voltage_1_after_convert=(voltage_1-16777214)
            else:
               voltage_1_after_convert=voltage_1
            channel_num =  (a/3)

            result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

        data_1ch_test.append(result[1])

        
        if len(data_1ch_test)==sample_len:
            # 1
            data_after_1 = data_1ch_test        
            dataset_1 =  data_before_1 + data_after_1
            data_before_1 = dataset_1[250:]
            data_for_graph_1 = dataset_1

            data_filt_numpy_high_1 = butter_highpass_filter(data_for_graph_1, highcut, fps)
            data_for_graph_1 = butter_lowpass_filter(data_filt_numpy_high_1, lowcut, fps)

            ax.plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_1[250:], color = '#0a0b0c')  
            ax.axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_1[50]-y_minus_graph, data_for_graph_1[150]+y_plus_graph])

            plt.pause(0.000001)
            
            axis_x=axis_x+sample_lens 
            data_1ch_test = []                             

            data_short = data_for_graph_1 #data[1000:8000]

            #sns.set(font_scale=1.2)

            # Define sampling frequency and time vector
            # convert samples to time
            # Define window length 1 sec
            win = 250
            sf = 250
            freqs, psd = signal.welch(data_short, sf, nperseg=win)

            # Plot the power spectrum
            sns.set(font_scale=1.2, style='white')

            # Define delta lower and upper limits
            low, high = 8, 13  # Delta Waves: Up to 4 Hz
                               # Alpha Waves: 8 - 13 Hz
                               # Theta Waves: 4-7 Hz
                               # Gamma Waves: 30-100 Hz

            # Find intersecting values in frequency vector
            idx_delta = np.logical_and(freqs >= low, freqs <= high)

            # Plot the power spectral density and fill the delta area
            
            """
            here you make visualisation for power calculation
            """
            #plt.figure(figsize=(7, 4))
            #plt.plot(freqs, psd, lw=2, color='k')

            #plt.fill_between(freqs, psd, where=idx_delta, color='green')
            #plt.xlabel('Frequency (Hz)')
            #plt.ylabel('Power spectral density (uV^2 / Hz)')
            #plt.xlim([0, 20])
            #plt.ylim([0, psd.max() * 1.1])
            #plt.title("Welch's periodogram")
            #plt.show()


            # Frequency resolution
            freq_res = freqs[1] - freqs[0]  

            # Compute the absolute power by approximating the area under the curve
            delta_power = simps(psd[idx_delta], dx=freq_res)
            #print('Absolute delta power: %.3f uV^2' % delta_power)
            data_power.append(delta_power)
            if len(data_power) == 10:
                data_power_str  = ', '.join(str(x) for x in data_power)

                prompt = "Based on the power in alpha rhythm for one EEG channel with fps 250 = [" + data_power_str + ", please evaluate my stress level and respond with only one of the following words: [calm, neutral, stress]"
                
                response = send_to_chatgpt(prompt)
                print(response)
                data_power = []

spi.close()
