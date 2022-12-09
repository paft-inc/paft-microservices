from opentelemetry import trace

from flask import Flask, request, json, Response
import jwt

tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# Dicionario de usuários cadastrados
users_data = {
    'aluno': '123'
}

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
    with tracer.start_as_current_span("registros") as regisspan:
        regisspan.set_attribute("usuario.value", retorno["usuario"])
        regisspan.set_attribute("senha.login", retorno["senha"])
        return retorno

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data    
    data = json.loads(request.data)
    usuario = data['usuario']
    senha = data['senha']
    with tracer.start_as_current_span("login_regis") as loginspan:
            loginspan.set_attribute("usuario.login", data["usuario"])
            loginspan.set_attribute("senha.login", data["senha"])
            if usuario in users_data and users_data[usuario] == senha:
                token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
                sucesso = app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
                loginspan.set_attribute("senha.sucesso", "sucesso")
                return sucesso
            else:
                erro = app.response_class(response=json.dumps({"erro": "credênciais inválidas"}), mimetype='application/json', status=403)
                loginspan.set_attribute("senha.sucesso", "erro")
                return erro
            
@app.route('/health', methods=['GET'])
def health():
    return app.response_class(
       response=json.dumps({"status": "OK"}),
       status=200,
       mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)