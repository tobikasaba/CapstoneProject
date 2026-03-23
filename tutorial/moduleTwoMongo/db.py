# Imports the MongoClient class from the pymongo library
# MongoClient is used to establish a connection to the MongoDB database server
from pymongo import MongoClient


# Defines a function called 'init_db' that will initialize and populate the database
# This function takes no parameters and returns a MongoDB client object
def init_db():
    # Creates a new MongoDB client connection to the local MongoDB server
    # With no arguments, it defaults to connecting to 'localhost' on port 27017
    # This establishes the connection between your Python/Flask app and MongoDB
    client = MongoClient()

    # Accesses the 'tododb' database, then the 'todo' collection, and drops (deletes) it completely
    # 'client.tododb' accesses a database named 'tododb'
    # '.todo' accesses a collection (like a table) named 'todo' within that database
    # '.drop()' permanently deletes the entire collection and all its documents
    # This ensures you start with a clean slate every time the function runs
    # MongoDB is intuitive enough to create the database without having to
    client.tododb.todo.drop()

    # Inserts multiple documents into the 'todo' collection all at once
    # 'insert_many()' is a PyMongo method that takes a list of dictionaries
    # Each dictionary becomes a separate document (record) in the collection
    client.tododb.todo.insert_many(
        [
            # First document: a high-priority todo item
            # Each key-value pair becomes a field in the MongoDB document
            {"priority": "high", "title": "Get milk"},

            # Second document: a medium-priority todo item
            {"priority": "medium", "title": "Get gasoline"},

            # Third document: a low-priority todo item
            {"priority": "low", "title": "Water plants"}
        ]
    )

    # Returns the MongoDB client object so other parts of your Flask app can use it
    # This allows you to query, update, or delete data without creating a new connection
    return client