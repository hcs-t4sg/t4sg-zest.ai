from flask import Flask, request, session, jsonify, redirect, render_template
from flask_cors import CORS
import pandas as pd 
import surgeo
# surgeo documentation: https://surgeo.readthedocs.io/en/dev/#usage

app = Flask(__name__)
CORS(app)

# @app.route('/bisg', methods=['POST', 'GET'])
# def bisg():
#     if request.method == 'POST':
#         req = request.json
#         print("this is req: ")
#         print(req)
#         sg = surgeo.SurgeoModel()
#         first_names = pd.Series([req["name"]])
#         zctas = pd.Series([req["zipcode"]])
#         sg_results = sg.get_probabilities(surnames, zctas)
#         print("these are sg_results:")
#         print(sg_results)
#         return jsonify(name=req)
#     if request.method == 'GET':
#         return {
# 			'this is': 'a test for the get method of the bisg route'
# 		}

@app.route('/test/', methods=['POST', 'GET'])
def api_post():
    if request.method == 'POST':
        req = request.json
        print("this is req:")
        print(req)
        # newstring = req["name"] + req["zipcode"]
        # req["name"] = newstring
        # print(req["name"])
        return jsonify(name=req)
    if request.method == 'GET':
        return {
			'test app route': 'get is working'
		}

@app.route('/hello')
def say_hello_world():
    return {'result': "flask says hi (backend has been connected)"}
