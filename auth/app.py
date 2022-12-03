from flask import Flask, request, json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "ola mundo"

#linux      curl --data '{"usuario":"lohann","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/registrar
#windows    curl.exe --data '{\"usuario\":\"lohann\",\"senha\":\"123\"}' -H "Content-Type:application/json" -X POST localhost:3000/registrar
@app.route("/registrar", methods=['POST'])
def registrar():
    global users_data    
    data = json.loads(request.data)
    users_data[data['usuario']] = data['senha']
    retorno = app.response_class(response="Usuario registrado com sucesso!",
                                  status=200,
                                  mimetype='application/json')
    return retorno

if __name__ == "__main__":
    users_data = {}
    porta = os.environ.get("AUTH_PORT", 3000)
    app.run(host="0.0.0.0", port=porta, debug=True)
