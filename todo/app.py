from flask import Flask, request, json
import jwt
import uuid

app = Flask(__name__)
lista_todos = {}

@app.route("/todos", methods=['POST'])
def todos():

    authorization = request.headers.get('Authorization')
    authorization = authorization.split()[-1]

    usuario = jwt.decode(authorization, "secret", algorithms=["HS256"])['usuario']

    id = uuid.uuid4()
    todo = {
        "id": id,
        "todo": "Fazer trabalho de devops!!",
        "concluido": False
    }

    global lista_todos
    if usuario not in lista_todos:
        lista_todos[usuario] = {}

    lista_todos[usuario][id] = todo

    response = app.response_class(status=200, response= json.dumps(todo))
    response.headers['Content-Type'] = 'application/json'
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
