from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch_data", methods = ["POST"])
def fetch_data():
    print("fetch_data")


if __name__ == "__main__":
    app.run(debug=True)