#!/usr/bin/python
# -*- coding: utf-8 -*-

##### 12/12/2014
##### Written by Sandra Truong
#####
##### This python script takes in a .csv file of LP-80 data 
##### and plots humidity and temperature for small and large angle canopies.
##### 
##### Example use:
##### 
##### python plot_temperature_humidity.py ../LP-80_TinyTag_Data/01_07222014a_RIL63_vs_RIL73.csv
#####
##### Columns of .csv file:
##### time_start,
##### time_end,
##### ft_abv_grnd,
##### RIL_63_height_dbl_avg_PAR,
##### RIL_73_height_dbl_avg_PAR,
##### RIL_63_avg_temp_Celsius,
##### RIL_63_avg_relative_humidity,
##### RIL_73_avg_temp_Celsius,
##### RIL_73_avg_relative_humidity

import sys
from collections import defaultdict
import scipy.stats as sp
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from pylab import *
from scipy.optimize import curve_fit
import numpy.polynomial.polynomial as poly


##### Read in input .csv
if len(sys.argv) <= 1:
    print("plot_temperature_humidity.py input.csv")
    sys.exit()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("plot_temperature_humidity.py input.csv")
    sys.exit()
try:
    str_dateOfData = (sys.argv[1].split("/"))[2]
    LILI_TABLE = [line.strip() for line in open(sys.argv[1])]
    LILI_TABLE = [element.split(',') for element in LILI_TABLE]

except IOError:
    print("Cannot open target file. Please check your input:")
    print("\t$ python plot_temperature_humidity.py input.csv")
    sys.exit()

###### class Individual
######   has a genotype
######   has a height
######   has a list of feetAboveGroundIndex
######   has a list of temperature
######   has a list of humidity
######   has a list of PAR

class Individual:
	"""This is the class Individual"""
	def __init__(self, genotype, height):
		self.__genotype = genotype
		self.__height = height
		self.__feetAboveGroundIndex = []           		
		self.__PAR = []   
		self.__keepRAW_PAR = []
		self.__keepRAW_depth = []
		self.__humidity = []
		self.__temperature = []         		
		self.__premature_sc_PAR = []
		self.__sc_PAR = []
		self.__sc_depth = []
		self.__sc_temperature = []
		self.__sc_humidity = []
		self.__plot_color=""

	def genotype(self):
		return self.__genotype
	def height(self):
		return self.__height
	def feetAboveGroundIndex(self):
		return self.__feetAboveGroundIndex
	def temperature(self):
		return self.__temperature
	def PAR(self):
		return self.__PAR
	def humidity(self):
		return self.__humidity

	def add_feetindex(self, inputFeetIndex):
		self.__feetAboveGroundIndex.append(inputFeetIndex)
	def add_temperature(self, inputTemperature):
		self.__temperature.append(inputTemperature)
	def add_PAR(self, inputPAR):
		self.__PAR.append(inputPAR)
	def add_humidity(self, inputHumidity):
		self.__humidity.append(inputHumidity)

	def scale_attributes_by_canopy_depth(self):
		for index_ft in range(0, len(self.feetAboveGroundIndex())):
			if ((self.feetAboveGroundIndex())[index_ft]/self.height() <= 0.99 and (self.feetAboveGroundIndex())[index_ft]/self.height()  >= 0.0):
				self.__premature_sc_PAR.append((self.PAR())[index_ft])
				self.__sc_depth.append(100.0*((self.feetAboveGroundIndex())[index_ft]/self.height()))
				self.__keepRAW_PAR.append((self.PAR())[index_ft])
				self.__keepRAW_depth.append((self.feetAboveGroundIndex())[index_ft])
				self.__sc_humidity.append(((self.humidity())[index_ft]))
				self.__sc_temperature.append((self.temperature())[index_ft])

			else:
				sys.stderr.write("Attributes above canopy \n")

	def sc_depth(self):
		return self.__sc_depth
	def keepRAW_depth(self):
		return self.__keepRAW_depth
	def keepRAW_PAR(self):
		return self.__keepRAW_PAR
	def premature_sc_PAR(self):
		return self.__premature_sc_PAR
	def sc_humidity(self):
		return self.__sc_humidity
	def sc_temperature(self):
		return self.__sc_temperature

	def scale_attributes_by_PAR(self):
		max_pre_sc_PAR = float(max(self.premature_sc_PAR()))
		for index_depth in range(0, len(self.sc_depth())):
			self.__sc_PAR.append(100.0*(((self.premature_sc_PAR())[index_depth])/max_pre_sc_PAR))
	
	def sc_PAR(self):
		return self.__sc_PAR

	def plot_color(self):
		if self.genotype() == int(63):
			self.__plot_color="#4169E1"
		elif self.genotype() == int(73):
			self.__plot_color="#FF8C00"
		else:
			sys.stderr.write("Unexpected genotype \n")
		return self.__plot_color


