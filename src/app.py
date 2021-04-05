from flask import Flask, request, session, jsonify, redirect, render_template
from flask_cors import CORS
import time

# Needed for surgeo route
import pandas as pd 
import surgeo
import pickle
import json

import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings(action='once')
import datetime as dt
import os, re, sys
from sklearn.preprocessing import MultiLabelBinarizer, OrdinalEncoder
from category_encoders import TargetEncoder
from xgboost import XGBClassifier
import zrp_predict
from zrp_predict import zrp_feature_engineering, Basic_PreProcessor


app = Flask(__name__)
CORS(app)

@app.route('/hello')
def say_hello_world():
    return {'result': "Flask says Hello World"}

def run_surgeo(surname, zipcode):
    # Returns the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}
    surname_series = pd.Series([surname])
    zip_series = pd.Series([zipcode])

    sg = surgeo.SurgeoModel()
    sg_results = sg.get_probabilities(surname_series, zip_series)

    sg_json = pd.DataFrame.to_json(sg_results)
    return(sg_json)

def zrp(zipcode, last_name, first_name, middle_name, precinct_split, gender, 
        county_code, congressional_district, senate_district, house_district, birth_date):
    # Returns the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}
    # Required fields: 'Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split','Gender', 
    # 'County_Code','Congressional_District', 'Senate_District', 'House_District', 'Birth_Date'

    data = {'Name_First': [str(first_name)], 
            'Name_Last': [str(last_name)],
            'Name_Middle': [str(middle_name)], 
            'Zipcode': [int(zipcode)], 
            'Precinct_Split': [str(precinct_split)], 
            'Gender': [str(gender)], 
            'County_Code': [str(county_code)], 
            'Congressional_District':[float(congressional_district)], 
            'Senate_District': [float(senate_district)], 
            'House_District': [float(house_district)], 
            'Birth_Date': [str(birth_date)]}
    
    sample = pd.DataFrame(data)
    preds = zrp_predict.generatePredictions(sample)


    preds_data = {'American Indian': str(preds[0][0]), 
                  'Asian Pacific Islander': str(preds[0][1]), 
                  'Black': str(preds[0][2]), 
                  'Hispanic': str(preds[0][3]), 
                  'White': str(preds[0][4]), 
                  'Other': str(preds[0][5]), 
                  'Multi': str(preds[0][6])}

    json_preds = json.dumps(preds_data)
    return json_preds

@app.route('/surgeo', methods=["GET", "POST"])
def internal_surgeo():
    # API for internal use and testing only; will be deprecated in the future
    # Required fields: 'surname', 'zipcode'

    surname = request.args.get('surname')
    zipcode = request.args.get('zipcode')
    return run_surgeo(surname=surname, 
                      zipcode=zipcode)

@app.route('/zrp', methods=["GET"])
def internal_zrp():
    # API for internal use and testing only; will be deprecated in the future
    # Required fields: 'Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split','Gender', 
    # 'County_Code','Congressional_District', 'Senate_District', 'House_District', 'Birth_Date'

    zipcode = request.args.get('zipcode')
    last_name = request.args.get('last_name')
    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')
    precinct_split = request.args.get('precinct_split')
    gender = request.args.get('gender')
    county_code = request.args.get('county_code')
    congressional_district = request.args.get('congressional_district')
    senate_district = request.args.get('senate_district')
    house_district = request.args.get('house_district')
    birth_date = request.args.get('birth_date')
    return zrp(zipcode=zipcode,
               last_name=last_name,
               first_name=first_name,
               middle_name=middle_name,
               precinct_split=precinct_split,
               gender=gender,
               county_code=county_code,
               congressional_district=congressional_district,
               senate_district=senate_district,
               house_district=house_district,
               birth_date=birth_date)
