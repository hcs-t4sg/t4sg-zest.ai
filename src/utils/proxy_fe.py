import pandas as pd
import numpy as np
import math
import time
import sys
import re
import os
from collections import Counter
# Geocoding modules
# import geopandas
# import censusbatchgeocoder as cbg
# import censusgeocode as cg 



################################################################



def fl_address_clean(app_data, streetaddress, city, state, zipcode):
    """Clean addresses by removing additional whitespace and converting all strings to lowercase.
        streetaddress: series
        city: series 
        state: series 
        zipcode: series"""
    app_data[streetaddress] = app_data[streetaddress].str.lower().str.strip()
    app_data[city] = app_data[city].str.lower().str.strip()
    app_data[state] = app_data[state].str.lower().str.strip()
    app_data[zipcode] = app_data[zipcode].astype(str).str.extract(r"(^\d{5})").astype(str)
    return app_data  
########################################################

def lower_case(data, columns):
    """Convert strings in the Series to lowercase.
        data: dataframe
        columns: list"""
    for col in columns:
        data[col] = data[col].str.lower()
    return data
########################################################


def handle_compounds(data):
    """Simple compund surname handler. An individual with N names will receive a sample weight 1/n (where n = number of names). Additional preprocessing to normalize compound name format could be helpful.
        data: dataframe"""
    
    # add sample weight col
    data['sample_weight'] = 1.0
    
    # convert dashes and multi-spaces to single space
    data['Name_Last'] = data['Name_Last'].str.replace('-', ' ') # replace dashes with spaces
    data['Name_Last'] = data['Name_Last'].str.replace(' +', ' ') # replace double spaces with single spaces

    # split compounds from non_compounds
    compound_name_str_all = data['Name_Last'].str.split(' ', expand=True) # split on spaces
    non_compound = data[compound_name_str_all[1].isna()].copy().reset_index(drop=True)
    compound = data[~compound_name_str_all[1].isna()].copy().reset_index(drop=True)
        
    # focus on compound folks
    compound['sample_weight'] = -1.0 # set init condition
    compound_name_str = compound['Name_Last'].str.split(' ', expand=True) # split on spaces
    n_compounds = compound_name_str.shape[1] # max number of unique strings
    compound_name_int = compound_name_str.copy() # binary representation of string
    for col in compound_name_str.columns:
        compound_name_int[col] = (~compound_name_str[col].isna()).astype(int)
    compound_name_int['compound_count'] = np.sum(compound_name_int, axis=1) # count rowwise count of strings  
    compound_name_int['sample_weight'] = 1 / compound_name_int['compound_count'] # sample weight

    compound_tiled = compound.loc[compound.index.repeat(n_compounds)].reset_index(drop=True)
    sw_tiled = compound_name_int.loc[compound_name_int.index.repeat(n_compounds)].reset_index(drop=True)
    unrolled_names = (compound_name_str.values.ravel())
    
    compound_tiled['sample_weight'] = sw_tiled['sample_weight']
    compound_tiled['Name_Last'] = unrolled_names
    
    compound_result = compound_tiled[~compound_tiled['Name_Last'].isna()]

    joint_result = non_compound.append(compound_result).reset_index(drop=True)
    
    return joint_result
########################################################

    
 