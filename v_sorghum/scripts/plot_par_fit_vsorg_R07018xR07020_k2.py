#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# python plot_par_fit_vsorg_R07018xR07020_k2.py ../caribu_out/July_22_2014/R07018xR07020_63/1530_20_eabs ../caribu_out/July_22_2014/R07018xR07020_63/1530_20_plant_positions ../caribu_out/July_22_2014/R07018xR07020_73/1530_20_eabs ../caribu_out/July_22_2014/R07018xR07020_73/1530_20_plant_positions

from pylab import *
import matplotlib.pyplot as plt
from operator import itemgetter
import scipy.stats as sp
from collections import defaultdict
import numpy as np
import sys
from scipy.optimize import curve_fit
from math import *

def consume(iterator, n):
    collections.deque(itertools.islice(iterator, n))

if len(sys.argv) <= 4:
    print("plotEABs.py 1_eabs.tsv 1_plant_position 2_eabs.tsv 2_plant_position")
    sys.exit()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("plotEABs.py 1_eabs.tsv 1_plant_position 2_eabs.tsv 2_plant_position")
    sys.exit()
try:
    li_1_eabs = [line.strip() for line in open(sys.argv[1])]
    li_1_eabs = [element.split('\t') for element in li_1_eabs]

    li_1_pp = [line.strip() for line in open(sys.argv[2])]
    li_1_pp = [element.split(' ') for element in li_1_pp]

    li_2_eabs = [line.strip() for line in open(sys.argv[3])]
    li_2_eabs = [element.split('\t') for element in li_2_eabs]

    li_2_pp = [line.strip() for line in open(sys.argv[4])]
    li_2_pp = [element.split(' ') for element in li_2_pp]

except IOError:
    print("Cannot open target file. Please check your input:")
    print("\t$ python plotEABs.py 1_eabs.tsv 1_planter_position 2_eabs.tsv 2_planter_position")
    sys.exit()

###### convert KJ/m^2s^1 to umol/m^2s^1
###### 2000umol/m2/s = 9800FC = 1060W/m2 = 1060J/m2/s = 106000LUX.  
###### 2000/1060 umol/J 1000/1 J/KJ
def KJ_to_umol(KJ):
	return (2000/1060)*1000.0*KJ

li_1X = []
li_1Y = []
li_2X = []
li_2Y = []

li_1X_percent = []
li_1Y_percent = []
li_2X_percent = []
li_2Y_percent = []

LILI_1Y =[]
LILI_2Y =[]

LILI_1Y_percent = []
LILI_2Y_percent = []

LI_plant_row_pos = ["1.0466507177", "1.14633173844", "1.24601275917", "1.3456937799", "1.44537480064", "1.54505582137", "1.64473684211", "1.74441786284", "1.84409888357", "1.94377990431"]
LI_plant_col_pos = ["1.14", "1.9"]

row = int(0)
col = int(1)
for assayed_col in range(len(LI_plant_col_pos)):
	for assayed_row in range(len(LI_plant_row_pos)):
		for plant in range(len(li_1_pp)):
			if (li_1_pp[plant][col] == LI_plant_col_pos[assayed_col]) and (li_1_pp[plant][row] == LI_plant_row_pos[assayed_row]):
				for eabs in range(len(li_1_eabs[plant])):
            				if eabs%2==0 and (eabs !=len(li_1_eabs[plant])-1):
                				li_1Y.append(float(li_1_eabs[plant][eabs])+float(li_1_eabs[plant][eabs+1]))
				for i in range(len(li_1Y)):
					li_1Y_percent.append((li_1Y[i]/max(li_1Y))*100.0)
				break
		LILI_1Y.append(li_1Y)
		LILI_1Y_percent.append(li_1Y_percent)
		li_1Y = []
		li_1Y_percent = []
		for plant in range(len(li_2_pp)):
			if (li_2_pp[plant][col] == LI_plant_col_pos[assayed_col]) and (li_2_pp[plant][row] == LI_plant_row_pos[assayed_row]):
				for eabs in range(len(li_2_eabs[plant])):
            				if eabs%2==0 and (eabs !=len(li_2_eabs[plant])-1):
                				li_2Y.append(float(li_2_eabs[plant][eabs])+float(li_2_eabs[plant][eabs+1]))
				for i in range(len(li_2Y)):
					li_2Y_percent.append((li_2Y[i]/max(li_2Y))*100.0)
				break
		LILI_2Y.append(li_2Y)
		LILI_2Y_percent.append(li_2Y_percent)
		li_2Y = []
		li_2Y_percent = []

