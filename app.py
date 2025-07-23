from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conecta():
    return sqlite3.connect('banco.db')

@app.route('/')
def index():   

    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    erro = None  

    if request.method == 'POST':
        email = request.form['email']
        telefone = request.form['telefone']
        categoria = request.form['categoria']
        senha = request.form['senha']
        confirmar = request.form['confirmar']

  
        if not email or not telefone or not categoria or not senha or not confirmar:
            erro = 'Preencha todos os campos.'
        elif senha != confirmar:
            erro = 'As senhas não são iguais.'
        else:
            conexao_banco = conecta()
            executador = conexao_banco.cursor()

            executador.execute('SELECT * FROM funcionarios WHERE email = ?', (email,))
            existe = executador.fetchone()

            if existe:
                erro = 'Esse email já está cadastrado.'
            else:
                executador.execute('INSERT INTO funcionarios (email, telefone, categoria, senha) VALUES (?, ?, ?, ?)',
                            (email, telefone, categoria, senha))
                conexao_banco.commit()
                executador.close()
                return redirect('/registro_sucesso')  

    return render_template('registro.html', erro=erro)

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao_banco = conecta()
        cursor = conexao_banco.cursor()
        cursor.execute('SELECT senha FROM funcionarios WHERE email = ?', (email,))
        resultado = cursor.fetchone()

        if resultado is None:
            erro = 'Usuário não encontrado.'
        else:
            senha_armazenada = resultado[0]
            if senha != senha_armazenada:
                erro = 'Senha incorreta.'
            else:
                return 'Login efetuado com sucesso!'  # Aqui você pode redirecionar para outra página

    return render_template('login.html', erro=erro)

@app.route('/registro_sucesso')
def sucesso():
    return 'Cadastro feito com sucesso!'

@app.route('/logout')
def logout():
    return render_template ('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
