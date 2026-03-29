from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

client = MongoClient()

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################

# Register GET /health — used by cloud platforms to check if the service is running
@app.route("/health", methods=["GET"])
def health():
    # Return JSON {"status": "OK"} with HTTP 200
    return jsonify(status="OK"), 200


# Register GET /count — returns total number of songs in the database
@app.route("/count")
def count():
    # count_documents({}) counts all documents in the collection; empty dict = no filter conditions
    song_count = db.songs.count_documents({})
    # Serialise result to JSON {"length": <number>} and return with HTTP 200 OK
    return jsonify(length=song_count), 200

# Register GET /song — returns all songs from MongoDB
@app.route("/song", methods=["GET"])
def songs():
    # find({}) returns a cursor of all documents
    cursor = db.songs.find({})
    # parse_json converts each MongoDB document (including ObjectId) to serialisable JSON
    return jsonify(songs=[parse_json(song) for song in cursor]), 200

@app.route("/song/<song_id>")
def get_song_by_id(song_id):
    # Look up a single song document whose numeric "id" matches the URL value.
    song = db.songs.find_one({"id":int(song_id)})
    # If MongoDB returned a document, convert it to JSON-safe data and send it back.
    if song:
        return jsonify(song=parse_json(song))
    # If no document matched the id, return a 404 response with an error message.
    return jsonify(message="Song with id not found"), 404
