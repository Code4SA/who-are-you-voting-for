import json
import a2c
import requests
import json
from flask import Flask
from flask import Response
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello"

def process_request(req):
    address = req.args.get("address")
    lat = req.args.get("lat")
    lon = req.args.get("lon")
    ward_no = req.args.get("ward")
    ward = None

    variables = {'missing': False}
    candidates = []
    if address:
        ward = a2c.address_to_ward(address)
    elif lat:
        ward = a2c.coords_to_ward(lon, lat)
    elif ward_no:
        ward = a2c.ward_to_ward(ward_no)

    if ward:
        if ward['ward']:
            variables.update(ward)
            candidates = a2c.get_candidates(ward["ward"])
            variables["candidates"] = candidates
            for candidate in candidates:
                age = a2c.get_age(candidate["IDNumber"])
                candidate["wards"] = a2c.ids[candidate["IDNumber"]]
                candidate["age"] = age
        else:
            variables['missing'] = True
    return variables

@app.route("/")
def get_candidates():
    variables = process_request(request)
    
    return render_template('index.html', **variables)

@app.route("/api")
def json_candidates():
    mimetype = "application/json"
    variables = process_request(request)
    return  Response(response=json.dumps(variables), status=200, mimetype=mimetype)

if __name__ == "__main__":
    app.run(debug=True)
