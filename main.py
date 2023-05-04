import sqlite3
from sqlite3 import Error
import uuid

class ConnDB:
    
    conn = None

    def __init__(self, urlDB):
        try:
            self.conn = sqlite3.connect(urlDB)
        except Error as e:
            raise e

    def close(self):
        if self.conn:
            self.conn.close()

    def executeCommit(self, query, parms=()):
        try:
            cur = self.conn.cursor()
            cur.execute(query, parms)
            self.conn.commit()
            return cur.lastrowid
        except Error as e:
            raise e

    def execute(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except Error as e:
            raise e
        
    def executeFetchAll(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Error as e:
            raise e

class FinanzeDB(ConnDB):

#------------------------------------------------------
# utilita
#------------------------------------------------------

    def creaTabelle(self):
        self.execute("""
CREATE TABLE conti (
    uuid_conto CHAR(32) PRIMARY KEY,
    nome_conto VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);
            """)

    def creaTabelle(self):
        self.execute("""
CREATE TABLE categorie (
    uuid_categoria CHAR(32) PRIMARY KEY,
    nome_categoria VARCHAR(31) NOT NULL UNIQUE,
    ultima_modifica DATETIME DEFAULT CURRENT_TIMESTAMP
);
            """)
        

    def creaTabelle(self):
        self.execute("""
CREATE TABLE transazioni (
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
        
    def creaTabelle(self):
        self.execute("""
CREATE TRIGGER modifica_conto
AFTER UPDATE ON conti
FOR EACH ROW
BEGIN
    UPDATE conti
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_conto = NEW.uuid_conto;
END;
            """)
        
    def creaTabelle(self):
        self.execute("""
CREATE TRIGGER modifica_categorie
AFTER UPDATE ON categorie
FOR EACH ROW
BEGIN
    UPDATE categorie
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_categoria = NEW.uuid_categoria; 
END;
            """)
        
    def creaTabelle(self):
        self.execute("""
CREATE TRIGGER modifica_transazioni
AFTER UPDATE ON transazioni
FOR EACH ROW
BEGIN
    UPDATE transazioni
    SET ultima_modifica = CURRENT_TIMESTAMP
    WHERE uuid_transazione=NEW.uuid_transazione; 
END;
            """)
        
#------------------------------------------------------
# get categorie
#------------------------------------------------------

    def getCategoriaByUUID(self, uuid):
        result = self.executeFetchAll("SELECT uuid_categoria, nome_categoria FROM categorie WHERE uuid_categoria=?;", (uuid))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getCategoriaByNome(self, nome):
        result = self.executeFetchAll("SELECT uuid_categoria, nome_categoria FROM categorie WHERE nome_categoria=?;", (nome))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getAllCategorie(self):
        return self.executeFetchAll("SELECT uuid_categoria, nome_categoria FROM categorie;")

#------------------------------------------------------
# get categorie
#------------------------------------------------------

    def getContoByUUID(self, uuid):
        result = self.executeFetchAll("uuid_conto, nome_conto FROM conti WHERE uuid_conto=?;", (uuid))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getContoByNome(self, nome):
        result = self.executeFetchAll("uuid_conto, nome_conto FROM conti WHERE nome_conto=?;", (nome))
        if len(result) == 0:
            return False
        else:
            return result[0]

    def getAllConti(self):
        return self.executeFetchAll("SELECT uuid_conto, nome_conto FROM conti;")

#------------------------------------------------------
# get transazioni
#------------------------------------------------------
   

#------------------------------------------------------
# inserimenti
#------------------------------------------------------


    def insertConto(self, nome):
        self.executeCommit("INSERT INTO conti(uuid_conto, nome_conto) VALUES (?, ?);", (uuid.uuid4().hex,nome))

    def insertCategoria(self, nome):
        self.executeCommit("INSERT INTO categorie(uuid_categoria, nome_categoria) VALUES (?, ?);", (uuid.uuid4().hex,nome))

    def insertTransazione(self, data, importo, descizione, uuid_conto, uuid_categoria):
        self.executeCommit("INSERT INTO transazioni( uuid_transazione, data_transazione, importo, descrizione, uuid_conto, uuid_categoria) VALUES (?, ?, ?, ?, ?, ?);", (uuid.uuid4().hex, data, importo, descizione, uuid_conto, uuid_categoria))


FinanzeDB = ConnDB("database/database.sqlite")

FinanzeDB.close()

