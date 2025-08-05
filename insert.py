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

with open('schema.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()
cursor.executescript(sql)

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

conn.commit()
conn.close()
print("Tabelas criadas e gerentes iniciais cadastrados com sucesso!")
