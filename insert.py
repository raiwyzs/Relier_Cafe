import sqlite3
import hashlib

SCHEMA = 'schema.sql'


conexao_banco = sqlite3.connect('projeto.db')
with open(SCHEMA) as f:
    conexao_banco.executescript(f.read())
conexao_banco.close()

def hash_password(password):
    secret_key = 'sua_secret_key_aqui'
    return hashlib.sha256((password + secret_key).encode()).hexdigest()

def inserir_funcionario(nome, email, telefone, categoria, senha):
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    senha_hash = hash_password(senha)
    cursor.execute("""
        INSERT INTO funcionarios (nome, email, telefone, categoria, senha_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, email, telefone, categoria, senha_hash))
    conn.commit()
    conn.close()

def inserir_produto(nome, preco):
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, preco)
        VALUES (?, ?)
    """, (nome, preco))
    conn.commit()
    conn.close()

def inserir_ingrediente(nome, custo):
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ingredientes (nome, custo)
        VALUES (?, ?)
    """, (nome, custo))
    conn.commit()
    conn.close()

def inserir_pedido(funcionario_id, data, forma_pagamento, valor_total, produtos, ingredientes):
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (funcionario_id, data, forma_pagamento, valor_total)
        VALUES (?, ?, ?, ?)
    """, (funcionario_id, data, forma_pagamento, valor_total))
    pedido_id = cursor.lastrowid
    for produto_id, quantidade in produtos:
        cursor.execute("""
            INSERT INTO pedido_produto (pedido_id, produto_id, quantidade)
            VALUES (?, ?, ?)
        """, (pedido_id, produto_id, quantidade))
    for ingrediente_id, quantidade in ingredientes:
        cursor.execute("""
            INSERT INTO pedido_ingrediente (pedido_id, ingrediente_id, quantidade)
            VALUES (?, ?, ?)
        """, (pedido_id, ingrediente_id, quantidade))
    conn.commit()
    conn.close()

def inserir_produtos_ficticios():
    produtos = [
        ("Café Expresso", 5.00),
        ("Cappuccino", 7.50),
        ("Pão de Queijo", 4.00),
        ("Bolo de Chocolate", 6.50),
        ("Suco Natural", 5.50),
        ("Croissant", 6.00)
    ]
    conn = sqlite3.connect('projeto.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        for nome, preco in produtos:
            cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
        conn.commit()
    conn.close()


inserir_produtos_ficticios()


