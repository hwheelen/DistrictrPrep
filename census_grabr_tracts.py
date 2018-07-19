#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 18:30:41 2018

@author: hannah
"""
import requests
import pandas as pd
from pprint import pprint

# constants
CENSUS_API_KEY = "YOUR_KEY_HERE"
HOST = "https://api.census.gov/data"

#set year for data and acs5 or sf1
year = "2010"
dataset = "sf1"
base_url = "/".join([HOST, year, dataset])

#p5_vars = ["P005" + str(i + 1).zfill(4) for i in range(17)]
#get_vars = ["NAME"] + p5_vars #link to sf1 vars https://api.census.gov/data/2010/sf1/variables.html
get_vars = ["NAME", "P0050001", "P0050003", "P0050004", "P0050005", "P0050006", "P0040003"]
#["NAME", "P0050001", "P0050003", "P0050004", "P0050005", "P0050006", "P0040003"]

data = []
#loop over the 67 counties in PA
for i in range(1,291): 
    predicates = {}         
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "tract:*"
    #state fips code, here 42 is Pennsylvania 
    predicates["in"] = "state:02+county:"+str(i)
    predicates["key"] = CENSUS_API_KEY

# Write the result to a response object:
    response = requests.get(base_url, params=predicates)
    try:
        col_names = response.json()[0]
        data = data + response.json()[1:]
    except :
        print(response.url)

census_df = pd.DataFrame(columns=col_names, data=data)
census_df.set_index(["state", "county", "tract"], drop=False, inplace=True)

census_df['geoid'] = census_df['state'].astype(str) + census_df['county'].astype(str) + census_df['tract'].astype(str)

census_df.to_csv("AK_tract.csv")
