from flask import Flask, request, json, Response
import jwt
from opentelemetry import trace, metrics

#traces
tracer = trace.get_tracer(__name__)
# metrics
meter = metrics.get_meter(__name__)

# Now create a counter instrument to make measurements with
roll_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",
)

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
    #usuario = data['usuario']
    #senha = data['senha']
    users_data[data['usuario']] = data['senha']
    return app.response_class(response="Usuario registrado com sucesso!",
                                  status=200,
                                  mimetype='application/json')
    with tracer.start_as_current_span("registrar") as span:
        span.set_attribute("Usuário cadastrado", data['usuario'])
        span.set_attribute("Senha cadastrada", data['senha'])

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data
    data = json.loads(request.data)
    usuario = data['usuario']
    senha = data['senha']
    with tracer.start_as_current_span("login") as span:
        span.set_attribute("Usuário logado", data['usuario'])
        span.set_attribute("Senha de login", data['senha'])
        if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
            span.set_attribute("Login status", "Login realizado")
        else:
            return app.response_class(response=json.dumps({"erro": "credenciais inválidas"}), mimetype='application/json', status=403)
            #with tracer.start_as_current_span("login") as span:
            span.set_attribute("Login status", "Credenciais inválidas")
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
