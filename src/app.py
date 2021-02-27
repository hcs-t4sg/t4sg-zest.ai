from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def say_hello_world():
    return {'result': "Flask says Hello World"}

@app.route('/surgeo', methods=["GET"])
def surgeo():
    # TO-DO: @KAYLA
    # Build out a public facing API that responds to a get request with the surname and zip code as query arguments. 
    # The API should return the probabilities of each race prediction as a JSON object.
    # Example of return object: {'AAPI': .56, 'Hispanic': .32, ..., 'White': .10}

    pass

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