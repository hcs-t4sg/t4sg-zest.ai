import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings(action='once')
import datetime as dt
import os, re, sys
from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
from xgboost import XGBClassifier
import zrp_feature_engineering

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


def generatePredictions(data):
    bpp = Basic_PreProcessor()
    sample_data_transform_0 = bpp.transform(data)
    zrp_fe = pd.read_pickle(r'/code/picklefiles/zrp_fe_pkl.obj')
    sample_data_transform_1 = zrp_fe.transform(sample_data_transform_0)
    zrp_model = pd.read_pickle(r'/code/picklefiles/clf_fl.obj')
    zrp_result_probs = np.round(zrp_model.predict_proba(sample_data_transform_1),3)
    return zrp_result_probs