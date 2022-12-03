from flask import Flask, json, Response

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(
       response=json.dumps({"status": "OK"}),
       status=200,
       mimetype='application/json'
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
