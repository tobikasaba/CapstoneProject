from flask import Flask, jsonify

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