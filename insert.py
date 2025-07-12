import sqlite3

# insert

conexao_do_banco = sqlite3.connect('banco.db')

SQL = 'INSERT INTO users(nome) VALUES (?)'

nome = 'Teste'

conexao_do_banco.execute(SQL, (nome, ))
conexao_do_banco.commit()

conexao_do_banco.close()