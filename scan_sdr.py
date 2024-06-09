#!/usr/bin/python3

from rtlsdr import RtlSdr
from pylab import *
import sys
import queue
import statistics

global q
q = queue.Queue()

def read_callback(data, context):
    try:
        output = []
        psd_vals, freqs = psd(data, NFFT=16384, Fs=context.sample_rate/1e6, Fc=context.center_freq/1e6)
        # print frequencies and powers to terminal
        for freq, psd_val in zip(freqs, psd_vals):
            power_db = 10*np.log10(psd_val)
            output.append([format(freq, ".4f"), round(power_db, 2)])
            
        q.put(output)
        context.cancel_read_async()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()

def get_freq_dict(sdr, freq_list):
    freq_dict = {}
    for frequency in freq_list:
        formatted_current_freq = str(format(frequency / 1e6, ".4f"))
        freq_dict[formatted_current_freq] = {}
        freq_dict[formatted_current_freq]['noise_floors'] = []
    for i in range(0, 3):
        for frequency in freq_list:
            sdr.center_freq = frequency - 350000
            formatted_current_freq = format(frequency / 1e6, ".4f")
            sdr.read_samples_async(read_callback, num_samples=32768)
            sdr_output = q.get()
            for j in range(0, len(sdr_output)):
                if sdr_output[j][0] == formatted_current_freq:
                    freq_dict[str(formatted_current_freq)]['noise_floors'].append(sdr_output[j][1])

    for key in freq_dict.keys():
        avg = statistics.mean(freq_dict[key]['noise_floors'])
        freq_dict[key]['detection_threshold'] = avg + 15

    return freq_dict


def main():
    sdr = RtlSdr()
    # configure device
    sdr.sample_rate = 1800000  # Hz
    sdr.freq_correction = 1   # PPM
    sdr.gain = 4
    freq_list = [462562500, 462587500, 462612500, 462637500, 462662500, 462687500, 462712500, 467562500, 467587500, 467612500, 467637500, 467662500, 467687500, 467712500, 462550000, 462575000, 462600000, 462625000, 462650000, 462675000, 462700000, 462725000]

    freq_dict = get_freq_dict(sdr, freq_list)
    try:
        while True:    
            for frequency in freq_list:
                sdr.center_freq = frequency - 350000
                formatted_current_freq = format(frequency / 1e6, ".4f")
                sdr.read_samples_async(read_callback, num_samples=32768)
                sdr_output = q.get()
                for i in range(0, len(sdr_output)):
                    if sdr_output[i][0] == formatted_current_freq:
                        if sdr_output[i][1] > freq_dict[str(sdr_output[i][0])]['detection_threshold']:
                            print(f"Activity on {sdr_output[i][0]}")
    except KeyboardInterrupt:
        print("Exiting.....")
        exit()
    


main() 
