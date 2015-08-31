#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# python plot_eabs_par_fit.py /home/skt/Documents/LeafAngle/CaribuOut/July_04_2014/smallangle/1500_eabs /home/skt/Documents/LeafAngle/CaribuOut/July_04_2014/smallangle/1500_plant_positions /home/skt/Documents/LeafAngle/CaribuOut/July_04_2014/largeangle/1500_eabs /home/skt/Documents/LeafAngle/CaribuOut/July_04_2014/largeangle/1500_plant_positions


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

if len(sys.argv) <= 2:
    print("calculate_LAI_from_aream2.py plant_aream2.tsv plant_position")
    sys.exit()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("calculate_LAI_from_aream2.py plant_aream2.tsv plant_position")
    sys.exit()
try:
    li_1_area = [line.strip() for line in open(sys.argv[1])]
    li_1_area = [element.split('\t') for element in li_1_area]

    li_1_pp = [line.strip() for line in open(sys.argv[2])]
    li_1_pp = [element.split(' ') for element in li_1_pp]

except IOError:
    print("Cannot open target file. Please check your input:")
    print("\t$ python calculate_LAI_from_aream2.py plant_aream2.tsv plant_position")
    sys.exit()

li_plant = []

LILI_plants = []


LI_plant_row_pos = ["1.0466507177", "1.14633173844", "1.24601275917", "1.3456937799", "1.44537480064", "1.54505582137", "1.64473684211", "1.74441786284", "1.84409888357", "1.94377990431"]
LI_plant_col_pos = ["1.14", "1.9"]

row = int(0)
col = int(1)
plant_leaf_area=float(0.0)
	
leaf_area_1 =float(0.0)
leaf_area_2 =float(0.0)
leaf_area_3 =float(0.0)
leaf_area_4 =float(0.0)
leaf_area_5 =float(0.0)
leaf_area_6 =float(0.0)
leaf_area_7 =float(0.0)
leaf_area_8 =float(0.0)
leaf_area_9 =float(0.0)

for assayed_col in range(len(LI_plant_col_pos)):
	for assayed_row in range(len(LI_plant_row_pos)):
		for plant in range(len(li_1_pp)):
			if (li_1_pp[plant][col] == LI_plant_col_pos[assayed_col]) and (li_1_pp[plant][row] == LI_plant_row_pos[assayed_row]):
				for area in range(len(li_1_area[plant])):
            				if area%2==1:
						plant_leaf_area=plant_leaf_area+float(li_1_area[plant][area])
						if area == 1:
                					leaf_area_1= leaf_area_1+float(li_1_area[plant][area])
						elif area == 3:
                					leaf_area_2= leaf_area_2+float(li_1_area[plant][area])
						elif area == 5:
                					leaf_area_3= leaf_area_3+float(li_1_area[plant][area])
						elif area == 7:
                					leaf_area_4= leaf_area_4+float(li_1_area[plant][area])
						elif area == 9:
                					leaf_area_5= leaf_area_5+float(li_1_area[plant][area])
						elif area == 11:
                					leaf_area_6= leaf_area_6+float(li_1_area[plant][area])
						elif area == 13:
                					leaf_area_7= leaf_area_7+float(li_1_area[plant][area])
						elif area == 15:
                					leaf_area_8= leaf_area_8+float(li_1_area[plant][area])
						elif area == 17:
                					leaf_area_9= leaf_area_9+float(li_1_area[plant][area])
						
				break

print("LAI:")
print(plant_leaf_area/2)		
print(leaf_area_1/2)
print(leaf_area_2/2)
print(leaf_area_3/2)
print(leaf_area_4/2)
print(leaf_area_5/2)
print(leaf_area_6/2)
print(leaf_area_7/2)
print(leaf_area_8/2)
print(leaf_area_9/2)	



