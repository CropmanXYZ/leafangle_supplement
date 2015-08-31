#!/usr/bin/python
# 03/31/2015
# Written by Sandra Truong and Ryan McCormick
#
# This python script takes in a .csv file of RIL metrics from R07018xR07020 plots CS Field 2014 and
#      plots summary box plots.
# Example use:
# python plot_boxplots_metadata_x_genotype.py ../Meta_Data/R07018xR07020_metrics.csv

import sys
import matplotlib.pyplot as plt

###
# Global variables
###

# Defining column numbers of data of interest from input .csv file.
INDEX_COLUMN_RIL		= 0    # ID of the RIL (63 or 73)
INDEX_COLUMN_REP		= 1    # number of the plant replicate
INDEX_COLUMN_LEAF_NUMBER	= 2    # number of the leaf
INDEX_COLUMN_AREA		= 3    # leaf area (cm^2)
INDEX_COLUMN_SUBTOTAL		= 4    # irrelevant value reported by acquisition tool
INDEX_COLUMN_MAX_WIDTH		= 5    # max leaf width (cm)
INDEX_COLUMN_AVG_WIDTH		= 6    # leaf width (cm)
INDEX_COLUMN_LENGTH		= 7    # leaf length (cm)
INDEX_COLUMN_ANGLE		= 8    # leaf angle (degrees)
INDEX_COLUMN_STEM_LENGTH	= 9    # stem length (inches)
INDEX_COLUMN_STEM_DIAMETER	= 10   # stem diameter (mm)
INDEX_COLUMN_RIL_HEIGHT		= 11   # height of the entire plant (inches)
INDEX_COLUMN_RIL_DRY_WEIGHT	= 12   # weight of the entire plant (g)

# The list of lists that data will be read into from the input file.
LILI_TABLE = []

###
# End global variables
###


###
# Classes corresponding to plant components
###
class Individual:
     """The Individual constructor expects a genotype ID (integer), a dry weight (float), and 
          a height (float). The constructor initializes an empty list of 
          Phytomer objects that needs to be populated using addPhytomer(). """
     def __init__(self, genotype, dry_weight, height):
          self.__genotype = genotype
          self.__dry_weight = dry_weight
          self.__height = height
          self.__phytomers = []

     def getGenotype(self):
          return self.__genotype
     def getDryWeight(self):
          return self.__dry_weight
     def getHeight(self):
          return self.__height
     def getPhytomers(self):
          return self.__phytomers
     def getNumberPhytomers(self):
          return len(self.__phytomers)
     def getDryWeightPerHeight(self):
          return float(self.__dry_weight)/float(self.__height)

     def addPhytomer(self, input_phytomer):
          self.__phytomers.append(input_phytomer)

class Phytomer:
     """The Phytomer constructor expects the number of the phytomer (i.e. phytomer ID) (integer).
          Phytomer objects have Stem and Leaf objects which are added using makeLeaf() or makeStem(). """
     def __init__(self, number_phytomer):
          self.__number = number_phytomer

     def getNumber(self):
          return self.__number
     def getLeaf(self):
          return self.__Leaf
     def getStem(self):
          return self.__Stem

     def makeLeaf(self, input_leaf):
          self.__Leaf = input_leaf
     def makeStem(self, input_stem):
          self.__Stem = input_stem

class Leaf:
     """The Leaf constructor expects the leaf angle (float), leaf area (float), leaf width (float), and
          leaf length (float). """
     def __init__(self, angle, area, width, length):
          self.__angle = angle
          self.__area = area
          self.__width = width
          self.__length = length 
     
     def getAngle(self):
          return self.__angle
     def getArea(self):
          return self.__area
     def getWidth(self):
          return self.__width
     def getLength(self):
          return self.__length

class Stem:
     """The Stem constructor expects the stem diameter (float) and stem length (float). """
     def __init__(self, diameter, length):
          self.__diameter = diameter
          self.__length = length 
     
     def getDiameter(self):
          return self.__diameter
     def getLength(self):
          return self.__length

###
# End classes corresponding to plant components
###


