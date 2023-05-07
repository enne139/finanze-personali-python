from classi.FinanzeDB import FinanzeDB

from config import pathDB

finanzeDB = FinanzeDB(pathDB)

#finanzeDB.insertConto("hype")

with open("database/contanti", "r") as file1:
    for line in file1.read().split("\n"):
        line = line.split(";")

        print(line)

        uuid_conto = finanzeDB.getContoByNome("contanti")[0]

        uuid_categoria = finanzeDB.getCategoriaByNome(line[2])
        if uuid_categoria == False:
            finanzeDB.insertCategoria(line[2])
            uuid_categoria = finanzeDB.getCategoriaByNome(line[2]) [0]
        else:
            uuid_categoria = uuid_categoria[0]


        finanzeDB.insertTransazione(str(line[0]), float(line[1]), str(line[3]), uuid_conto, uuid_categoria)



finanzeDB.close()

