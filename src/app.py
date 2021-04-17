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

from utils.zrp_predict import Basic_PreProcessor
from utils.api_tools import surgeo_helper, zrp_helper

app = Flask(__name__)
CORS(app, resources={r"/surgeo/*": {"origins": "*"}, r"/zrp/*": {"origins": "*"}})

@app.route('/hello')
def say_hello_world():
    return {'result': "Flask says Hello World"}

@app.route('/surgeo', methods=["GET", "POST"])
def internal_surgeo():
    # API for internal use and testing only; will be deprecated in the future
    # Required fields: 'surname', 'zipcode'

    surname = request.args.get('surname')
    zipcode = request.args.get('zipcode')

    return surgeo_helper(surname=surname, 
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