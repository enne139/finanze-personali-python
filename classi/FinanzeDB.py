import sqlite3
from sqlite3 import Error
import uuid

from classi.ConnDB import ConnDB

class FinanzeDB(ConnDB):

#------------------------------------------------------
# utilita
#------------------------------------------------------

    def creaTabelle(self):
        self.execute("""
CREATE TABLE IF NOT EXISTS conti (
    uuid_conto CHAR(32) PRIMARY KEY,
    nome_conto VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);
            """)

        self.execute("""
CREATE TABLE IF NOT EXISTS categorie (
    uuid_categoria CHAR(32) PRIMARY KEY,
    nome_categoria VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);
            """)
        
        self.execute("""
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
            """)

        self.execute("""
CREATE TRIGGER IF NOT EXISTS modifica_conto
AFTER UPDATE ON conti
FOR EACH ROW
BEGIN
    UPDATE conti
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_conto = NEW.uuid_conto;
END;
            """)

        self.execute("""
CREATE TRIGGER IF NOT EXISTS modifica_categorie
AFTER UPDATE ON categorie
FOR EACH ROW
BEGIN
    UPDATE categorie
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_categoria = NEW.uuid_categoria; 
END;
            """)

        self.execute("""
CREATE TRIGGER IF NOT EXISTS modifica_transazioni
AFTER UPDATE ON transazioni
FOR EACH ROW
BEGIN
    UPDATE transazioni
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_transazione=NEW.uuid_transazione; 
END;
            """)
        
        if self.getCategoriaByNome("giroconto") == False:
            self.insertCategoria("giroconto")
        
#------------------------------------------------------
# get categorie
#------------------------------------------------------

    def getCategoriaByUUID(self, uuid):
        result = self.executeFetchAll("""
SELECT 
    uuid_categoria, 
    nome_categoria 
FROM 
    categorie 
WHERE 
    uuid_categoria=?;
            """, (uuid,))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getCategoriaByNome(self, nome):
        result = self.executeFetchAll("""
SELECT 
    uuid_categoria, 
    nome_categoria 
FROM 
    categorie 
WHERE 
    nome_categoria=?;
            """, (nome,))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getAllCategorie(self):
        return self.executeFetchAll("""
SELECT 
    uuid_categoria, 
    nome_categoria 
FROM 
    categorie;
            """)

#------------------------------------------------------
# get conto
#------------------------------------------------------

    def getContoByUUID(self, uuid):
        result = self.executeFetchAll("""
SELECT 
    uuid_conto, 
    nome_conto 
FROM 
    conti 
WHERE 
    uuid_conto=?;
            """, (uuid,))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getContoByNome(self, nome):
        result = self.executeFetchAll("""
SELECT 
    uuid_conto, 
    nome_conto 
FROM 
    conti 
WHERE nome_conto=?;
            """, (nome,))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getAllConti(self):
        return self.executeFetchAll("""
SELECT 
    uuid_conto, 
    nome_conto 
FROM 
    conti;
            """)

#------------------------------------------------------
# get transazioni
#------------------------------------------------------
   
    def getAllTransazioni(self):
        return self.executeFetchAll("""
SELECT uuid_transazione,
    data_transazione,
    importo,
    descrizione,
    uuid_conto,
    uuid_categoria
FROM transazioni
            """)
    
    def getAllTransazioniJoined(self):
        return self.executeFetchAll("""
SELECT 
	T.uuid_transazione,
    T.data_transazione,
    T.importo,
    T.descrizione,
	conti.nome_conto AS conto,
	categorie.nome_categoria AS categoria,
    T.uuid_conto,
    T.uuid_categoria
FROM transazioni AS T
JOIN conti ON conti.uuid_conto=T.uuid_conto
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
            """)

#------------------------------------------------------
# inserimenti
#------------------------------------------------------


    def insertConto(self, nome):
        self.executeCommit("""
INSERT INTO 
    conti(
        uuid_conto, 
        nome_conto
    ) 
VALUES 
    (?, ?);
            """, (uuid.uuid4().hex,nome))

    def insertCategoria(self, nome):
        self.executeCommit("""
INSERT INTO 
    categorie(
        uuid_categoria, 
        nome_categoria
    ) 
VALUES 
    (?, ?);
            """, (uuid.uuid4().hex,nome))

    def insertTransazione(self, data, importo, descizione, uuid_conto, uuid_categoria):
        self.executeCommit("""
INSERT INTO 
    transazioni( 
        uuid_transazione, 
        data_transazione, 
        importo, 
        descrizione, 
        uuid_conto, 
        uuid_categoria
    ) 
VALUES 
    (?, ?, ?, ?, ?, ?);
            """, (uuid.uuid4().hex, data, importo, descizione, uuid_conto, uuid_categoria))

#------------------------------------------------------
# modifiche
#------------------------------------------------------


    def updateConto(self, uuid_conto, nome):
        self.executeCommit("""
UPDATE conti
SET 
    nome_conto = ?
WHERE
    uuid_conto = ? 
            """, (nome, uuid_conto))

    def updateCategoria(self, uuid_categoria, nome):
        self.executeCommit("""
UPDATE categorie
SET 
    nome_categoria = ?
WHERE
    uuid_categoria = ? 
            """, (nome, uuid_categoria))

    def updateTransazione(self, uuid_transazione, data, importo, descizione, uuid_conto, uuid_categoria):
        self.executeCommit("""
UPDATE transazioni 
SET  
    data_transazione = ?,
    importo = ?,
    descrizione = ?,
    uuid_conto = ?,
    uuid_categoria = ?
WHERE
    uuid_transazione = ?;
            """, (data, importo, descizione, uuid_conto, uuid_categoria, uuid_transazione))

#------------------------------------------------------
# eliminazione
#------------------------------------------------------


    def deleteConto(self, uuid_conto):
        pass

    def deleteCategoria(self, uuid_categoria):
        pass

    def deleteTransazione(self, uuid_transazione):
        self.executeCommit("""
DELETE FROM 
    transazione
WHERE
    uuid_transazione = ?;
            """, (uuid_transazione))


