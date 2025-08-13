from flask import Flask, render_template, redirect, url_for, request, flash, abort, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

gerenciador_login = LoginManager()
gerenciador_login.init_app(app)
gerenciador_login.login_view = 'login'

def gerar_hash_senha(senha):
    return generate_password_hash(senha)

def verificar_senha(hash_senha, senha):
    return check_password_hash(hash_senha, senha)

class Funcionario(UserMixin):
    def __init__(self, id, nome, email, telefone, categoria, hash_senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.categoria = categoria
        self.hash_senha = hash_senha

def buscar_funcionario_por_email(email):
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE email = ?", (email,))
    linha = cursor.fetchone()
    conexao.close()
    if linha:
        return Funcionario(*linha)
    return None

def buscar_funcionario_por_id(id):
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (id,))
    linha = cursor.fetchone()
    conexao.close()
    if linha:
        return Funcionario(*linha)
    return None

@gerenciador_login.user_loader
def carregar_usuario(id_usuario):
    return buscar_funcionario_por_id(id_usuario)

@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if current_user.categoria != 'gerente':
        flash('Apenas gerentes podem cadastrar novos funcionários.')
        return redirect(url_for('painel'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        categoria = request.form['categoria']
        senha = request.form['senha']

        if not nome or not email or not telefone or not categoria or not senha:
            flash('Todos os campos são obrigatórios.')
            return render_template('cadastro.html')

        if buscar_funcionario_por_email(email):
            flash('Email já cadastrado.')
            return render_template('cadastro.html')

        hash_senha = gerar_hash_senha(senha)
        conexao = sqlite3.connect('projeto.db')
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO funcionarios (nome, email, telefone, categoria, senha_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, telefone, categoria, hash_senha))
        conexao.commit()
        conexao.close()
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('painel'))

    return render_template('cadastro.html')

@app.route('/alternar_tema')
def alternar_tema():
    tema_atual = request.cookies.get('tema', 'claro')
    novoTema = 'escuro' if tema_atual == 'claro' else 'claro'
    
    resposta = make_response(redirect(url_for('painel')))
    resposta.set_cookie('tema', novoTema, max_age=30*24*60*60)
    flash(f"Tema alterado para {novoTema}!")
    return resposta

@app.route('/funcionarios')
@login_required
def listar_funcionarios():
    if current_user.categoria != 'gerente':
        flash('Acesso restrito a gerentes.')
        return redirect(url_for('painel'))
    
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email, telefone, categoria FROM funcionarios")
    funcionarios = cursor.fetchall()
    conexao.close()
    return render_template('funcionarios.html', funcionarios=funcionarios)

@app.route('/funcionario/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_funcionario(id):
    if current_user.categoria != 'gerente':
        flash('Acesso restrito a gerentes.')
        return redirect(url_for('painel'))
    
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        categoria = request.form['categoria']
        
        cursor.execute("""
            UPDATE funcionarios 
            SET nome = ?, email = ?, telefone = ?, categoria = ?
            WHERE id = ?
        """, (nome, email, telefone, categoria, id))
        conexao.commit()
        conexao.close()
        flash('Funcionário atualizado com sucesso!')
        return redirect(url_for('listar_funcionarios'))
    
    cursor.execute("SELECT id, nome, email, telefone, categoria FROM funcionarios WHERE id = ?", (id,))
    funcionario = cursor.fetchone()
    conexao.close()
    
    if not funcionario:
        abort(404)
    
    return render_template('editar_funcionario.html', funcionario=funcionario)

@app.route('/funcionario/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_funcionario(id):
    if current_user.categoria != 'gerente':
        flash('Acesso restrito a gerentes.')
        return redirect(url_for('painel'))
    
    if current_user.id == id:
        flash('Você não pode excluir seu próprio usuário.')
        return redirect(url_for('listar_funcionarios'))
    
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    flash('Funcionário excluído com sucesso!')
    return redirect(url_for('listar_funcionarios'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        funcionario = buscar_funcionario_por_email(email)
        if funcionario and verificar_senha(funcionario.hash_senha, senha):
            login_user(funcionario)
            return redirect(url_for('painel'))
        else:
            return render_template('login.html', erro='Credenciais inválidas', hide_navbar=True)
    return render_template('login.html', hide_navbar=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('home.html', hide_navbar=True)

@app.route('/painel')
@login_required
def painel():
    return render_template('index.html', funcionario=current_user)

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', funcionario=current_user)


@app.route('/precos', methods=['GET', 'POST'])
@login_required
def precos():
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    mensagem = None

    if request.method == 'POST' and 'produto_id' in request.form and current_user.categoria in ['caixa', 'gerente']:
        id_produto = request.form['produto_id']
        novo_preco = request.form['novo_preco']
        cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, id_produto))
        conexao.commit()
        mensagem = 'Preço atualizado com sucesso!'

    if request.method == 'POST' and 'novo_nome' in request.form and current_user.categoria in ['caixa', 'gerente']:
        nome = request.form['novo_nome']
        preco = request.form['novo_preco_produto']
        if nome and preco:
            cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
            conexao.commit()
            mensagem = 'Produto adicionado com sucesso!'

    cursor.execute("SELECT * FROM produtos")
    lista_produtos = cursor.fetchall()
    conexao.close()
    return render_template(
        'precos.html',
        produtos=lista_produtos,
        pode_editar=current_user.categoria in ['caixa', 'gerente'],
        mensagem=mensagem
    )

@app.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    if current_user.categoria != 'caixa':
        flash('Acesso restrito.')
        return redirect(url_for('painel'))
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    lista_produtos = cursor.fetchall()
    if request.method == 'POST':
        produtos_selecionados = request.form.getlist('produtos')
        forma_pagamento = request.form['forma_pagamento']
        valor_total = 0
        for id_produto in produtos_selecionados:
            for produto in lista_produtos:
                if str(produto[0]) == id_produto:
                    quantidade = int(request.form.get(f'quantidade_{id_produto}', 1))
                    valor_total += produto[2] * quantidade
        cursor.execute("""
            INSERT INTO pedidos (funcionario_id, data, forma_pagamento, valor_total)
            VALUES (?, datetime('now'), ?, ?)
        """, (current_user.id, forma_pagamento, valor_total))
        conexao.commit()
        flash('Pedido registrado com sucesso!')
    conexao.close()
    return render_template('pedidos.html', produtos=lista_produtos)

@app.route('/relatorios')
@login_required
def relatorios():
    if current_user.categoria != 'gerente':
        flash('Acesso restrito.')
        return redirect(url_for('painel'))
    conexao = sqlite3.connect('projeto.db')
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', data) as mes, SUM(valor_total) as renda
        FROM pedidos GROUP BY mes
    """)
    renda_mensal = cursor.fetchall()
    cursor.execute("""
        SELECT strftime('%Y-%m', p.data) as mes, SUM(i.custo * pi.quantidade) as custo
        FROM pedidos p
        JOIN pedido_ingrediente pi ON p.id = pi.pedido_id
        JOIN ingredientes i ON pi.ingrediente_id = i.id
        GROUP BY mes
    """)
    custo_mensal = cursor.fetchall()
    conexao.close()
    return render_template('relatorios.html', renda_mensal=renda_mensal, custo_mensal=custo_mensal)

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_servidor(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
