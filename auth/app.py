from flask import Flask, request, json, Response
import jwt

app = Flask(__name__)

tracer = trace.get_tracer(__name__)

meter = metrics.get_meter(__name__)

register_counter = meter.create_counter(
        "register_counter",
        description="Number of registrys",
)
login_auth_counter = meter.create_counter(
        "login_auth_counter",
        description="Number of sucessfull logins",
)
login_refu_counter = meter.create_counter(
        "login_refu_counter",
        description="Number of unsucessfull logins",
)


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
        register_counter.add(1, {"register_counter":0})
    	return retorno

#linux      curl --data '{"usuario":"aluno","senha":"123"}' -H "Content-Type: application/json" -X POST localhost:3000/login
@app.route("/login", methods=['POST'])
def login():
    global users_data    
    with tracer.start_as_current_span("login") as loginspan:
	data = json.loads(request.data)
    	usuario = data['usuario']
    	senha = data['senha']
	loginspan.set_attribute("usuario.value", data['usuario'])
        loginspan.set_attribute("senha.value", data['senha'])
    	if usuario in users_data and users_data[usuario] == senha:
            token_jwt = jwt.encode({"usuario": usuario}, "secret", algorithm="HS256")
            loginspan.set_attribute("loginspan.value", "AUTORIZADO")
            login_auth_counter.add(1, {"login_auth_counter":0})
	    return app.response_class(response=json.dumps({"token": token_jwt}), mimetype='application/json', status=200)
    	else:
            loginspan.set_attribute("loginspan.value", "RECUSADO")
	    login_refu_counter.add(1, {"login_refu_counter":0})
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
