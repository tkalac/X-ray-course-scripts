# -*- coding: utf-8 -*-
"""
Created on Thu May 11 22:04:33 2023

@author: Tine
"""

from matplotlib import pyplot as plt
import numpy as np
import os.path
from scipy import signal


########################
#      PLOT INIT       #
########################

plt.style.use('classic')
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

### Color gradient for the Kratky plots
colors = plt.cm.viridis(np.linspace(0,1,10))

### Creating the plot objects
fig1, ax1 = plt.subplots()    # Kratky plot
fig2, ax2 = plt.subplots()    # Kratky plot + curve fits
fig3, (ax3, ax4) = plt.subplots(nrows=2, ncols=1)    #Peaks and transmittance


########################
#     DATA IMPORT      #
########################

### Path to data files
path = os.path.dirname(os.path.realpath(__file__)) + '\preprocessed data'

### Counting the files in file folder
num_files = len([f for f in os.listdir(path)
if os.path.isfile(os.path.join(path, f))])

### Generate a list with the data file names
data_file_names=[]
for x in os.walk(path):
    data_file_names = np.append(data_file_names, x[2])

### Generate the list of sampling times from data file names
time = []
for j in range(len(data_file_names)):
    time = np.append(time, data_file_names[j].replace('.txt', ''))
    time = time.astype(int)

### Writing the first data file into a NumPy array
data=np.loadtxt("preprocessed data/20.txt", skiprows=1)

### Appending the data from the other files into the array
for i in range(num_files-1):
    data_i=np.loadtxt("preprocessed data/%d.txt"%time[i+1], skiprows=1)
    data=np.append(data, data_i, axis=1)



########################
#    DATA ANALYSIS     #
########################

### Plotting the data in Kratky plots (both figures)
for i in range(num_files):
    data[:,2*i+1]=data[:,2*i+1]*(data[:,0])**2
    ax1.plot(data[:,0], data[:,2*i+1], color=colors[i], label="%d minutes"%time[i])
    ax2.plot(data[:,0], data[:,2*i+1], color=colors[i], label="%d minutes"%time[i])

### Limits for the fitting interval
fit_limit_low=90
fit_limit_high=400

### Initialise the array for the peaks
peaks=[]

### Curve fitting, peak finding and plotting the models
for i in range(num_files):
    I_fit = signal.savgol_filter(data[fit_limit_low:fit_limit_high, 2*i+1], 300, 3)
    ax2.plot(data[fit_limit_low:fit_limit_high, 0], I_fit, color="red")
    peak, _ = signal.find_peaks(I_fit)
    peaks = np.append(peaks, peak)
    ax2.scatter(data[peak+fit_limit_low, 0], I_fit[peak], color="black")

### Conversion to integer type for indexing
peaks=peaks.astype(int)



########################
#      TIME PLOTS      #
########################

### Polynomial regression curve for Bragg distace plot, from the peaks
bragg_poly = np.poly1d(np.polyfit(time, 2*np.pi/data[peaks,0], deg=3))

ax3.scatter(time, 2*np.pi/data[peaks,0], color="black", label="scattering peaks")
ax3.plot(time, bragg_poly(time), color="red")

### Polynomial regression for transmittance plot
transmittance = np.loadtxt("transmitance.txt", skiprows=1)
transmittance_poly = np.poly1d(np.polyfit(time, transmittance[:,1], deg=1))

ax4.scatter(time, transmittance[:,1], label="transmittance", color="black")
ax4.plot(time, transmittance_poly(time), color="red")



########################
#        GRAPHS        #
########################

### FIGURE 1

### Figure width and height
fig1.set_figwidth(10)
fig1.set_figheight(8)

### Axis limits
ax1.set_xlim(0, data[:,0].max()+0.02)
ax1.set_ylim(0, 0.022)

### Labels and legends
ax1.set_title("SAXS intensity of drying CNF hydrogel")
ax1.set_xlabel("q $[nm^{-1}]$")
ax1.set_ylabel("$q^2*I(q)$")
ax1.legend(loc="upper right")


### FIGURE 2

### Figure width and height
fig2.set_figwidth(10)
fig2.set_figheight(8)

### Axis limits
ax2.set_xlim(0, data[:,0].max()+0.02)
ax2.set_ylim(0, 0.022)

### Labels and legends
ax2.set_title("SAXS intensity of drying CNF hydrogel")
ax2.set_xlabel("q $[nm^{-1}]$")
ax2.set_ylabel("$q^2*I(q)$")
ax2.legend(loc="upper right")


### FIGURE 3

### Figure width and height
fig3.set_figwidth(5)
fig3.set_figheight(10)

### Labels and legends
ax3.set_xlabel("time $[min]$")
ax3.set_ylabel("Bragg distance $[nm]$")
ax3.legend(loc="upper right")


### FIGURE 4

ax4.set_xlabel("time $[min]$")
ax4.set_ylabel("transmittance $[\%]$")
ax4.legend(loc="upper left")

### Save plots as images 

fig1.savefig("cnf_drying_saxs.png")
fig2.savefig("cnf_drying_saxs_model.png")
fig3.savefig("cnf_drying_interfibrilar_distance.png")



