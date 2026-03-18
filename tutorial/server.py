from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/dict")
def python_dictionary():
    return {"message": "Hello World 2"}


@app.route("/jsonify")
def use_jsonify():
    return jsonify(message="Hello World 3")


@app.route("/no_content")
def no_content():
    # return no content to the user due to 204 status code implemented
    return {"message": "No content found"}, 204

@app.route("/exp")
def index_explicit():
    # Create a response object with the message "Hello World"
    resp = make_response({"message": "Hello World"})
    # Set the status code of the response to 200
    resp.status_code = 200
    # Return the response object
    return resp

