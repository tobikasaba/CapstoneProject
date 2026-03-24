from pymongo import MongoClient

client = MongoClient()

db = client.training.mongodb_glossary

doc = ({"database":"a database contains collections"},
       {"collection":"a collection stores the documents"},
       {"document":"a document contains the data in the form of key value pairs."})

db.collection.insert_many(doc)

documents = db.collection.find({})

print("Printing the documents in the collection.")

for document in documents:
    print(document)

# close the server connection
print("Closing the connection.")
client.close()