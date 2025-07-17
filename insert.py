import sqlite3

conexao_banco = sqlite3.connect('banco.db')
SCHEMA = 'schema.sql'

with open(SCHEMA) as f:
    conexao_banco.executescript(f.read())

conexao_banco.close()


