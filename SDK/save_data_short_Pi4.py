import pandas as pd
import spidev
import time
from RPi import GPIO
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy import signal
from time import sleep

# GPIO config in RPi
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)

# SPI connections beetwen ADS1299 and RPi
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=600000
spi.lsbfirst=False
spi.mode=0b01
spi.bits_per_word = 8

# Registers from ADS1299 
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

# Functions for communication beetwen RPi and ADS1299

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 
def send_command(command):
 send_data = [command]
 com_reg=spi.xfer(send_data)
 
def write_byte(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 spi.xfer(data)

# Send command to ADS1299 
send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

# Regsiters to ADS1299 
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

result=[0]*27
data_1ch_test = []
data_2ch_test = []
data_3ch_test = []
data_4ch_test = []
data_5ch_test = []
data_6ch_test = []
data_7ch_test = []
data_8ch_test = []

 
test_DRDY = 5 

while 1:

        GPIO.wait_for_edge(37, GPIO.FALLING)
        output=spi.readbytes(27) # read 27 bytes, firts 3 bytes it is status, after 24 bytes for 8 ch, evbery ch is 3 bytes 
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
        data_2ch_test.append(result[2])
        data_3ch_test.append(result[3])
        data_4ch_test.append(result[4])
        data_5ch_test.append(result[5])
        data_6ch_test.append(result[6])
        data_7ch_test.append(result[7])
        data_8ch_test.append(result[8])
        

        if len(data_1ch_test)==10000:  # set necessery kenght 250 it is 1 sec          
            data_dict = {
                'data_1ch_test': data_1ch_test,
                'data_2ch_test': data_2ch_test,
                'data_3ch_test': data_3ch_test,
                'data_4ch_test': data_4ch_test,
                'data_5ch_test': data_5ch_test,
                'data_6ch_test': data_6ch_test,
                'data_7ch_test': data_7ch_test,
                'data_8ch_test': data_8ch_test
                        }

            df = pd.DataFrame(data_dict)
            df.to_excel("output3.xlsx", index=False)
            print (df)
spi.close()
