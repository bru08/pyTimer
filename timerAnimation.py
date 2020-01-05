#!/Users/bruno_papa/.virtualenvs/cvpy3/bin/python
"""
This take minute to make a timer
plot a bar that decrease accordingly and show the remaining time
at the end reproduce an alarm
"""
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import pyaudio
import threading
import sys, select


########################################

mins=int(input("how many minutes?"))
secs=mins * 60
counter_height=secs/10

plt.ion()
plt.figure(figsize=(2, 5))
plt.axis("off")


for i in range(secs):
	inizio=time.time()

	s_t=60 - i % 60
	if i % 60 == 0:
		mins -= 1
	time_str=str(mins) + ":" + str(s_t)

	plt.axis("off")
	plt.bar(1, secs, color="white")

	if secs-i>secs/10:
		plt.bar(1, secs - i, color="blue")
	else:
		plt.bar(1, secs - i, color="red")

	plt.Circle((0,1), 10, color="green")
	plt.text(1, counter_height, 
		time_str, 
		bbox=dict(facecolor='white', alpha=0.5), 
		fontsize=20,
		horizontalalignment="center")

	plt.draw()
	plt.pause(1 - (time.time() - inizio))
	plt.clf()
#############################


# ending alarm
p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float

f = 440.0        # sine frequency, Hz, may be float
f2 = 750.0       # second frequency

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
sample2 = (np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


i=0 
while True:
	if i==0:
		stream.write(volume*samples)
		i=1
	elif i==1:
		stream.write(volume*sample2)
		i=0

	k, o, e = select.select( [sys.stdin], [], [], .5 )
	if k:
		break

stream.stop_stream()
stream.close()
p.terminate()
