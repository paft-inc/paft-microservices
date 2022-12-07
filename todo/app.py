from flask import Flask, request, json, Response
import jwt
import uuid

app = Flask(__name__)
lista_todos = {}

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(
       response=json.dumps({"status": "OK"}),
       status=200,
       mimetype='application/json'
    )

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
    porta = os.environ.get("TODO_PORT", 4000)
    app.run(host="0.0.0.0", port=porta, debug=True)
