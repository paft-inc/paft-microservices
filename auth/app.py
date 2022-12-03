from flask import Flask, request, json

app = Flask(__name__)

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
