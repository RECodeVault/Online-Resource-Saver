from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


client = MongoClient()
app = Flask(__name__)

client = MongoClient("localhost", 27017)
client = MongoClient("mongodb://localhost:27017/")

db = client.database


@app.route("/")
def index():

    # TODO: delete this and add procedural reloading so database loads and updates page when loaded
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        db.drop_collection(collection_name)
    return render_template("index.html")


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
        "name": name,
        "link": link
    }

    collection.insert_one(data)
    for document in collection.find():
        print(document)

    return jsonify({'message': 'Entry submitted successfully'})


if __name__ == "__main__":
    app.run(debug=True)