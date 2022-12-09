from opentelemetry import trace
from opentelemetry import metrics

from flask import Flask, request, json, Response
import jwt
import os

# Acquire a tracer and meter
tracer = trace.get_tracer("auth-app")
meter = metrics.get_meter("auth-app")
########### TELEMETRIA
registry_counter = meter.create_counter(
    "registry_counter",
    description="number of registry try",
)

login_counter= meter.create_counter(
        "login_counter",
        description="number of login try"
)
######### APLICAÇÃO
app = Flask(__name__)
# Dicionario de usuários cadastrados
users_data = {
    'aluno': '123'
}
#linux      curl --data '{"usuario":"lohann","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/registrar

@app.route("/registrar", methods=['POST'])
def registrar():
    global users_data
    data = json.loads(request.data)
    users_data[data['usuario']] = data['senha']
    retorno = app.response_class(response="Usuario registrado com sucesso!",
                                  status=200,
                                  mimetype='application/json')

    with tracer.start_as_current_span("registrar") as registryspan:
        registryspan.set_attribute("registry.value",data['usuario'])
        registryspan.set_attribute("registrypass.value",data['senha'])
        registry_counter.add(1, {"registry_counter": 0})
        return retorno

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data
    data = json.loads(request.data)
    usuario = data['usuario']
    senha = data['senha']

    with tracer.start_as_current_span("login") as loginspan:
        loginspan.set_attribute("login.value", data['usuario'])
        loginspan.set_attribute("loginpass.value",data['senha'])
        if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            loginspan.set_attribute("login.sucess", "sucess")
            return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
        else:
            loginspan.set_attribute("login.sucess", "fail")
            return app.response_class(response=json.dumps({"erro": "credênciais inválidas"}), mimetype='application/json', status=403)

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(
       response=json.dumps({"status": "OK"}),
       status=200,
       mimetype='application/json'
    )

if __name__ == "__main__":
    porta = os.environ.get("AUTH_PORT", 3000)
    app.run(host="0.0.0.0", port=porta, debug=True)
