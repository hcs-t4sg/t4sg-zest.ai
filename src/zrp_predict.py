import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings(action='once')
import datetime as dt
import os, re, sys
from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
from xgboost import XGBClassifier
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


class ZRPFeatureEngineering():
    '''This class is used to execute general ZRP feature engineering.''' 
    
    def __init__(self):
        
        # label encode via target
        self.label_encoded_columns = ['Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split']
  
        # ordinal encoding
        self.ordinal_encoded_columns = ['Gender', 'County_Code']
        self.oe = OrdinalEncoder()

        # numerical columns (categories, but let the tree figure it out...)
        self.numerical_columns =  ['Congressional_District', 'Senate_District', 'House_District']
        
        # dates
        self.date_columns = ['Birth_Date']


    def _process_target(self, y):                
        y_unique = y.unique()
        y_unique.sort()
        self.n_classes = len(y_unique)

        census_code_mapping = {1: 'AI', 2: 'API', 3: 'Black', 4: 'Hispanic', 5: 'White', 6: 'Other', 7: 'Multi', 9: 'Unknown'}

        # handle multi-labeled output
        self.mlb = MultiLabelBinarizer(classes = y_unique)
        self.mlb_columns = [census_code_mapping[x] for x in y_unique]
        
        self.mlb.fit(y.values.reshape(-1,1))
        y_ohe = pd.DataFrame(self.mlb.transform(y.values.reshape(-1,1)), columns=self.mlb_columns)

        self.le = {}
        for i in range(self.n_classes):
            self.le[i] = TargetEncoder()

        return y_ohe
    
    def fit(self, X, y):
        
        X = X.reset_index(drop=True)
        y = y.reset_index(drop=True)        
        
        y_ohe = self._process_target(y)
        
        # fit label encoded columns
        for i in range(self.n_classes):
            self.le[i].fit(X[self.label_encoded_columns], y_ohe.iloc[:,i])

        # fit ordinal columns
        self.oe.fit(X[self.ordinal_encoded_columns]) 
        

        return self
    
    def transform(self, X):

        X = X.reset_index(drop=True)
        
        # handle missing gender
        X[['Gender']] = X[['Gender']].replace(to_replace='nan', value='U')
        
        # transform X
        X_date_convert = X[self.date_columns].apply(pd.to_datetime, errors='coerce')
        X_date_convert = X_date_convert[self.date_columns].apply(lambda x: getattr(pd.DatetimeIndex(x),'year'))
  
        X_fe = pd.concat([self.le[i].transform(X[self.label_encoded_columns]) for i in range(self.n_classes)],
                         axis=1, sort=False
                        )

        X_fe = pd.concat([X_fe,
                          pd.DataFrame(self.oe.transform(X[self.ordinal_encoded_columns])),
                          X_date_convert[self.date_columns],
                          X[self.numerical_columns]
                         ], axis=1, sort=False)
    
        label_encoded_colname = []
        for label in self.mlb_columns:
            for col in self.label_encoded_columns:
                label_encoded_colname.append(label+'_'+col)

        X_fe.columns = label_encoded_colname + self.ordinal_encoded_columns + self.date_columns + self.numerical_columns

        return X_fe

def generatePredictions(data):
    bpp = Basic_PreProcessor()
    sample_data_transform_0 = bpp.transform(data)
    zrp_fe = pd.read_pickle(r'../picklefiles/zrp_feature_engineering.obj')
    sample_data_transform_1 = zrp_fe.transform(sample_data_transform_0)
    zrp_model = pd.read_pickle(r'../picklefiles/clf-all-fl-30pct-sample.obj')
    zrp_result_probs = np.round(zrp_model.predict_proba(sample_data_transform_1),3)
    return zrp_result_probs