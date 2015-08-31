from openalea.file.files import *
from openalea.lpy_wralea.lpy_nodes import *
from alinea.adel.lpy2mtg import *
from alinea.adel.stand.stand import *
from alinea.adel.io.io import *
from alinea.adel.mtg import *
from alinea.adel.stand.CanMTGPlanter import *
from alinea.caribu.mtg import *
from alinea.caribu.CaribuScene import *
from alinea.caribu.ScatteringOptions import *
from alinea.caribu.vcaribu import *
from alinea.caribu.vcaribu_adaptor import *
from alinea.caribu.vcaribuOut_adaptor import *
from alinea.caribu.visualisation.gammaTrans import *
from openalea.color.py_color import *
from openalea.functional.functional import *
from alinea.caribu.selectOutput import *
from alinea.caribu.WriteCan import *
from alinea.caribu.visualisation.py_canview import *
from PyQt4 import QtGui, QtCore
from openalea.core.logger import *
from alinea.adel.wheat.Write_Table import *
import pickle
app = QtGui.QApplication([])
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
str_angle = sys.argv[1]
str_date = sys.argv[2]
str_time = sys.argv[3]
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Read in .lpy Lsystem
lpy_filenamepath = "/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/lsystems/" + str_angle + ".lpy"
lpy_File = file(lpy_filenamepath)
lpy_FileRead = FileRead()
lpy_FileRead.read_contents(lpy_File)

# Read in light file
light_filenamepath = "/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/light_files/" + str_date + "/" + str_time + ".light"
lightFile = file(light_filenamepath)
lightString = FileRead()
lightString.read_contents(lightFile)

# Read in par file
optFile = file("/usr/lib/python2.7/dist-packages/alinea/caribu/data/par4.opt")
optString = FileRead()
optString.read_contents(optFile)

# Read in caribu output file
caribu_filenamepath ="/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/caribu_out/" + str_date + "/" + str_angle + "/" + str_time +"_caribu.ssv"
caribu_outFile = file(caribu_filenamepath)

# Read in plant positions output file
plantpositions_filenamepath = "/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/caribu_out/" + str_date + "/" + str_angle + "/" + str_time + "_plant_positions"
plantpositions_outFile = file(plantpositions_filenamepath)


lSystem = lsystem(lpy_FileRead.s)

newLSystemIterate, newRunLSystem = run(lSystem)

newMTG = lpy2mtg(newLSystemIterate, newRunLSystem)

# parameter for agronomic plotting
# These parameters reflect planting of sorghum in fields as previously described in Olson
# et al (2013).
plot_length_meters = 3.048
plot_width_meters = 3.04
plot_sowing_density = 13.20
plot_plant_density = 13.20
plot_inter_row =  0.76
plot_noise =  50.0  # this parameter is just a guess
plot_convunit = 1.0

splot_n_emerged, splot_positions, splot_domain, splot_density = agronomicplot(plot_length_meters,
                                                                              plot_width_meters,
                                                                              plot_sowing_density,
                                                                              plot_plant_density,
                                                                              plot_inter_row,
                                                                              plot_noise,
                                                                              plot_convunit)

plantpositions_outFile = open(plantpositions_filenamepath, 'w')
plantpositions_outFile.write("\n".join('%s %s %s' %x for x in splot_positions))
plantpositions_outFile.close()

duplicatedMTG = duplicate(newMTG, splot_n_emerged)

canestraDupMTG=CanMTGPlanter(duplicatedMTG, splot_positions, random_seed=0, azimuths=None)

canestra_id, canestra_contents = to_canestra(canestraDupMTG[0],
                                             OptId = "optical_specie",
                                             Opak = "transparency",
                                             Geometry = "geometry",
                                             defopt = 1,
                                             defopak = 0,
                                             epsilon=1e-5)

ObjCaribuScene = newObjCaribuScene(scene_obj=canestra_contents,
                                ligth_string=lightString.s,
                                pattern_tuple=None,
                                opt_string=optString.s,
                                waveLength=None)

No_Multiple_Scattering = True
Nz = 5
SphereDiameter = 0.5
Zmax = 2

scene, lightsources, opticals, pattern, optiondict = vcaribu_adaptor(ObjCaribuScene,
                                                                     No_Multiple_Scattering,
                                                                     Nz,
                                                                     Zmax,
                                                                     SphereDiameter)


irradiances, status = vcaribu(scene, lightsources, opticals, pattern, optiondict)

godict = vcaribuOut_adaptor(irradiances)

Write_Table(Table = godict,
            filename = caribu_filenamepath,
            first = True)
