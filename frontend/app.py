from flask import Flask
import os

from flask import Flask, request, Response, render_templat

app = Flask(__name__)
FRONT_PORT= os.environ.get("FRONT_PORT", 8080)



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
# inclusão da variavel de ambiente FRONT_PORT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONT_PORT, debug=True)

    
