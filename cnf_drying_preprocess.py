# -*- coding: utf-8 -*-
"""
Created on Thu May 11 22:07:41 2023

@author: Tine Kalac
"""

newlines=['Q\tI\n']

with open('SAXS_Sample_A.txt') as A_bg:
    lines = A_bg.readlines()
    for i in range(len(lines)):
        lines[i]=lines[i].lstrip()
        lines[i]=lines[i].replace('   ', '\t')
        newlines.append(lines[i])
        
with open('preprocessed data\A.txt', 'w') as newfile:
    for j in range(len(newlines)):
        newfile.write(newlines[j])
