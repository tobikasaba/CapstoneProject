from pymongo import MongoClient

# connect to MongoDB server
connection = MongoClient()

# select the 'training' database
db = connection.training

# select the python collection
collection = db.python

# create a sample document
doc = {"lab":"Accessing mongodb using python", "Subject":"No SQL Databases"}

# insert a sample document
db.collection.insert_one(doc)

# query for all documents in 'training' database and 'python' collection
docs = db.collection.find({})

print("Printing the documents in the collection.")

for document in docs:
    print(document)

# close the server connection
print("Closing the connection.")
connection.close()