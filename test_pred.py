import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings(action='once')
import datetime as dt
import os, re, sys
sys.path.append('../')
import pickle
sys.path.append('/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai/src/')
from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
import zrp_feature_engineering_NC

sys.path.append('/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai/src/')
import zrp_feature_engineering_NC

from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
from xgboost import XGBClassifier


data = {'Name_First': ['Lindsey'], 'Name_Last': ['Powell'], 'Name_Middle': ['Deitz'], 'Zipcode': ['27017'], 'Precinct_Split': ['29.0'], 'Gender': ['F'], 'County_Code': ['86.0'], 'Congressional_District':[10.0], 'Senate_District': [45.0], 'House_District': [90.0], 'Birth_Date': ['1/5/1983']}
sample_2 = pd.DataFrame(data)
sample_2.head()

class Basic_PreProcessor():
    '''This class is used to execute general ZRP preprocessing. This is an example class requiring access to the proxy_fe.py script & functions. 
    ''' 

    def __init__(self):
        pass
    def fit(self):
        pass
    def transform(self, data):
        from proxy_fe import fl_address_clean
        from proxy_fe import lower_case
        from proxy_fe import handle_compounds
        
#         # create id
#         data["applicant_id"] =  data.index
        
        data_fl_co_all_sample_clean = data.copy()

        # clean address information
        data_fl_co_all_sample_clean['Zipcode'] = data_fl_co_all_sample_clean['Zipcode'].astype(str).str.extract(r"(^\d{5})").astype(str)

        # handle dashes and spaces
        data_fl_co_all_sample_clean['Name_Last'] = data_fl_co_all_sample_clean['Name_Last'].str.replace('-', ' ') # replace dashes with spaces
        data_fl_co_all_sample_clean['Name_Last'] = data_fl_co_all_sample_clean['Name_Last'].str.replace(' +', ' ') # replace double spaces with single spaces

        # handle casing
        data_fl_co_all_sample_clean = lower_case(data_fl_co_all_sample_clean, ['Name_Last', 'Name_First', 'Name_Middle']) 

        # compound names (row indicies are not preserved!)
        # data_fl_co_all_sample_clean = handle_compounds(data_fl_co_all_sample_clean)
        return(data_fl_co_all_sample_clean)

bpp = Basic_PreProcessor()
sample_data_transform_0 = bpp.transform(sample_2)
sample_data_transform_0.head()
print(sample_data_transform_0['Name_First'], file=sys.stdout)
print(sample_data_transform_0['Name_Last'], file=sys.stdout)
print(sample_data_transform_0['Name_Middle'], file=sys.stdout)
print(sample_data_transform_0['Zipcode'], file=sys.stdout)
print(sample_data_transform_0['Precinct_Split'], file=sys.stdout)
print(sample_data_transform_0['Gender'], file=sys.stdout)
print(sample_data_transform_0['County_Code'], file=sys.stdout)
print(sample_data_transform_0['Congressional_District'], file=sys.stdout)
print(sample_data_transform_0['Senate_District'], file=sys.stdout)
print(sample_data_transform_0['House_District'], file=sys.stdout)
print(sample_data_transform_0['Birth_Date'], file=sys.stdout)

from zrp_feature_engineering_NC import ZRPFeatureEngineeringNC
zrp_fe = pd.read_pickle(r'/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai/picklefiles/zrp_fe_nc.obj')

sample_data_transform_1 = zrp_fe.transform(sample_data_transform_0)
print(sample_data_transform_1.head())

zrp_model = pd.read_pickle(r'/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai/picklefiles/clf-nc-5pct.obj')

zrp_result = zrp_model.predict(sample_data_transform_1)
print(zrp_result)

zrp_result_probs = np.round(zrp_model.predict_proba(sample_data_transform_1),3)
print(zrp_result_probs)