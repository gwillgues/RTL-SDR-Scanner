# RTL-SDR-Scanner
Scan frequencies for traffic with an RTL-SDR

Requires pyrtlsdr Python library

Usage (Linux):
```
python3 -m pip install -r requirements.txt
```


```
./scan_sdr.py 2>/dev/null 
```

Example output:
![image](https://github.com/gwillgues/RTL-SDR-Scanner/assets/96144967/dc9bfb5f-d5b3-4b9e-b636-79e8688e6c88)




You can modify the ```freq_list``` list variable to contain frequencies you want to monitor. By default it has GMRS frequencies.

Since librtlsdr writes debug logging to stderr without providing a way to capture or redirect it, we have to use bash to redirect stderr to /dev/null. If on Windows, find your own method, or deal with the librtlsdr output. 

The script iterates over the list of frequencies, takes 3 samples on each frequency and gets the average power level (dB), and creates a noise floor baseline. Then, it iterates over each frequency checking for any signal that is 15 dB stronger than the previously acquired baseline. If there is a match, the script prints out "Activity on FREQUENCY"


