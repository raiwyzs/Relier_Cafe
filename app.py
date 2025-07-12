import sqlite3
from flask import *

app = Flask(__name__)

conexao_do_banco = sqlite3.connect('banco.db')
SCHEMA = 'schema.sql'

with open(SCHEMA) as f:
    conexao_do_banco.executescript(f.read())

conexao_do_banco.close()

@app.route('/')
def home():
    return render_template('index.html')