for i in range(len(LILI_1Y[0])):
	li_1X.append(float(i+1))
	li_1X_percent.append(((float(i)+1.0)/float(len(LILI_1Y[0])))*100)
for phytomer in range(len(LILI_1Y[0])):
	phytomer_energy = 0.0	
	for plant in range(len(LILI_1Y)):
		phytomer_energy = phytomer_energy + LILI_1Y[plant][phytomer]
	li_1Y.append(phytomer_energy)
	

for i in range(len(LILI_2Y[0])):
	li_2X.append(float(i+1))
	li_2X_percent.append(((float(i)+1.0)/float(len(LILI_2Y[0])))*100)
for phytomer in range(len(LILI_2Y[0])):
	phytomer_energy = 0.0	
	for plant in range(len(LILI_2Y)):
		phytomer_energy = phytomer_energy + LILI_2Y[plant][phytomer]
	li_2Y.append(phytomer_energy)

light_available = sum(li_1Y)
li_1Y = list(reversed(li_1Y))
li_1X = list(reversed(li_1X))
li_1X_percent = list(reversed(li_1X_percent))

li_1Y_available = []
for phytomer in range(len(li_1Y)):
	light_available = light_available - sum(li_1Y[phytomer])
	li_1Y_available.append(light_available)

light_available = sum(li_2Y)
li_2Y = list(reversed(li_2Y))
li_2X = list(reversed(li_2X))
li_2X_percent = list(reversed(li_2X_percent))

li_2Y_available = []
for phytomer in range(len(li_2Y)):
	light_available = light_available - sum(li_2Y[phytomer])
	li_2Y_available.append(light_available)

# convert kJ to umol
li_1Y_available = KJ_to_umol(np.array(li_1Y_available))
li_2Y_available = KJ_to_umol(np.array(li_2Y_available))

# plot colors
small_color = "#4169E1"
large_color = "#FF8C00"


###### PAR(depth) = PAR(top)*(np.exp(k*depth)) 
def light_func((ril_depth, ril_height),k,PARtop):
	return PARtop*(np.exp(-k*(ril_height-ril_depth)))

li_1X_percent_all = 100*(np.array(li_1X_percent)/(li_1X_percent[2]))
li_2X_percent_all = 100*(np.array(li_2X_percent)/(li_2X_percent[2]))

# whorl phytomers are set to the same depth:
li_1X_percent_all[0] = 100
li_2X_percent_all[0] = 100
li_1X_percent_all[1] = 100
li_2X_percent_all[1] = 100

# fit phytomers for k2
li_1X_percent = li_1X_percent_all[2::]
li_2X_percent = li_2X_percent_all[2::]

li_1Y_available_all = li_1Y_available
li_2Y_available_all = li_2Y_available

li_1Y_available = li_1Y_available[2::]
li_2Y_available = li_2Y_available[2::]

##### Fitting data to light absorption curve (Beer-Lambert's law)
pop1,popc = curve_fit(light_func, ((li_1X_percent), np.array(max(li_1X_percent))) , (li_1Y_available))
k_1, partop_1 = pop1
pop2,popc = curve_fit(light_func, ((li_2X_percent), np.array(max(li_2X_percent))) , (li_2Y_available))
k_2, partop_2 = pop2

##### Plot % depth and PAR available with curve fit
fig = plt.figure(figsize=(9*(2.0/3.0),5*(2.0/3.0)))
plot(np.array(li_1Y_available_all), li_1X_percent_all, '--o', color=small_color)
plot(np.array(li_2Y_available_all), li_2X_percent_all, '--o', color=large_color)
##### plot the curve_fit
plot(light_func((np.linspace(0.0, max(li_2X_percent)*2, 200), np.array(max(li_2X_percent))), k_2, partop_2), np.linspace(0., max(li_2X_percent)*2, 200), color=large_color,label=r'$k_{2}$ = %f' %(k_2))
plot(light_func((np.linspace(0.0, max(li_1X_percent)*2, 200), np.array(max(li_1X_percent))), k_1, partop_1), np.linspace(0., max(li_1X_percent)*2, 200), color=small_color,label=r'$k_{2}$ = %f' %(k_1))

plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)
plt.xlabel('PAR available ' r'($\mu$mol $m^{-2} s^{-1}$)')
plt.ylabel('% depth')
plt.xlim(-15.0, 2300)
plt.ylim(-1.0, 104.0)

plt.savefig("vsorg_R07018xR07020_k2.png", dpi=300, format="png")



