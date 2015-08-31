#!/usr/bin/python
# -*- coding: utf-8 -*-

##### 12/04/2014
##### Written by Sandra Truong
#####
##### This python script takes in a .csv file of LP-80 data 
##### and plots light available for small and large angle canopies.
##### It also fits data to Beer-Lambert's Law.
##### Example use:
##### 
##### python plot_PAR_fit.py ../LP-80_TinyTag_Data/01_07222014a_RIL63_vs_RIL73.csv
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


from collections import defaultdict
from matplotlib.ticker import FuncFormatter
from pylab import *
from scipy.optimize import curve_fit
import sys
import scipy.stats as sp
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly




##### Read in input .csv
if len(sys.argv) <= 1:
    print("plot_PAR_fit.py input.csv")
    sys.exit()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("plot_PAR_fit.py input.csv")
    sys.exit()
try:
    str_dateOfData = (sys.argv[1].split("/"))[2]
    LILI_TABLE = [line.strip() for line in open(sys.argv[1])]
    LILI_TABLE = [element.split(',') for element in LILI_TABLE]

except IOError:
    print("Cannot open target file. Please check your input:")
    print("\t$ python plot_PAR_fit.py input.csv")
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
		self.__sigmoid_humidity_parameters = []
		self.__sigmoid_temperature_parameters = []
		self.__hyperbolic_humidity_parameters = []
		self.__hyperbolic_temperature_parameters = []
		self.__hyperbolic_humidity_parameters = []

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

###### PAR(depth) = PAR(top)*(np.exp(k*depth)) 
def light_func((ril_depth, ril_height),k,PARtop):
	return PARtop*(np.exp(-k*(ril_height-ril_depth)))

plot_rows = 2
plot_columns = 1

fig = plt.figure(figsize=(9*(2.0/3.0),10*(2.0/3.0)))
##### Plot depth in the canopy and PAR with fit to Beer-Lambert's law
plt.subplot2grid((plot_rows,plot_columns),(0, 0))
##### plot curated data to PAR and depth into repspective canopies
plot(ril63.keepRAW_PAR(), ril63.keepRAW_depth(), '--o', color="#4169E1")
plot(ril73.keepRAW_PAR(), ril73.keepRAW_depth(), '--o', color="#FF8C00")
##### Fitting data to light absorption curve (Beer-Lambert's law)
popt,popc = curve_fit(light_func, (np.array(ril63.keepRAW_depth()), np.array(ril63.height())) , np.array(ril63.keepRAW_PAR()))
k_63, partop_63 = popt
popt,popc = curve_fit(light_func, (np.array(ril73.keepRAW_depth()), np.array(ril73.height())) , np.array(ril73.keepRAW_PAR()))
k_73, partop_73 = popt
##### plot the curve_fit
plot(light_func((np.linspace(-5.0, ril73.height(), 200), np.array(ril73.height())), k_73, partop_73), np.linspace(0., ril73.height(), 200), color="#FF8C00",label='k = %f' %(k_73))
plot(light_func((np.linspace(-5.0, ril63.height(), 200), np.array(ril63.height())), k_63, partop_63), np.linspace(0., ril63.height(), 200), color="#4169E1",label='k = %f' %(k_63))
#plt.xlabel('PAR ' r'($\mu$mol $m^{-2} s^{-1}$)')
plt.ylabel('depth (ft)')
frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)
#plt.title(str_dateOfData)

##### Plot % depth in the canopy and PAR  with fit to Beer-Lambert's law
plt.subplot2grid((plot_rows,plot_columns),(1, 0))
##### plot curated data to PAR and % depth into repspective canopies
plot(ril63.keepRAW_PAR(), ril63.sc_depth(), '--o', color="#4169E1")
plot(ril73.keepRAW_PAR(), ril73.sc_depth(), '--o', color="#FF8C00")
##### Fitting data to light absorption curve (Beer-Lambert's law)
popt,popc = curve_fit(light_func, (np.array(ril63.sc_depth()), np.array(100.0)) , np.array(ril63.keepRAW_PAR()))
k_63, partop_63 = popt
popt,popc = curve_fit(light_func, (np.array(ril73.sc_depth()), np.array(100.0)) , np.array(ril73.keepRAW_PAR()))
k_73, partop_73 = popt
##### plot the curve_fit
plot(light_func((np.linspace(-5.0, 100.0, 200), np.array(100.0)), k_73, partop_73), np.linspace(0., 100.0, 200), color="#FF8C00",label='k = %f' %(k_73))
plot(light_func((np.linspace(-5.0, 100.0, 200), np.array(100.0)), k_63, partop_63), np.linspace(0., 100.0, 200), color="#4169E1",label='k = %f' %(k_63))
plt.ylabel('% depth')
plt.xlabel('PAR ' r'($\mu$mol $m^{-2} s^{-1}$)')
plt.legend(numpoints=1, bbox_to_anchor=(1, 0), loc=4, borderaxespad=0.)

plt.savefig("PAR_RIL63_RIL73_0X.png", dpi=300, format="png")

