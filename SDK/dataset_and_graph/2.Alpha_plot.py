import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import pywt

# Load the Excel file into a DataFrame
df = pd.read_excel("output3.xlsx")

# Assuming you want to visualize data from columns data_1ch_test to data_8ch_test
columns_to_visualize = ['data_1ch_test', 'data_2ch_test', 'data_3ch_test', 'data_4ch_test', 'data_5ch_test', 'data_6ch_test', 'data_7ch_test', 'data_8ch_test']

# Plotting each column separately
for column in columns_to_visualize:
    plt.plot(df[column], label=column)

plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Data Visualization')
plt.legend()
plt.show()

fps = fs = 250
highcut = 8
lowcut = 12

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

data_filt_numpy_high_1 = butter_highpass_filter(df['data_1ch_test'], highcut, fps)
data_for_graph_1 = butter_lowpass_filter(data_filt_numpy_high_1, lowcut, fps)

data_filt_numpy_high_2 = butter_highpass_filter(df['data_2ch_test'], highcut, fps)
data_for_graph_2 = butter_lowpass_filter(data_filt_numpy_high_2, lowcut, fps)

data_filt_numpy_high_3 = butter_highpass_filter(df['data_3ch_test'], highcut, fps)
data_for_graph_3 = butter_lowpass_filter(data_filt_numpy_high_3, lowcut, fps)

data_filt_numpy_high_4 = butter_highpass_filter(df['data_4ch_test'], highcut, fps)
data_for_graph_4 = butter_lowpass_filter(data_filt_numpy_high_4, lowcut, fps)

data_filt_numpy_high_5 = butter_highpass_filter(df['data_5ch_test'], highcut, fps)
data_for_graph_5 = butter_lowpass_filter(data_filt_numpy_high_5, lowcut, fps)

data_filt_numpy_high_6 = butter_highpass_filter(df['data_6ch_test'], highcut, fps)
data_for_graph_6 = butter_lowpass_filter(data_filt_numpy_high_6, lowcut, fps)

data_filt_numpy_high_7 = butter_highpass_filter(df['data_7ch_test'], highcut, fps)
data_for_graph_7 = butter_lowpass_filter(data_filt_numpy_high_7, lowcut, fps)

data_filt_numpy_high_8 = butter_highpass_filter(df['data_8ch_test'], highcut, fps)
data_for_graph_8 = butter_lowpass_filter(data_filt_numpy_high_8, lowcut, fps)

plt.plot(data_for_graph_1)
plt.show()


def wavelet(eeg_signal):
    fs = 250
    wavelet = 'cmor'  # Complex Morlet wavelet
    scales = np.arange(1, 64)  #  128 Scale range
    coefficients, frequencies = pywt.cwt(eeg_signal, scales, wavelet, sampling_period=1/fs)
    return coefficients, frequencies

channels = ["Ch 1", "Ch 2", "Ch 3", "Ch 4", "Ch 5", "Ch 6", "Ch 7", "Ch 8"]
data_for_graph = [data_for_graph_1, data_for_graph_2, data_for_graph_3, data_for_graph_4,
                  data_for_graph_5, data_for_graph_6, data_for_graph_7, data_for_graph_8]

plt.figure(figsize=(12, 16))
for i, (channel, data) in enumerate(zip(channels, data_for_graph), 1):
    plt.subplot(8, 2, i * 2 - 1)
    plt.plot(data)
    plt.title('Original EEG Signal ' + channel)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Plot the wavelet transform
    plt.subplot(8, 2, i * 2)
    coefficients, frequencies = wavelet(data)
    plt.imshow(np.abs(coefficients), aspect='auto', extent=[0, len(data)/fs, 1, 64], cmap='jet')
    plt.title('Wavelet Transform ' + channel)
    plt.xlabel('Time (s)')
    plt.ylabel('Scale')
    plt.colorbar()

plt.tight_layout()
plt.show()
