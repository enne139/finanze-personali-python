from classi.FinanzeDB import FinanzeDB

finanzeDB = FinanzeDB("database/database.sqlite")

valore = "3c08c308b6e5426a9646eb87517b4a1b"

print(finanzeDB.getCategoriaByNome("giroconto"))

finanzeDB.close()

