from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "No pictures available"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
# Define a route that handles GET requests to the "/picture" endpoint
@app.route("/picture", methods=["GET"])
# Function that retrieves and returns all pictures
def get_pictures():
    # Check if the data variable contains any pictures
    if data:
        # Return the data as JSON with a 200 OK status code
        return jsonify(data), 200
    # Return an error message with a 500 Internal Server Error status if no data exists
    return {"message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################

# Define a route that handles GET requests to "/picture/<id>" where id is an integer
@app.route("/picture/<int:id>", methods=["GET"])
# Function that retrieves a specific picture by its ID
def get_picture_by_id(id):
    # Check if the data variable contains any pictures
    if data:
        # Iterate through each picture in the data list
        for picture in data:
            # Check if the current picture's id matches the requested id
            if picture["id"] == id:
                # Return the matching picture as JSON with a 200 OK status code
                return jsonify(picture), 200
    # Return a 404 Not Found error if no picture with the given id exists
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pass

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
