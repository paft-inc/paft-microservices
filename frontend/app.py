from flask import Flask
import os

app = Flask(__name__)
FRONT_PORT= os.environ.get("FRONT_PORT", 8080)



@app.route("/")
def hello_world():
    return "ola mundo"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONT_PORT, debug=True)
