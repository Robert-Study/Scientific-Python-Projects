"""
Intermediate Project 2: Spectral Analysis of Digital Signals (80%)

Showcase-only source converted from a Jupyter notebook.
Any student ID fields have been intentionally left blank.

NOTE: This code references the course-provided `module_engine` package in places.
The repository does not include `module_engine` (academic integrity / plagiarism prevention).
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from module_engine.assignment import Boxes


# Do not alter any of the code within this cell other than the value of studentID
studentID = ""  # intentionally left blank for showcase

# Creating box objects to be investigated in this assignment.
# Please do NOT change the line below. Your student ID must be inserted ABOVE.
# The "Student ID is valid" or "Student ID not found" message
# will be printed out six times (once by each box object), this is normal.

t1_box1, t1_box2, t1_box3, t1_box4, t2_box, t3_rec, check_SNR, play = Boxes.get_boxes(studentID)

sampling_rate=Boxes.SAMP_RATE
print("Audio sampling rate: ", sampling_rate, "Hz")

duration = 1
f1 = 10      #min 10
f2 = 4000    #max 4000
#sampling_rate = 44100Hz            (sampling_rate defined previously)
N = duration * sampling_rate       #(N = number of points)


times = np.linspace(0, duration, N, endpoint=False)            #times for each point
frequencies = np.linspace(f1, f2, N)                     #frequencies at each point in time
ssine_in = np.sin(2*np.pi*frequencies*times)             #ssine_in short for the swept sine wave input


 # time variables
tot_time = times[-1]-times[0]
timestep = tot_time/(N-1)


 # time axis
plt.figure(figsize=(15,3))
plt.plot(times, ssine_in, 'b-')
plt.title('Input signal')
plt.xlabel('t [s]')
plt.ylabel('V in [V]')
plt.axis([0, duration, -1, 1])
plt.show()


 # frequency axis
plt.figure(figsize=(15, 3))
plt.plot(frequencies, ssine_in, 'b-')
plt.title('Input Signal')
plt.xlabel('f [Hz]')
plt.ylabel('V in [V]')
plt.axis([f1, f2, -1, 1])
plt.show()

 # data
print("Data points = {}".format(N))
print("Total time  = {} s".format(tot_time))
print("Time step   = {} s".format(timestep))
print("time of first and last point = ", times[0],times[-1])
print("Sampling frequency = {} Hz".format((1/timestep)))

# INPUT SIGNAL

freq_in = np.fft.fftfreq(len(times), 1/sampling_rate)
freq_in = freq_in[freq_in >= 0]

signal_in = np.fft.fft(ssine_in)
signal_in = np.abs(signal_in[:len(freq_in)])

plt.figure(figsize=(10, 5))
plt.plot(freq_in, signal_in)
plt.title('Input Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()

# FILTERED SIGNAL (essentially the same as before just with 'box.process(times, ssine_in)', instead of 'ssine_in')

box = t1_box4   #CHANGE TO OTHER BOXES AS REQUIRED TO COMPARE

freq_out = np.fft.fftfreq(len(times), 1/sampling_rate)
freq_out = freq_out[freq_out >= 0]

signal_out = np.fft.fft(box.process(times, ssine_in))
signal_out = np.abs(signal_out[:len(freq_out)])

plt.figure(figsize=(10, 5))
plt.plot(freq_out, signal_out)
plt.title('Output Signal (with box)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()

RL_circuit = 1 #as similar to input above 5000Hz only
RC_circuit = 2 #as magnitude decreases with frequency (it matches ~250 magnitude only at 0Hz)
RLC_bandpass = 3 #as only reaches a magnitude ~250 at a specific frequency ~500Hz
RLC_bandstop = 4 #as matches input but at only ~500Hz the magnitude drops to 0

def my_box_process(t, s_in, R, L, C):
    f0 = 1 / (2*np.pi * np.sqrt(L*C))
    g = R / (2*np.pi*L)

    #frequency
    freq_in = np.fft.fftfreq(len(t), (t[1]-t[0]))
    f = freq_in[freq_in >= 0]

    s_in_freq = np.fft.fft(s_in)
    s_in_pos = s_in_freq[:len(f)]

    #transfer function
    T = (f**2 - f0**2) / (f**2 - f0**2 - 1j * g * f)

    #signal
    s_out_pos = s_in_pos * T
    s_out = np.fft.ifft(s_out_pos)
    s_out_real = np.real(s_out)

    return s_out_real

play(t3_rec)

student_figure = plt.figure(1, figsize=(15, 7))

# Params
duration = len(t3_rec) / sampling_rate
f_min = 20
f_max = 8000

# FFT
freqs = np.fft.fftfreq(len(t3_rec), 1/sampling_rate)
freqs_pos = freqs[freqs >= 0]

fft_vals = np.fft.fft(t3_rec)
fft_mag = np.abs(fft_vals)
fft_mag_pos = fft_mag[:len(freqs_pos)]

# Plot
plt.loglog(freqs_pos, fft_mag_pos)
plt.title('Spectrum')
plt.xlabel('f [Hz]')
plt.ylabel('X(f) - magnitude')
plt.grid(True)

# Noise peak
noise_idx = np.argmax(fft_mag_pos)
noise_freq = freqs_pos[noise_idx]

# Mark noise freq
plt.axvline(noise_freq, linestyle='--')
plt.show()
print(f"Noise peak frequency is at {noise_freq}Hz")

duration = len(t3_rec) / sampling_rate
times = np.linspace(0, duration, len(t3_rec), endpoint=False)

# filter multiple times
def my_box_process_n_times(t, s_in, R, L, C, N):
    s_out = my_box_process(t, s_in, R, L, C)
    if N == 1:
        return s_out
    elif N > 1:
        return my_box_process_n_times(t, s_out, R, L, C, N-1)
    else:
        print("Order of the filter N must be a positive integer")

# parameters
L = 0.0255
R = 300
C = 1.14e-6
N = 3  # filter order


filtered_signal = my_box_process_n_times(times, t3_rec, R, L, C, N)


play(filtered_signal)

# Calculate SNR
print(check_SNR(R, L, C, N))

# Provide your answer as a string
student_PIN = "5737"

# Uncomment the following lines if you do not have access to sound
# and provide your R,L,C, and N parameters
# Your signal to noise ratio (SNR) must exceed 1

# student_R =  # in Ohms
# student_L =  # in Henrys
# student_C =  # in Farads
# student_filter_order = # the order of the filter

Boxes.check()
