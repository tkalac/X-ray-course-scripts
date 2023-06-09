# -*- coding: utf-8 -*-
"""
Created on Fri May 11 09:34:12 2023

@author: Tine Kalac
"""

from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

########################
#      DATA INPUT      #
########################

### Data import
data = np.genfromtxt("WAXS_AuNP.txt", dtype=float, names=True)
data_bg = np.genfromtxt("WAXS_AuNP_background.txt", dtype=float, names=True)

### Background subctraction
data["I"]=data["I"]-data_bg["I"]

### Finding the peak
I_fit = signal.savgol_filter(data["I"], 25, 2)
peaks, _ = signal.find_peaks(I_fit, height=data["I"].max()*0.9)

### Baeline and FWHM
baseline_height=0.86

FWFM_indicies=signal.peak_widths(I_fit, peaks, rel_height=baseline_height)
FWHM_indicies=signal.peak_widths(I_fit, peaks, rel_height=baseline_height/2)

### Conversion from indicies to values
FWFM=FWFM_indicies[0]*(data["Q"][1]-data["Q"][0])
FWFM=FWFM.astype(str)

FWHM=FWHM_indicies[0]*(data["Q"][1]-data["Q"][0])
FWHM=FWHM.astype(str)


########################
#        OUTPUT        #
########################
print("Peak locations:", data["Q"][peaks])
print("FWHM:", FWHM)


########################
#        GRAPHS        #
########################

##  STYLE
plt.style.use('classic')
plt.rcParams["font.family"] = "Arial"
plt.rcParams['font.size'] = 11
plt.figure(figsize=(8,5))

### DATA
plt.plot(data["Q"], data["I"], label="AuNP", color="black")

### ANNOTATIONS
#   Peak
plt.plot(data["Q"][peaks], data["I"][peaks], "x", color="red", markersize=10)

#   Baseline and FWHM line 
plt.hlines(FWHM_indicies[1], data["Q"][FWHM_indicies[2].astype(int)], data["Q"][FWHM_indicies[3].astype(int)], color="red", linewidth=2)
plt.hlines(FWFM_indicies[1], data["Q"][FWFM_indicies[2].astype(int)], data["Q"][FWFM_indicies[3].astype(int)], color="green", linewidth=2)

#   Pointer and text
plt.plot([data["Q"][FWHM_indicies[3].astype(int)], data["Q"][FWHM_indicies[3].astype(int)+50]], [FWHM_indicies[1], FWHM_indicies[1]*1.25], color="red", linewidth=0.5)
plt.text(data["Q"][FWHM_indicies[3].astype(int)+50], FWHM_indicies[1]*1.25, "FWHM: %f"%FWHM, color="red")

plt.title("WAXS scattering intensity")
plt.xlabel("q $[\AA ^{-1}]$")
plt.ylabel("Intensity $[A.U.]$")
plt.legend(loc="upper left")
plt.grid(True)               

plt.savefig("AuNP_graph.png", dpi=300)
