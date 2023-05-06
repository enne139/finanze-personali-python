from flask import Flask
from flask import render_template
from flask import request

from classi.FinanzeDB import FinanzeDB

from config import pathDB

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
@app.route("/home.html", methods=["POST", "GET"])
def home():

    lista_categorie = []
    lista_conti = []

    out = []
    out2 = []

    lista_GBtot_cat = []
    lista_GBtot_val = []

    lista_GBmes_cat = []
    lista_GBmes_val = []

    errore = None

    try:
        finanzeDB = FinanzeDB(pathDB)

        lista_categorie = finanzeDB.getAllCategorie()
        lista_conti = finanzeDB.getAllConti()

        finanzeDB.close()
    except Exception as e:
        errore = str(e)

    Sconto = request.args.get('Sconto')

    if Sconto is not None and Sconto!="-1":
        try:
            finanzeDB = FinanzeDB(pathDB)

            out = finanzeDB.executeFetchAll("""
SELECT 
    SUM(T.importo),
    categorie.nome_categoria AS categoria
FROM transazioni AS T
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
WHERE T.uuid_conto=?
GROUP BY T.uuid_categoria
                """, (Sconto,))

            out2 = finanzeDB.executeFetchAll("""
SELECT 
    SUM(T.importo),
    categorie.nome_categoria AS categoria
FROM transazioni AS T
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
WHERE T.uuid_conto=? AND date('now','start of month','-1 days') < T.data_transazione
GROUP BY T.uuid_categoria
                """, (Sconto,))

            finanzeDB.close()
        except Exception as e:
            errore = str(e)
    else:
        try:
            finanzeDB = FinanzeDB(pathDB)

            out = finanzeDB.executeFetchAll("""
SELECT 
    SUM(T.importo),
    categorie.nome_categoria AS categoria
FROM transazioni AS T
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
GROUP BY T.uuid_categoria
                """)
            
            out2 = finanzeDB.executeFetchAll("""
SELECT 
    SUM(T.importo),
    categorie.nome_categoria AS categoria
FROM transazioni AS T
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
WHERE date('now','start of month','-1 days') < T.data_transazione
GROUP BY T.uuid_categoria
                """)

            finanzeDB.close()
        except Exception as e:
            errore = str(e)

    for row in out:
        lista_GBtot_cat.append(row[1])
        lista_GBtot_val.append(row[0])

    for row in out2:
        lista_GBmes_cat.append(row[1])
        lista_GBmes_val.append(row[0])

    return render_template("home.html",                             
                            errore=errore, 
                            lista_categorie=lista_categorie, 
                            lista_conti=lista_conti,
                            lista_GBtot_cat=lista_GBtot_cat,
                            lista_GBtot_val=lista_GBtot_val,
                            lista_GBmes_cat=lista_GBmes_cat,
                            lista_GBmes_val=lista_GBmes_val
                            )

@app.route("/inserimento.html", methods=["POST", "GET"])
def inserimento():

    lista_categorie = []
    lista_conti = []

    errore = None
    successo = None

    if request.method == 'POST':
        if "creaGiroconto" in request.form:
            data = request.form["data"]
            importo = request.form["importo"]
            contoS = request.form["contoS"]
            contoD = request.form["contoD"]

            try:
                finanzeDB = FinanzeDB(pathDB)

                print(contoD)

                nomeD = finanzeDB.getContoByUUID(contoD)[1]
                nomeS = finanzeDB.getContoByUUID(nomeS)[1]
                uuidC = finanzeDB.getCategoriaByNome( "giroconto" )[0]

                finanzeDB.insertTransazione(data, -float(importo), "giroconto verso " + nomeD, contoS, uuidC )
                finanzeDB.insertTransazione(data, importo, "giroconto da " + nomeS, contoD, uuidC )

                finanzeDB.close()

                successo = "giroconto inserito"
            except Exception as e:
                errore = str(e)

        elif "creaCategoria" in request.form:
            nome = request.form["categoria"]

            try:
                finanzeDB = FinanzeDB(pathDB)

                finanzeDB.insertCategoria(nome)

                finanzeDB.close()

                successo = "categoria inserito"
            except Exception as e:
                errore = str(e)

        elif "creaConto" in request.form:
            nome = request.form["conto"]

            try:
                finanzeDB = FinanzeDB(pathDB)

                finanzeDB.insertConto(nome)

                finanzeDB.close()

                successo = "conto inserito"
            except Exception as e:
                errore = str(e)
        elif "creaTransazione" in request.form:
            importo = request.form["importo"]
            data = request.form["data"]
            conto = request.form["conto"]
            categoria = request.form["categoria"]
            descrizione = request.form["descrizione"]

            try:
                finanzeDB = FinanzeDB(pathDB)

                finanzeDB.insertTransazione(data,importo, descrizione, conto, categoria)

                finanzeDB.close()

                successo = "transazione inserito"
            except Exception as e:
                errore = str(e)

    try:
        finanzeDB = FinanzeDB(pathDB)

        lista_categorie = finanzeDB.getAllCategorie()
        lista_conti = finanzeDB.getAllConti()

        finanzeDB.close()
    except Exception as e:
        errore = str(e)

    return render_template("inserimento.html", successo=successo, errore=errore, lista_categorie=lista_categorie, lista_conti=lista_conti)

@app.route("/lista.html", methods=["POST", "GET"])
def lista():

    lista_categorie = []
    lista_conti = []

    lista_tabella = []
    lista_colonne = []
    lista_indici = []

    errore = None

    try:
        finanzeDB = FinanzeDB(pathDB)

        lista_categorie = finanzeDB.getAllCategorie()
        lista_conti = finanzeDB.getAllConti()

        finanzeDB.close()
    except Exception as e:
        errore = str(e)

    Sconto = request.args.get('Sconto')
    Scategoria = request.args.get('Scategoria')
    SdataI = request.args.get('SdataI')
    SdataF = request.args.get('SdataF')
    Snum = request.args.get('Snum')
    SpagC = request.args.get('SpagC')
    Bfiltra = request.args.get('Bfiltra')

    if Sconto is not None and Sconto!="-1":
        try:
            finanzeDB = FinanzeDB(pathDB)

            lista_colonne = ["data_transazione", "importo", "descrizione", "categoria"]
            lista_indici = [1, 2, 3, 5]

            lista_tabella = finanzeDB.executeFetchAll("""
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
WHERE T.uuid_conto=?
ORDER BY T.data_transazione DESC
                """, (Sconto,))

            finanzeDB.close()
        except Exception as e:
            errore = str(e)
    else:
        try:
            finanzeDB = FinanzeDB(pathDB)

            lista_colonne = ["data_transazione", "importo", "descrizione", "conto", "categoria"]
            lista_indici = [1, 2, 3, 4, 5]

            lista_tabella = finanzeDB.executeFetchAll("""
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
ORDER BY T.data_transazione DESC
                """)

            finanzeDB.close()
        except Exception as e:
            errore = str(e)

    return render_template("lista.html", 
                            errore=errore, 
                            lista_categorie=lista_categorie, 
                            lista_conti=lista_conti, 
                            lista_tabella=lista_tabella, 
                            lista_colonne=lista_colonne, 
                            lista_indici=lista_indici
                        )