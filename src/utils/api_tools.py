import json

import pandas as pd
import surgeo

import utils.zrp_predict as zrp_predict

def surgeo_helper(surname, zipcode):
    # Returns the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}
    surname_series = pd.Series([surname])
    zip_series = pd.Series([zipcode])

    sg = surgeo.SurgeoModel()
    sg_results = sg.get_probabilities(surname_series, zip_series)

    sg_json = pd.DataFrame.to_json(sg_results)
    return(sg_json)

def zrp_helper(zipcode, last_name, first_name, middle_name, precinct_split, gender, 
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