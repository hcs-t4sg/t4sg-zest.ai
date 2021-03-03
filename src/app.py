from flask import Flask, request, session, jsonify, redirect, render_template
from flask_cors import CORS

# Needed for surgeo route
import pandas as pd 
import surgeo

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

    # print for debugging
    # print("these are the surgeo model results: ")
    # print(sg_results)

    sg_json = pd.DataFrame.to_json(sg_results)
    return(sg_json)

    # END OF SURGEO API; END OF TO-DO @KAYLA

@app.route('/zrp', methods=["GET"])
def zrp():
    # TO-DO: @RAKESH
    # Build out a public facing API that responds to a get request with the full name, address, age, and gender as a query arguments. 
    # The API should return the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}

    # As part of this, you should add any relevant pickle files that you might want to call to the directory "picklefiles".
    # These files will be stored on the server and your API will be able to call them in order to make predictions.
    # Currently, there's just one file in the picklefiles folder: the pickled Florida predictor that was sent over by Kasey, but feel free to add more.
    # Also, if you're having trouble accessing a picklefile in the picklefiles folder, DM Chris. It may be a problem with how the Dockerfile is set up
    # and how it copies the picklefile folder over to the container.
    
    pass
    
    # END OF ZRP API; END OF TO-DO @RAKESH