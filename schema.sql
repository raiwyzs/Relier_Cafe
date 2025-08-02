DROP TABLE IF EXISTS funcionarios;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS pedido_produto;
DROP TABLE IF EXISTS ingredientes;
DROP TABLE IF EXISTS pedido_ingrediente;

CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    categoria TEXT NOT NULL, -- cozinheiro, caixa, gerente
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

CREATE TABLE IF NOT EXISTS pedido_produto (
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE IF NOT EXISTS ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    custo REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido_ingrediente (
    pedido_id INTEGER,
    ingrediente_id INTEGER,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);
