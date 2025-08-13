# insert.py
import sqlite3
from werkzeug.security import generate_password_hash

GERENTES = [
    {
        'nome': 'Rita',
        'email': 'rita.gerente@reliercafe.com',
        'telefone': '(11) 99999-1111',
        'categoria': 'gerente',
        'senha': 'SenhaSegura123'
    },
    {
        'nome': 'Isabelle',
        'email': 'isabelle.gerente@reliercafe.com',
        'telefone': '(11) 99999-2222',
        'categoria': 'gerente',
        'senha': 'SenhaSegura123'
    },
    {
        'nome': 'Ezaelly',
        'email': 'ezaelly.gerente@reliercafe.com',
        'telefone': '(11) 99999-3333',
        'categoria': 'gerente',
        'senha': 'SenhaSegura123'
    },
    {
        'nome': 'Raissa',
        'email': 'raissa.gerente@reliercafe.com',
        'telefone': '(11) 99999-4444',
        'categoria': 'gerente',
        'senha': 'SenhaSegura123'
    }
]

PRODUTOS = [
    {'nome': 'Espresso', 'preco': 6.50},
    {'nome': 'Cappuccino', 'preco': 9.90},
    {'nome': 'Latte', 'preco': 10.50},
    {'nome': 'Mocha', 'preco': 12.00},
    {'nome': 'Café Preto', 'preco': 5.00},
    {'nome': 'Chá Gelado', 'preco': 8.00},
    {'nome': 'Croissant', 'preco': 7.50},
    {'nome': 'Bolo de Chocolate', 'preco': 9.00},
    {'nome': 'Sanduíche Natural', 'preco': 12.50},
    {'nome': 'Água Mineral', 'preco': 4.00}
]

INGREDIENTES = [
    {'nome': 'Café em grãos', 'custo': 0.50},
    {'nome': 'Leite', 'custo': 0.30},
    {'nome': 'Chocolate', 'custo': 0.80},
    {'nome': 'Açúcar', 'custo': 0.10},
    {'nome': 'Farinha', 'custo': 0.20},
    {'nome': 'Ovos', 'custo': 0.40}
]

with open('schema.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()
cursor.executescript(sql)

# Cadastra gerentes
for gerente in GERENTES:
    hash_senha = generate_password_hash(gerente['senha'])
    cursor.execute("""
        INSERT INTO funcionarios (nome, email, telefone, categoria, senha_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (
        gerente['nome'],
        gerente['email'],
        gerente['telefone'],
        gerente['categoria'],
        hash_senha
    ))

# Cadastra produtos
for produto in PRODUTOS:
    cursor.execute("""
        INSERT INTO produtos (nome, preco)
        VALUES (?, ?)
    """, (
        produto['nome'],
        produto['preco']
    ))

# Cadastra ingredientes
for ingrediente in INGREDIENTES:
    cursor.execute("""
        INSERT INTO ingredientes (nome, custo)
        VALUES (?, ?)
    """, (
        ingrediente['nome'],
        ingrediente['custo']
    ))

conn.commit()
conn.close()
