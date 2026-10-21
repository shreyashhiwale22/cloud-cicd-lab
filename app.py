
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Cloud Computing Lab"

@app.route("/student")
def student():
    return jsonify({
        "name": "Shreyash Hiwale",
        "course": "Computer Science Engineering",
        "experiment": "CI/CD Pipeline"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
