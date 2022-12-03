from flask import Flask, request, json, Response
import jwt

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
    app.run(host="0.0.0.0", port=3000, debug=True)

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data    
    data = json.loads(request.data)
    usuario = data['usuario']
    senha = data['senha']
    
    if users_data[usuario] == senha: 
        token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
        return app.response_class(response=json.dumps({"token": token_jwt}), headers='application/json', status=200)
    
    else:
        return app.response_class(body=json.dumps({"erro": "credênciais inválidas"}), headers='application/json', status=403)
