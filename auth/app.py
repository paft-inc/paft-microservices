from opentelemetry import trace
from flask import Flask, request, json, Response
import jwt


tracer = trace.get_tracer("auth-app")


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
    with tracer.start_as_current_span("registrar") as registrarspan:
        registrarspan.set_attribute("registro.usuario",data['usuario'])
        registrarspan.set_attribute("registro.senha",data['senha'])
        
        return retorno


#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data    
    data = json.loads(request.data)
    usuario = data['usuario']
    senha = data['senha']

    with tracer.start_as_current_span("login") as loginspan:
        loginspan.set_attribute("login.usuario", data['usuario'])
        loginspan.set_attribute("login.senha",data['senha'])
        if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            loginspan.set_attribute("login.realizado", "login")
            return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
        else:
            loginspan.set_attribute("login.realizado", "falhou")
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