from flask import Flask, request, session, jsonify, redirect, render_template
from flask_cors import CORS

# Needed for surgeo route
import pandas as pd 
import surgeo
import pickle
import zrp_predict
import json

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def say_hello_world():
    return {'result': "Flask says Hello World"}

@app.route('/surgeo', methods=["GET"])
def run_surgeo():
    # TO-DO: @KAYLA
    # Build out a public facing API that responds to a get request with the surname and zip code as query arguments. 
    # The API should return the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}

    surname = request.args.get('surname')
    zipcode = request.args.get('zipcode')
    surname_series = pd.Series([surname])
    zip_series = pd.Series([zipcode]) 

    sg = surgeo.SurgeoModel()
    sg_results = sg.get_probabilities(surname_series, zip_series)

    sg_json = pd.DataFrame.to_json(sg_results)
    return(sg_json)

    # END OF SURGEO API; END OF TO-DO @KAYLA

@app.route('/zrp', methods=["GET"])
def zrp():
    # TO-DO: @RAKESH
    # Build out a public facing API that responds to a get request with the full name, address, age, and gender as a query arguments. 
    # The API should return the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}
    # Required fields: 'Name_First', 'Name_Last', 'Name_Middle', 'Zipcode', 'Precinct_Split','Gender', 'County_Code','Congressional_District', 'Senate_District', 'House_District', 'Birth_Date'

    # As part of this, you should add any relevant pickle files that you might want to call to the directory "picklefiles".
    # These files will be stored on the server and your API will be able to call them in order to make predictions.
    # Currently, there's just one file in the picklefiles folder: the pickled Florida predictor that was sent over by Kasey, but feel free to add more.
    # Also, if you're having trouble accessing a picklefile in the picklefiles folder, DM Chris. It may be a problem with how the Dockerfile is set up
    # and how it copies the picklefile folder over to the container.

    zipcode = request.args.get('zipcode')
    last_name = request.args.get('last_name')
    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')
    zipcode = request.args.get('zipcode')
    precinct_split = request.args.get('precinct_split')
    gender = request.args.get('gender')
    county_code = request.args.get('county_code')
    congressional_district = request.args.get('congressional_district')
    senate_district = request.args.get('senate_district')
    house_district = request.args.get('house_district')
    birth_date = request.args.get('birth_date')

    data = {'Name_First': [str(first_name)], 'Name_Last': [str(last_name)], 'Name_Middle': [str(middle_name)], 'Zipcode': [int(zipcode)], 'Precinct_Split': [str(precinct_split)], 'Gender': [str(gender)], 'County_Code': [str(county_code)], 'Congressional_District':[float(congressional_district)], 'Senate_District': [float(senate_district)], 'House_District': [float(house_district)], 'Birth_Date': [str(birth_date)]}
    #data = {'Name_First': ['George'], 'Name_Last': ['Chambers'], 'Name_Middle': ['William'], 'Zipcode': [34293], 'Precinct_Split': ['NaN'], 'Gender': ['M'], 'County_Code': ['SAR'], 'Congressional_District':[17.0], 'Senate_District': [23.0], 'House_District': [74.0], 'Birth_Date': ['12/02/1951']}
    sample = pd.DataFrame(data)
    preds = zrp_predict.generatePredictions(sample)

    preds_data = {'American Indian': preds[0], 'Asian Pacific Islander': preds[1], 'Black': preds[2], 'Hispanic': preds[3], 'White': preds[4], 'Other': preds[5], 'Multi': preds[6]}
    json_preds = json.dumps(preds_data)
    return json_preds
    
    # END OF ZRP API; END OF TO-DO @RAKESH