#!/usr/bin/python
# -*- coding: utf-8 -*-
# SKT 10/2014
# Input:
# (a) output file (Eabs) from WriteTable of Caribu in OpenAlea
# Output:
# (a) file that contains Eabs (energy absorbed) per layer, x.
#


from pylab import *
import matplotlib.pyplot as plt
from operator import itemgetter
import scipy.stats as sp
from collections import defaultdict
import numpy as np
import sys

def consume(iterator, n):
    collections.deque(itertools.islice(iterator, n))

if len(sys.argv) <= 1:
    print("calculate_eabs.py input_from_caribu.ssv")
    sys.exit()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("calculate_eabs.py input_from_caribu.ssv")
    sys.exit()
try:
    # read in LILI_caribu_input
    LILI_caribu_input = [line.strip() for line in open(sys.argv[1])]
    LILI_caribu_input = [element.split(' ') for element in LILI_caribu_input]
except IOError:
    print("Cannot open target file. Please check your input:")
    print("\t$ python calculate_eabs.py input_from_caribu.ssv")
    sys.exit()

# write input into LILI_caribu_input
li_tsv_temp=[]
li_tsv_filtered=[]
for i in range(len(LILI_caribu_input)):
    if i == 0:
        continue # header
    for j in range(len(LILI_caribu_input[i])):
        li_tsv_temp.append(float(LILI_caribu_input[i][9])) # Eabs
        li_tsv_temp.append(float(LILI_caribu_input[i][3])) # plant
        li_tsv_temp.append(float(LILI_caribu_input[i][4])) # leaf ?
        li_tsv_temp.append(float(LILI_caribu_input[i][5])) # area discretized
    li_tsv_filtered.append(li_tsv_temp)
    li_tsv_temp=[]
LILI_caribu_input = li_tsv_filtered

i_eabs=0.0
i_area=0.0
li_eabs=[]

# For each plant 
for i in range (len(LILI_caribu_input)):
    if i == len(LILI_caribu_input)-1:
        i_eabs = i_eabs + LILI_caribu_input[i][0]
        i_area = i_area + LILI_caribu_input[i][3]

        li_tsv_temp.append(i_eabs)

        li_eabs.append(li_tsv_temp)
        continue
    # for each phytomer (leaf or stem)
    if (LILI_caribu_input[i][1] == LILI_caribu_input[i+1][1]):
        if (LILI_caribu_input[i][2] ==LILI_caribu_input[i+1][2]):
            i_eabs = i_eabs + LILI_caribu_input[i][0]
            i_area = i_area + LILI_caribu_input[i][3]

        else:
            li_tsv_temp.append(i_eabs)
            i_eabs=0.0
            i_area=0.0

    else:
        i_eabs = i_eabs + LILI_caribu_input[i][0]
        i_area = i_area + LILI_caribu_input[i][3]

        li_tsv_temp.append(i_eabs)
        i_eabs=0.0
        i_area=0.0

        li_eabs.append(li_tsv_temp)
        li_tsv_temp=[]

print '\n'.join(('\t'.join(str(i) for i in item[0:])) for item in li_eabs)
