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


# Define a route that handles POST requests to "/picture" for creating new pictures
@app.route("/picture", methods=["POST"])
# Function that handles creating a new picture entry
def create_picture():
    # Parse the JSON body from the incoming request
    new_pic = request.get_json()

    # Validate that the request body exists and contains an 'id' field
    if not new_pic or "id" not in new_pic:
        # Return a 400 Bad Request if validation fails
        return {"message": "Invalid request: 'id' is required"}, 400

    # if any(pic["id"] == new_pic["id"] for pic in data):
    # Iterate through all existing pictures to check for duplicate IDs
    for pic in data:
        # Compare the new picture's ID with the current picture's ID
        if new_pic["id"] == pic["id"]:
            # Return a 302 Found if a picture with this ID already exists
            return {"message": f"picture with id {new_pic['id']} already present"}, 302

    # Add the new picture to the data list
    data.append(new_pic)
    # Return the newly created picture with a 201 Created status
    return jsonify(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


# Define a route that handles PUT requests to "/picture/<id>" for updating a picture
@app.route("/picture/<int:id>", methods=["PUT"])
# Function that updates an existing picture by its ID
def update_picture(id):
    # Parse the JSON body containing the updated picture data
    new_data = request.get_json()

    # Iterate through all pictures to find the one to update
    for pic in data:
        # Check if the current picture's ID matches the requested ID
        if pic["id"] == id:
            # Update the picture dictionary with the new data
            pic.update(new_data)
            # Return the updated picture with a 200 OK status
            return jsonify(pic), 200
    # Return a 404 Not Found if no picture with the given ID exists
    return {"message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################


# Define a route that handles DELETE requests to "/picture/<id>" for removing a picture
@app.route("/picture/<int:id>", methods=["DELETE"])
# Function that deletes a picture by its ID
def delete_picture(id):
    # Iterate through all pictures to find the one to delete
    for pic in data:
        # Check if the current picture's ID matches the requested ID
        if pic["id"] == id:
            # Remove the picture from the data list
            data.remove(pic)
            # Return a success message with a 204 No Content status
            return "", 204
    # Return a 404 Not Found if no picture with the given ID exists
    return {"message": "Picture not found"}, 404
