from flask import Flask, request, Response, render_template

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "ola mundo"

@app.route("/", methods=['GET','POST'])
def cadastro():
    #global registrar
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        msg = 'Cadastro realizado com sucesso! {} : {}'.format(usuario, senha)
        html = render_template('index.html', mensagem = msg)
    else:
        html = render_template('index.html')        
    retorno = app.response_class(response=html,
                            status=200,
                            mimetype='text/html')
    return retorno

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