## Read in data for RIL 63 and RIL 73
INDEX_COLUMN_time_start				= 0
INDEX_COLUMN_time_end				= 1
INDEX_COLUMN_ft_abv_grnd			= 2
INDEX_COLUMN_RIL_63_height_dbl_avg_PAR		= 3
INDEX_COLUMN_RIL_73_height_dbl_avg_PAR		= 4
INDEX_COLUMN_RIL_63_avg_temp_Celsius		= 5
INDEX_COLUMN_RIL_63_avg_relative_humidity	= 6
INDEX_COLUMN_RIL_73_avg_temp_Celsius		= 7
INDEX_COLUMN_RIL_73_avg_relative_humidity	= 8
INDEX_COLUMN_avg_abv_PAR			= 9

INDEX_ROW_descriptor				= 0

ril63 = Individual(int(63), float(((LILI_TABLE[INDEX_ROW_descriptor][INDEX_COLUMN_RIL_63_height_dbl_avg_PAR]).split("_"))[3]))

ril73 = Individual(int(73), float(((LILI_TABLE[INDEX_ROW_descriptor][INDEX_COLUMN_RIL_73_height_dbl_avg_PAR]).split("_"))[3]))

for index_row in range((INDEX_ROW_descriptor+1),len(LILI_TABLE)):
	ril63.add_feetindex(float(LILI_TABLE[index_row][INDEX_COLUMN_ft_abv_grnd]))
	ril63.add_temperature(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_63_avg_temp_Celsius]))
	ril63.add_PAR(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_63_height_dbl_avg_PAR]))
	ril63.add_humidity(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_63_avg_relative_humidity]))
	ril73.add_feetindex(float(LILI_TABLE[index_row][INDEX_COLUMN_ft_abv_grnd]))
	ril73.add_temperature(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_73_avg_temp_Celsius]))
	ril73.add_PAR(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_73_height_dbl_avg_PAR]))
	ril73.add_humidity(float(LILI_TABLE[index_row][INDEX_COLUMN_RIL_73_avg_relative_humidity]))

ril63.scale_attributes_by_canopy_depth()
ril73.scale_attributes_by_canopy_depth()
ril63.scale_attributes_by_PAR()
ril73.scale_attributes_by_PAR()

plot_rows = 1
plot_columns = 3

fig = plt.figure(figsize=(25*(2.0/3.0),10*(2.0/3.0)))

#################
##### PAR #######
#################
##### Plot raw height without respect to height of plant and raw PAR
plt.subplot2grid((plot_rows,plot_columns),(0, 0))
# plot all raw data with lines to represent sequence of aquisition
plot(ril63.PAR(), ril63.feetAboveGroundIndex(), '--o', color=ril63.plot_color(), alpha=0.4)
plot(ril73.PAR(), ril73.feetAboveGroundIndex(), '--o', color=ril73.plot_color(), alpha=0.4)
# plot data to be used for further curation
plot(ril63.keepRAW_PAR(), ril63.keepRAW_depth(), 'o', color=ril63.plot_color(), label='RIL 63 - small angles')
plot(ril73.keepRAW_PAR(), ril73.keepRAW_depth(), 'o', color=ril73.plot_color(), label='RIL 73 - large angles')
plt.xlabel('PAR ' r'($\mu$mol $m^{-2} s^{-1}$)')
plt.ylabel('depth (ft)')
plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)
plt.title(str_dateOfData)
plt.ylim([1,14.5])

####################
#### humidity ######
####################
plt.subplot2grid((plot_rows,plot_columns),(0, 1))
plt.ylabel('depth (ft)')
# plot all raw data with lines to represent sequence of aquisition
plot(ril63.humidity(), ril63.feetAboveGroundIndex(), '--+', color=ril63.plot_color(), alpha=0.4)
plot(ril73.humidity(), ril73.feetAboveGroundIndex(), '--+', color=ril73.plot_color(), alpha=0.4)
# plot data to be used for further curation
plot(ril63.sc_humidity(), ril63.keepRAW_depth(), '+', color=ril63.plot_color(), label='humidity')
plot(ril73.sc_humidity(), ril73.keepRAW_depth(), '+', color=ril73.plot_color(), label='humidity')
plt.xlabel('Humidity ' r'($\%$)')
plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)
plt.ylim([1,14.5])


#######################
#### temperature ######
#######################
##### Plot raw height without respect to height of plant and raw PAR
plt.subplot2grid((plot_rows,plot_columns),(0, 2))
plt.ylabel('depth (ft)')
# plot all raw data with lines to represent sequence of aquisition
plot(ril63.temperature(), ril63.feetAboveGroundIndex(), '--x', color=ril63.plot_color(), alpha=0.4)
plot(ril73.temperature(), ril73.feetAboveGroundIndex(), '--x', color=ril73.plot_color(), alpha=0.4)
# plot data to be used for further curation
plot(ril63.sc_temperature(), ril63.keepRAW_depth(), 'x', color=ril63.plot_color(), label='temperature')
plot(ril73.sc_temperature(), ril73.keepRAW_depth(), 'x', color=ril73.plot_color(), label='temperature')
plt.xlabel('Temperature ' r'($^{o} C$)')
plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)

#plt.show()

plt.savefig("PAR_HUM_TEMP_RIL63_RIL73_01.png", dpi=300, format="png")
