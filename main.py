from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, collection

client = MongoClient()
app = Flask(__name__)

client = MongoClient("localhost", 27017)
client = MongoClient("mongodb://localhost:27017/")

db = client.database


@app.route("/")
def index():

    # TODO: delete this and add procedural reloading so database loads and updates page when loaded
    collection_names = db.list_collection_names()

    # DROPS TABLES
    # for collection_name in collection_names:
    #     db.drop_collection(collection_name)

    # PRINTS TABLES
    for collection_name in collection_names:
        print("Collection:", collection_name)
        collection = db[collection_name]

        documents = collection.find()

        for document in documents:
            print("Document:", document)

    return render_template("index.html")

@app.route("/get_data_on_page_load", methods = ["GET"])
def get_data_on_page_load():

    documents_data = []

    collection_names = db.list_collection_names()

    for collection_name in collection_names:
        collection = db[collection_name]

        documents = collection.find()

        for document in documents:
            data = {
                "name": document["name"],
                "link": document["link"],
                "category": document["category"]
            }
            documents_data.append(data)

    data = {
        "categories": collection_names,
        "rows": documents_data
    }

    return jsonify({'collections': data})


@app.route("/submit_entry", methods = ["POST"])
def submit_entry():
    data = request.json

    category = data.get('category')
    name = data.get('name')
    link = data.get('link')

    if category in db.list_collection_names():
        collection = db[category]
    else:
        collection = db.create_collection(category)

    data = {
        "category": category,
        "name": name,
        "link": link
    }

    collection.insert_one(data)
    for document in collection.find():
        print(document)

    return jsonify({'message': 'Entry submitted successfully'})


if __name__ == "__main__":
    app.run(debug=True)