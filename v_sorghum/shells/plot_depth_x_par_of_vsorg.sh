#!/bin/bash
############
# bash script to plot eabs from two sorghum plots (varying in leaf angle)
# Written by Sandra Truong
# 10/24/2014

# smallangle R07018xR07020_63
STR_SMALL_ANGLE="R07018xR07020_63"
#STR_SMALL_ANGLE="smallangle_whorl"
#STR_SMALL_ANGLE="smallangle_nowhorl"
# largeangle R07018xR07020_73
STR_LARGE_ANGLE="R07018xR07020_73"
#STR_LARGE_ANGLE="largeangle_whorl"
#STR_LARGE_ANGLE="largeangle_nowhorl"
STR_DATE="July_22_2014"
#STR_DATE="July_04_2014"
#STR_DATE="June_15_2013"
STR_TIME="1530_20"

python_wrapper_caribu_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/scripts/openalea_wrapper.py
python_calculate_eabs_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/scripts/calculate_eabs.py
python_plot_eabs_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/scripts/plot_eabs_par_fit.py

# files
Lpy_SMALL_ANGLE_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/lsystems/${STR_SMALL_ANGLE}.lpy
if [ -a "${Lpy_SMALL_ANGLE_filenamepath}" ]
then
        echo -e "Lpy_SMALL_ANGLE_filenamepath exists"
else
        echo -e "\n\tUnable to locate Lpy_SMALL_ANGLE_filenamepath.\n\tPlease make sure the Lpy is in the appropriate directory.\n"
fi

Lpy_LARGE_ANGLE_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/lsystems/${STR_LARGE_ANGLE}.lpy
if [ -a "${Lpy_LARGE_ANGLE_filenamepath}" ]
then
        echo -e "Lpy_LARGE_ANGLE_filenamepath exists"
else
        echo -e "\n\tUnable to locate Lpy_LARGE_ANGLE_filenamepath.\n\tPlease make sure the Lpy is in the appropriate directory.\n"
fi

light_filenamepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/light_files/${STR_DATE}/${STR_TIME}.light
if [ -a "${light_filenamepath}" ]
then
        echo -e "light_filenamepath exists"
else
        echo -e "\n\tUnable to locate light_filenamepath.\n\tPlease make sure the light file is in the appropriate directory.\n"
fi

# file paths
caribu_output_filepath=/home/skt/Documents/LeafAngle/manuscript_2014/vsorg/caribu_out/
if [ -d ${caribu_output_filepath} ]
then
        echo -e "caribu_output_filepath exists"
else
        echo -e "\n\tUnable to locate caribu_output_filepath. Creating directory...\n"
        mkdir ${caribu_output_filepath}
fi

caribu_date_filepath=${caribu_output_filepath}/${STR_DATE}/
if [ -d ${caribu_date_filepath} ]
then
        echo -e "caribu_date_filepath exists"
else
        echo -e "\n\tUnable to locate caribu_date_filepath. Creating directory...\n"
        mkdir ${caribu_date_filepath}
fi

caribu_small_filepath=${caribu_date_filepath}/${STR_SMALL_ANGLE}/
if [ -d ${caribu_small_filepath} ]
then
        echo -e "caribu_small_filepath exists"
else
        echo -e "\n\tUnable to locate caribu_small_filepath. Creating directory...\n"
        mkdir ${caribu_small_filepath}
fi

caribu_large_filepath=${caribu_date_filepath}/${STR_LARGE_ANGLE}/
if [ -d ${caribu_large_filepath} ]
then
        echo -e "caribu_large_filepath exists"
else
        echo -e "\n\tUnable to locate caribu_large_filepath. Creating directory...\n"
        mkdir ${caribu_large_filepath}
fi

caribu_small_filenamepath=${caribu_small_filepath}/${STR_TIME}_caribu.ssv
if [ -a ${caribu_small_filenamepath} ]
then
        echo -e "caribu_small_filenamepath exists"
else
        echo -e "\n\tUnable to locate caribu_small_filenamepath. Creating file...\n"
        touch ${caribu_small_filenamepath}
fi

caribu_large_filenamepath=${caribu_large_filepath}/${STR_TIME}_caribu.ssv
if [ -a ${caribu_large_filenamepath} ]
then
        echo -e "caribu_large_filenamepath exists"
else
        echo -e "\n\tUnable to locate caribu_large_filenamepath. Creating file...\n"
        touch ${caribu_large_filenamepath}
fi

pp_small_filenamepath=${caribu_small_filepath}/${STR_TIME}_plant_positions
if [ -a ${pp_small_filenamepath} ]
then
        echo -e "pp_small_filenamepath exists"
else
        echo -e "\n\tUnable to locate pp_small_filenamepath. Creating file...\n"
        touch ${pp_small_filenamepath}
fi

pp_large_filenamepath=${caribu_large_filepath}/${STR_TIME}_plant_positions
if [ -a ${pp_large_filenamepath} ]
then
        echo -e "pp_large_filenamepath exists"
else
        echo -e "\n\tUnable to locate pp_large_filenamepath. Creating file...\n"
        touch ${pp_large_filenamepath}
fi

# python scripts!
python ${python_wrapper_caribu_filenamepath} ${STR_SMALL_ANGLE} ${STR_DATE} ${STR_TIME}
python ${python_calculate_eabs_filenamepath} ${caribu_small_filenamepath} > ${caribu_small_filepath}${STR_TIME}_eabs


python ${python_wrapper_caribu_filenamepath} ${STR_LARGE_ANGLE} ${STR_DATE} ${STR_TIME}
python ${python_calculate_eabs_filenamepath} ${caribu_large_filenamepath} > ${caribu_large_filepath}${STR_TIME}_eabs

python ${python_plot_eabs_filenamepath} ${caribu_small_filepath}${STR_TIME}_eabs ${pp_small_filenamepath} ${caribu_large_filepath}${STR_TIME}_eabs ${pp_large_filenamepath}

