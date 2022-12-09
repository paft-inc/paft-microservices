from flask import Flask, request, json, Response
import jwt
from opentelemetry import trace


tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# Dicionario de usuários cadastrados
users_data = {
    'aluno': '123'
}

@app.route("/rolldice")
def roll_dice():
    return str(login())

#linux      curl --data '{"usuario":"lohann","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/registrar
#windows    curl.exe --data '{\"usuario\":\"lohann\",\"senha\":\"123\"}' -H "Content-Type:application/json" -X POST localhost:3000/registrar

@app.route("/registrar", methods=['POST'])
def registrar():
    with tracer.start_as_current_span("registro") as registrarspan:
        global users_data    
        data = json.loads(request.data)
        res = data['usuario']
        registrarspan.set_attribute("registro.value", res)
        users_data[data['usuario']] = data['senha']
        retorno = app.response_class(response="Usuario registrado com sucesso!",
                                    status=200,
                                    mimetype='application/json')
        return retorno

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    with tracer.start_as_current_span("login") as loginspan:
        global users_data    
        data = json.loads(request.data)        
        res = data['usuario']
        loginspan.set_attribute("login.value", res)
        usuario = data['usuario']
        senha = data['senha']
        if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
        else:
            return app.response_class(response=json.dumps({"erro": "credênciais inválidas"}), mimetype='application/json', status=403)
           

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(
       response=json.dumps({"status": "OK"}),
       status=200,
       mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)