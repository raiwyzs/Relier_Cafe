-- schema.sql
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT NOT NULL,
    categoria TEXT NOT NULL,
    senha_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    forma_pagamento TEXT NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    custo REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido_ingrediente (
    pedido_id INTEGER NOT NULL,
    ingrediente_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    PRIMARY KEY (pedido_id, ingrediente_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);