###
# Classes and functions corresponding to plot construction
###
class RILBoxPlotData:
     """RILBoxPlotData contains many lists of data that can be plotted as box plots using matplotlib.boxplot().
          The constructor expects a list of Individuals (list) and the genotype ID of the individuals to plot (integer; either 63 or 73).
          The constructor then parses that information to the plottable lists."""
     def __init__(self, list_individuals, genotype_ID):
          # Populate box plot data by genotype ID (either 63 or 73):
          self.__list_dry_weight = []
          self.__list_height = []
          self.__list_number_phytomers = []
          self.__list_dry_weight_per_height = []
          for index_ind in range(0,len(list_individuals)):
               if int(list_individuals[index_ind].getGenotype()) == int(genotype_ID):
                    self.__list_dry_weight.append(float(list_individuals[index_ind].getDryWeight()))
                    self.__list_height.append(2.54*float(list_individuals[index_ind].getHeight()))
                    self.__list_number_phytomers.append(float(list_individuals[index_ind].getNumberPhytomers()))
                    self.__list_dry_weight_per_height.append((1.0/2.54)*float(list_individuals[index_ind].getDryWeightPerHeight()))
               else :
                    sys.stderr.write("Not using data corresponding to alternate genotype ID. \n")
          
          # Populate box plot data by phytomer:
          self.__list_leaf_angle = []
          self.__list_leaf_width = []
          self.__list_leaf_length = []
          self.__list_leaf_area = []
          self.__list_stem_length = []
          self.__list_stem_diameter = []
          # Find the maximum number of phytomers that any plant will have for plotting purposes.
          max_phytomers = 0     
          for index_ind in range(0,len(list_individuals)):
               if int(list_individuals[index_ind].getNumberPhytomers()) > max_phytomers :
                    max_phytomers = int(list_individuals[index_ind].getNumberPhytomers())
          # For each Phytomer, populate data lists for the Phytomer using data from the Individuals with the specified genotypeID.
          for index_phytomer in range(0,max_phytomers):
               list_single_phytomer_leaf_angle = []
               list_single_phytomer_leaf_width = []
               list_single_phytomer_leaf_length = []
               list_single_phytomer_leaf_area = []
               list_single_phytomer_stem_length = []
               list_single_phytomer_stem_diameter = []
               for index_ind in range(0,len(list_individuals)):
                    if int(list_individuals[index_ind].getGenotype()) == int(genotype_ID):
                         if list_individuals[index_ind].getNumberPhytomers() > index_phytomer:
                              list_single_phytomer_leaf_angle.append(float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getLeaf()).getAngle()))
                              list_single_phytomer_leaf_width.append(float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getLeaf()).getWidth()))
                              list_single_phytomer_leaf_length.append(float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getLeaf()).getLength()))
                              list_single_phytomer_leaf_area.append(float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getLeaf()).getArea()))
                         # Phytomers have one less stem than they do leaves.
                         if list_individuals[index_ind].getNumberPhytomers() - 1 > index_phytomer:
                              list_single_phytomer_stem_length.append(2.54*float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getStem()).getLength()))
                              list_single_phytomer_stem_diameter.append((1.0/10.0)*float((((list_individuals[index_ind].getPhytomers())[index_phytomer]).getStem()).getDiameter()))     
                         else :
                              sys.stderr.write("No more phytomers on individual. \n")     
                    else:
                         sys.stderr.write("Not used genotypeID. \n")
               self.__list_leaf_angle.append(list_single_phytomer_leaf_angle)
               self.__list_leaf_width.append(list_single_phytomer_leaf_width)
               self.__list_leaf_length.append(list_single_phytomer_leaf_length)
               self.__list_leaf_area.append(list_single_phytomer_leaf_area)
               self.__list_stem_length.append(list_single_phytomer_stem_length)
               self.__list_stem_diameter.append(list_single_phytomer_stem_diameter)
     # End RILBoxPlotData constructor

     def getDryWeight(self):
          return self.__list_dry_weight
     def getHeight(self):
          return self.__list_height
     def getNumberPhytomers(self):
          return self.__list_number_phytomers
     def getDryWeightPerHeight(self):
          return self.__list_dry_weight_per_height

     def getLeafAngle(self):
          return self.__list_leaf_angle
     def getLeafArea(self):
          return self.__list_leaf_area
     def getLeafWidth(self):
          return self.__list_leaf_width
     def getLeafLength(self):
          return self.__list_leaf_length
     def getStemDiameter(self):
          return self.__list_stem_diameter
     def getStemLength(self):
          return self.__list_stem_length

