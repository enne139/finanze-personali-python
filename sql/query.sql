CREATE TABLE IF NOT EXISTS conti (
    uuid_conto CHAR(32) PRIMARY KEY,
    nome_conto VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categorie (
    uuid_categoria CHAR(32) PRIMARY KEY,
    nome_categoria VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transazioni (
    uuid_transazione CHAR(32) PRIMARY KEY,
    data_transazione DATE NOT NULL,
    importo REAL NOT NULL,
    descrizione TEXT NOT NULL,
    uuid_conto CHAR(32),
    uuid_categoria CHAR(32),
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uuid_conto) REFERENCES conti,
    FOREIGN KEY (uuid_categoria) REFERENCES categorie
);

CREATE TRIGGER IF NOT EXISTS modifica_conto
AFTER UPDATE ON conti
FOR EACH ROW
BEGIN
    UPDATE conti
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_conto = NEW.uuid_conto;
END;

CREATE TRIGGER IF NOT EXISTS modifica_categorie
AFTER UPDATE ON categorie
FOR EACH ROW
BEGIN
    UPDATE categorie
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_categoria = NEW.uuid_categoria; 
END;

CREATE TRIGGER IF NOT EXISTS modifica_transazioni
AFTER UPDATE ON transazioni
FOR EACH ROW
BEGIN
    UPDATE transazioni
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_transazione=NEW.uuid_transazione; 
END;