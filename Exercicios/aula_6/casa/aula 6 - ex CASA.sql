CREATE TABLE categoria (
    id INTEGER NOT NULL,
    nome VARCHAR NOT NULL,
    cor VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE bagulho (
    id INTEGER NOT NULL,
    nome VARCHAR NOT NULL,
    imagem VARCHAR,
    score INTEGER NOT NULL,
    categoria_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(categoria_id) REFERENCES categoria (id)
);