# -*- coding: utf-8 -*-
"""
@authors: zach, assaf, lee

For the given state FIPS codes, downloads the shapefiles for Census 2010 blocks, block groups, and tracts.
Shapefiles are joined with Census 2010 population data at each level and placed in the correspodning state FIP folder. 

"""

import os

import geopandas as gpd
import pandas as pd

from urllib.request import urlopen
from zipfile import ZipFile


# Data retrieval
def get_and_unzip(url, data_dir=os.getcwd()):
    basename = url.split("/")[-1]
    name_with_path = os.path.join(data_dir, basename)
    if not os.path.exists(name_with_path):
        file_data = urlopen(url)
        data_to_write = file_data.read()
        with open(name_with_path, "wb") as f:
            f.write(data_to_write)

        zip_obj = ZipFile(name_with_path)
        zip_obj.extractall(data_dir)
        del(zip_obj)


# State FIPS codes - specify here your state(s) of interest
fips = ["36"]

#Change directory to tigerline folder
os.chdir("./tigerline")

#Iterate through each state fips code
for fip in fips:

    #TRACTS
    url_tract = "https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_" + fip + "_tract10.zip"    #2010 tigerline tracts shapefile
    get_and_unzip(url_tract,os.getcwd())                                                                    #download shapefile from census and unzip
    shp_tracts = gpd.read_file("tl_2010_" + fip + "_tract10.shp")                                           #read shapefile into geo dataframe
    os.chdir("../states/" + fip)                                                                            #directory = state folder
    pop_tracts = pd.read_csv("2010_" + fip + "_tract_poptable.csv", dtype={"GEOID10": str})                 #read pop csv into dataframe
    tracts = pd.merge(shp_tracts, pop_tracts, on="GEOID10")                                                 #merge pop + shapefile
    tracts.to_file(driver='ESRI Shapefile',filename='2010_' + fip + '_tract_pop.shp')                       #save final shapefile
    os.chdir("..")                                                                                          
    os.chdir("..")                                                                                  
    os.chdir("tigerline")                                                                                   #directory = tigerline

    #BLOCKS
    url_block = "https://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2010/tl_2010_" + fip + "_tabblock10.zip"  #2010 tigerline blocks shapefile
    get_and_unzip(url_block,os.getcwd())
    #shp_blocks = gpd.read_file("tl_2010_" + fip + "_block10.shp")
    shp_blocks = gpd.read_file("tl_2010_" + fip + "_tabblock10.shp")
    os.chdir("../states/" + fip)
    pop_blocks = pd.read_csv("2010_" + fip + "_tabblock_poptable.csv", dtype={"GEOID10": str})
    blocks = pd.merge(shp_blocks, pop_blocks, on="GEOID10")
    blocks.to_file(driver='ESRI Shapefile',filename='2010_' + fip + '_tabblock_pop.shp')
    os.chdir("..")
    os.chdir("..")
    os.chdir("tigerline") 
    
    #BLOCK GROUPS
    url_bg = "https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/tl_2010_" + fip + "_bg10.zip"             #2010 tigerline block groups shapefile
    get_and_unzip(url_bg,os.getcwd())
    shp_bgs = gpd.read_file("tl_2010_" + fip + "_bg10.shp")
    os.chdir("../states/" + fip)
    pop_bgs = pd.read_csv("2010_" + fip + "_bg_poptable.csv", dtype={"GEOID10": str})
    bgs = pd.merge(shp_bgs, pop_bgs, on="GEOID10")
    bgs.to_file(driver='ESRI Shapefile',filename='2010_' + fip + '_bg_pop.shp')
    os.chdir("..")
    os.chdir("..")
    os.chdir("tigerline")