# Writes a boxplot to the canvas given a np array and integer ID. This function
# is used for plotting data from Individual objects.
def BoxPlotGenotype(input_data_to_plot, genotype_ID):
     if int(genotype_ID) == 63:
          color = "#4169E1"
          position_genotype = [0.2]
     elif int(genotype_ID) == 73:
          color = "#FF8C00"
          position_genotype = [0.4]
     plot = plt.boxplot(input_data_to_plot, positions=position_genotype, sym='bo')
     plt.setp(plot['medians'], color='black', linewidth=3)
     plt.setp(plot['boxes'], color=color, linewidth=4)
     plt.setp(plot['fliers'], color=color, linewidth=4, alpha=0.7)
     plt.setp(plot['whiskers'], ls= '-', color=color, linewidth=4)
     plt.setp(plot['caps'], color=color, linewidth=4)

# Writes a boxplot to the canvas given a np array and integer ID. This function
# is used for plotting data from Phytomer objects.
def BoxPlotPhytomer(input_data_to_plot, genotype_ID):
     if int(genotype_ID) == 63:
               color = "#4169E1"
     elif int(genotype_ID) == 73:
               color = "#FF8C00"
     plot = plt.boxplot(input_data_to_plot, sym='bo')
     plt.setp(plot['medians'], color='black', linewidth=1)
     plt.setp(plot['boxes'], color=color, linewidth=2)
     plt.setp(plot['fliers'], color=color, linewidth=2, alpha=0.7)
     plt.setp(plot['whiskers'], ls= '-', color=color, linewidth=2)
     plt.setp(plot['caps'], color=color, linewidth=2)

###
# End classes and functions corresponding to plot construction
###


###
# Utility functions
###
def usage():
     sys.stderr.write("\nExample usage:\n\tplot_boxplots_metadata_x_genotype.py R07018xR07020_RIL_metrics.csv\n\n")
     sys.stderr.flush()
     sys.exit()

###
# End utility functions
###


###
# Begin main()
###
if len(sys.argv) <= 1:
     usage()
if sys.argv[1] == "--help" or sys.argv[1] == "-h":
     usage()

# Read input file to global list of lists.
try:
     LILI_TABLE = [line.strip() for line in open(sys.argv[1])]
     LILI_TABLE = [element.split(',') for element in LILI_TABLE]
except IOError:
     sys.stderr.write("\nCannot open target file. Please check your input.")
     usage()

# Populate a list of Individuals with their data.
list_individuals = []
index_individual = 0
for index_row in range(1, len(LILI_TABLE)):
     # The first row doesn't have a preceding row to compare against, so it initializes the first Individual
     if index_row == 1:
          list_individuals.append(Individual(LILI_TABLE[index_row][INDEX_COLUMN_RIL], 
                                                   LILI_TABLE[index_row][INDEX_COLUMN_RIL_DRY_WEIGHT],
                                                   LILI_TABLE[index_row][INDEX_COLUMN_RIL_HEIGHT])) 
     # Each Individual has multiple sequential rows of Phytomer data that share the same replicate column ID.
     # This checks replicate column ID and creates a new Individual when finished processing the preceding Individual.
     elif (LILI_TABLE[index_row][INDEX_COLUMN_REP] != LILI_TABLE[index_row-1][INDEX_COLUMN_REP]):
          list_individuals.append(Individual(LILI_TABLE[index_row][INDEX_COLUMN_RIL], 
                                                   LILI_TABLE[index_row][INDEX_COLUMN_RIL_DRY_WEIGHT],
                                                   LILI_TABLE[index_row][INDEX_COLUMN_RIL_HEIGHT]))
          index_individual = index_individual + 1 
     # Default behavior means the current row corresponds to the same Individual as the preceding row.     
     else:
          sys.stdout.write("Processing the same Individual.\n")
          sys.stdout.flush()

     # Each row always contains Phytomer data, so the data gets stored in a Phytomer object and added to 
     #      its corresponding Individual.
     current_phytomer = Phytomer(LILI_TABLE[index_row][INDEX_COLUMN_LEAF_NUMBER])
     current_phytomer.makeLeaf(Leaf(LILI_TABLE[index_row][INDEX_COLUMN_ANGLE], 
                                       LILI_TABLE[index_row][INDEX_COLUMN_AREA],
                                       LILI_TABLE[index_row][INDEX_COLUMN_AVG_WIDTH],
                                       LILI_TABLE[index_row][INDEX_COLUMN_LENGTH]))
     current_phytomer.makeStem(Stem(LILI_TABLE[index_row][INDEX_COLUMN_STEM_DIAMETER], 
                                       LILI_TABLE[index_row][INDEX_COLUMN_STEM_LENGTH]))
     list_individuals[index_individual].addPhytomer(current_phytomer)

