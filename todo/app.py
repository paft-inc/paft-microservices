from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "ola mundo"
 
if __name__ == "__main__":
    porta = os.environ.get("TODO_PORT", 4000)
    app.run(host="0.0.0.0", port=porta, debug=True)
