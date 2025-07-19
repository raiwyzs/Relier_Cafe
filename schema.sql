DROP TABLE IF EXISTS funcionarios;

CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    categoria TEXT NOT NULL,
    senha TEXT NOT NULL
);
