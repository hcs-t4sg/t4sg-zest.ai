import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings(action='once')
import datetime as dt
import os, re, sys
sys.path.append('../')
import pickle

from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
from xgboost import XGBClassifier

sample_in = pd.read_csv('/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai-data/ZRP_FL_30_pct/sample_data.csv')
sample_in.head()
sample_in['Precinct_Split'][0]

sample_in['Race'].value_counts()

data = {'Name_First': ['George'], 'Name_Last': ['Chambers'], 'Name_Middle': ['William'], 'Zipcode': [34293], 'Precinct_Split': ['NaN'], 'Gender': ['M'], 'County_Code': ['SAR'], 'Congressional_District':[17.0], 'Senate_District': [23.0], 'House_District': [74.0], 'Birth_Date': ['12/02/1951']}
sample_2 = pd.DataFrame(data)
sample_2.head()


required_cols = ['Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split','Gender', 'County_Code','Congressional_District', 'Senate_District', 'House_District', 'Birth_Date']
sample_data = sample_in.copy()
sample_data = sample_data[required_cols]
sample_data.head()


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
        self.n_classes = 9
        self.le = {}
        for i in range(self.n_classes):
            self.le[i] = TargetEncoder()
        
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

opt_params = {'gamma': 1.410542602972238,
              'lambda': 14.733034116863823,
              'learning_rate': 0.018600037053769385,
              'max_depth': 5,
              'min_child_weight': 1492,
              'n_estimators': 1125,
              'subsample': 0.878175668041017}


bpp = Basic_PreProcessor()
sample_data_transform_0 = bpp.transform(sample_2)
sample_data_transform_0.head()

#zrp_fe = pd.read_pickle(r'/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai-data/ZRP_FL_30_pct/zrp_feature_engineering.obj')

if __name__ == "__main__":
    # code for standalone use
    zrp_fe = pd.read_pickle(r'/Users/rakeshnori/Desktop/2020-21 School Year/Clubs/T4SG/Zest/t4sg-zest.ai-data/ZRP_FL_30_pct/zrp_feature_engineering.obj')
    ZRPFeatureEngineering.__module__ = "zrp_predict_flask"
    Basic_PreProcessor.__module__ = "zrp_predict_flask"
    zrp_fe.__class__ = ZRPFeatureEngineering
    with open("zrp_fe.obj") as f:
    	pickle.dump(zrp_fe, f)
