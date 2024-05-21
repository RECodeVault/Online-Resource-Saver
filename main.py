from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient()
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")

db = client.database


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/get_all_entries", methods = ["GET"])
def get_all_entries():

    documents = []

    for collection_name in db.list_collection_names():
        collection = db[collection_name]

        for document in collection.find():
            data = {
                "name": document["name"],
                "link": document["link"],
                "category": document["category"]
            }

            documents.append(data)

    return jsonify({'collections': documents})




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

    return jsonify({'collections': documents_data})


@app.route("/delete_row", methods = ["POST"])
def delete_row():

    data = request.json

    currentCategory = data.get('currentCategory')
    index = data.get('index')

    collection_names = db.list_collection_names()

    for collection_name in collection_names:
        if collection_name == currentCategory:
            collection = db[collection_name]
            document_to_delete = collection.find_one(skip=index)
            if document_to_delete:
                collection.delete_one({"_id": document_to_delete["_id"]})
            else:
                print("No document found at index", index)

    return jsonify({'message': 'Entry submitted successfully'})



@app.route("/delete_category", methods = ["POST"])
def delete_category():

    data = request.data.decode('utf-8')

    collection_names = db.list_collection_names()

    for collection_name in collection_names:
        if collection_name == data:
            db.drop_collection(collection_name)

    return jsonify({'message': 'Entry submitted successfully'})


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