from bson import json_util
from flask import Flask
from . import db

app = Flask(__name__)

client = db.init_db()


@app.route("/todos")
def index():
    # Queries the MongoDB database to find all documents in the 'todo' collection
    # find({}) with empty dict means "no filter, return everything"
    # Returns a Cursor object (like a pointer to results, not the actual data yet)
    result = client.tododb.todo.find({})

    # Converts MongoDB cursor to JSON and returns it with HTTP status 200
    # json_util.dumps() converts BSON (MongoDB format) to JSON string
    # list(result) converts the cursor into a Python list of dictionaries
    # 200 is the HTTP status code meaning "OK, request successful"
    return json_util.dumps(list(result)), 200



@app.route("/todos/<priority>")
# Defines the function that handles requests to "/todos/<priority>"
# The 'priority' parameter receives the value from the URL automatically
# If URL is /todos/high, then priority = "high"
def get_by_priority_better(priority):
    # Queries MongoDB to find documents where the 'priority' field matches the URL parameter
    # {"priority": priority} is a filter - only returns matching documents
    # If priority="high", this finds all documents with "priority": "high"
    # Returns a Cursor object pointing to the matching results
    result = client.tododb.todo.find({"priority": priority})

    # Converts the cursor to a Python list immediately
    # We need the list here (not in the return) because we check its length next
    # After converting to list, the cursor is exhausted (can't be used again)
    result_list = list(result)

    # Checks if no results were found
    # 'not result' checks if cursor is falsy (though cursors are always truthy)
    # 'len(result_list) < 1' checks if the list is empty (no matching documents)
    # This condition is True when no todos match the priority filter
    if not result or len(result_list) < 1:
        # Returns an empty list as JSON with HTTP status 404 (Not Found)
        # 404 tells the client "I understood your request, but found nothing"
        return json_util.dumps(result_list), 404

    # If we reach here, we found at least one matching document
    # Converts the list to JSON and returns it with HTTP status 200 (OK)
    return json_util.dumps(result_list), 200