###
# Plotting all of the data
###
# Set up Plotting parameters
plot_rows = 8
plot_columns = 4
fig = plt.figure(figsize=(30*(2.0/3.0),25*(2.0/3.0)))

###### Plot phytomer characteristics against phytomers

# Leaf Angle
plt.subplot2grid((plot_rows,plot_columns),(0, 0), rowspan=3, colspan=3)
plt.ylabel('leaf inclination angle ($^{o}$)')
plt.ylim([0,100])
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getLeafAngle(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getLeafAngle(), 73)

# Leaf Width
plt.subplot2grid((plot_rows,plot_columns),(3, 0), rowspan=1, colspan=3)
plt.ylabel('leaf width ($cm$)')
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getLeafWidth(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getLeafWidth(), 73)

# Leaf Length
plt.subplot2grid((plot_rows,plot_columns),(4, 0), rowspan=1, colspan=3)
plt.ylabel('leaf length ($cm$)')
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getLeafLength(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getLeafLength(), 73)

# Leaf Area
plt.subplot2grid((plot_rows,plot_columns),(5, 0), rowspan=1, colspan=3)
plt.ylabel('leaf area ($cm^{2}$)')
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getLeafArea(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getLeafArea(), 73)

# Stem Diameter
plt.subplot2grid((plot_rows,plot_columns),(6, 0), rowspan=1, colspan=3)
plt.ylabel('diameter ($cm$)')
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getStemDiameter(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getStemDiameter(), 73)

# Stem Length
plt.subplot2grid((plot_rows,plot_columns),(7, 0), rowspan=1, colspan=3)
plt.ylabel('length ($cm$)')
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 63).getStemLength(), 63)
BoxPlotPhytomer(RILBoxPlotData(list_individuals, 73).getStemLength(), 73)
plt.xlabel('phytomers')

###### Plot Individual characteristics against Individuals

# dry weight
plt.subplot2grid((plot_rows,plot_columns),(0, 3), rowspan=2, colspan=1)
plt.ylabel('dry weight ($g$)')
plt.ylim([75,210])
BoxPlotGenotype(RILBoxPlotData(list_individuals, 63).getDryWeight(), 63)
BoxPlotGenotype(RILBoxPlotData(list_individuals, 73).getDryWeight(), 73)
plt.xticks([0.20,0.40],  ('', '') )
plt.xlim([0.1,0.5])

# height
plt.subplot2grid((plot_rows,plot_columns),(2, 3), rowspan=2, colspan=1)
plt.ylabel('height ($cm$)')
BoxPlotGenotype(RILBoxPlotData(list_individuals, 63).getHeight(), 63)
BoxPlotGenotype(RILBoxPlotData(list_individuals, 73).getHeight(), 73)
plt.xticks([0.2,0.40],  ('', '') )
plt.xlim([0.1,0.5])

# number of phytomers
plt.subplot2grid((plot_rows,plot_columns),(4, 3), rowspan=2, colspan=1)
plt.ylabel('# of phytomers')
plt.ylim([6,13])
BoxPlotGenotype(RILBoxPlotData(list_individuals, 63).getNumberPhytomers(), 63)
BoxPlotGenotype(RILBoxPlotData(list_individuals, 73).getNumberPhytomers(), 73)
plt.xticks([0.2,0.40],  ('', '') )
plt.xlim([0.1,0.5])

# dry_weight/height
plt.subplot2grid((plot_rows,plot_columns),(6, 3), rowspan=2, colspan=1)
plt.ylabel('dry weight per height (g/cm)')
BoxPlotGenotype(RILBoxPlotData(list_individuals, 63).getDryWeightPerHeight(), 63)
BoxPlotGenotype(RILBoxPlotData(list_individuals, 73).getDryWeightPerHeight(), 73)
plt.xticks([0.20,0.40],  ('RIL 63', 'RIL 73'))
plt.xlim([0.1,0.5])
plt.xlabel('genotypes')

# Write plot to file
plt.savefig("Meta_RIL63_RIL73.png", dpi=900, format="png")

###
# End plotting all of the data
###

###
# End main()
###
