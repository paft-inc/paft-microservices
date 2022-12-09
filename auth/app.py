from flask import Flask, request, json, Response
from opentelemetry import trace
from opentelemetry import metrics
import jwt

tracer = trace.get_tracer(__name__)

meter = metrics.get_meter(__name__)

# Now create a counter instrument to make measurements with
registrar_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",

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
    with tracer.start_as_current_span("registrar") as registrospan:   
        data = json.loads(request.data)
        users_data[data['usuario']] = data['senha']
        retorno = app.response_class(response="Usuario registrado com sucesso!",
                                    status=200,
                                    mimetype='application/json')
        registrospan.set_attribute("usuario.value", data['usuario'])
        registrospan.set_attribute("senha.value", data['senha'])
        registrar_counter.add(1, {"registrar": 1})
        return retorno

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data
    with tracer.start_as_current_span("login") as loginspan:   
        data = json.loads(request.data)
        usuario = data['usuario']
        senha = data['senha']
        if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            loginspan.set_attribute("status.value", 200 OK
            return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
        else:
            loginspan.set_attribute("status.value", 403 Forbidden)
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