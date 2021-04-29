from flask import Flask, request, session, jsonify, redirect, render_template
from flask_cors import CORS, cross_origin
import time
import json
import requests

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

from utils.zrp_predict import Basic_PreProcessor
from utils.api_tools import surgeo_helper, zrp_helper
from utils.data_augmentation import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_ORIGINS'] = ['http://localhost:3000', 'http://localhost:50000', "*"]
app.config['CORS_HEADERS'] = ['Content-Type']

@app.route('/hello')
def say_hello_world():
    return {'result': "Flask says Hello World"}

@app.route('/surgeo', methods=["GET", "POST"])
@cross_origin()
def internal_surgeo():
    # API for internal use and testing only; will be deprecated in the future
    # Required fields: 'surname', 'zipcode'

    surname = request.args.get('surname')
    zipcode = request.args.get('zipcode')

    return surgeo_helper(surname=surname,
                        zipcode=zipcode)

@app.route('/zrp', methods=["GET"])
@cross_origin()
def internal_zrp():
    # API for internal use and testing only; will be deprecated in the future
    # Required fields: 'Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split','Gender', 
    # 'County_Code','Congressional_District', 'Senate_District', 'House_District', 'Birth_Date'

    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')
    last_name = request.args.get('last_name')
    gender = request.args.get('gender')
    age = int(request.args.get('age'))

    currentYear = dt.date.today().year
    birth_date = "01/02/" + str(2021 - age)
    zipcode = request.args.get('zipcode')

    street_address = request.args.get('street_address')
    city = request.args.get('city')
    state = request.args.get('state')

    address = str(street_address) + ' ' + str(city) + ' ' + str(state) + ' ' + str(zipcode)

    req = requests.get(f'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address={address}&format=json&benchmark=4&vintage=4&layers=10,54,56,58&key=5554dd8086566b4f511eaf1add52ea5d8c4b09fa')
    req = req.json()

    precinct_split = ""

    #County Code in the Florida Voting Registration Data is unique in that it is a 3 letter code. In the Census API, it is a 3 digit code — the json is used to facilitate the mapping between the two codes for the model to run properly
    county_code = req["result"]["addressMatches"][0]["geographies"]["Census Block Groups"][0]["COUNTY"]
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'fl_county_codes.json')
    special_county_codes = json.load(open(json_url))
    county_code = special_county_codes[county_code]

    congressional_district = req["result"]["addressMatches"][0]["geographies"]["116th Congressional Districts"][0]["CD116"]
    senate_district = req["result"]["addressMatches"][0]["geographies"]["2018 State Legislative Districts - Upper"][0]["SLDU"]
    house_district = req["result"]["addressMatches"][0]["geographies"]["2018 State Legislative Districts - Lower"][0]["SLDL"]

    return zrp_helper(zipcode=zipcode,
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

@app.route('/predictions', methods=["GET"])
def get_predictions():
    # Final API that returns both the surgeo and zrp predictions as a JSON object

    # Below is the exhaustive list of necessary fields (with no data augmentation; we hope to shorten this list)

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
    birth_date = request.args.get('birth_date')         #need to change to age

    # Data Augmentation step (not implemented yet)
    # TO-DO: for each data augmentation step / API called, factor the API call into a helper function in utils/data_augmentation.py

    surgeo_prediction_json = surgeo_helper(surname=last_name, 
                                      zipcode=zipcode)

    zrp_prediction_json = zrp_helper(zipcode=zipcode,
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

    # flag for later: this is inefficient, encoding/decoding the json objects multiple times; will fix on future refactor if possible
    return json.dumps({'surgeo': json.loads(surgeo_prediction_json), 
                       'zrp': json.loads(zrp_prediction_json)})
