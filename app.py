from flask import Flask
from flask import render_template
from flask import request

from classi.FinanzeDB import FinanzeDB

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

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
                finanzeDB = FinanzeDB("database/database.sqlite")

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
                finanzeDB = FinanzeDB("database/database.sqlite")

                finanzeDB.insertCategoria(nome)

                finanzeDB.close()

                successo = "categoria inserito"
            except Exception as e:
                errore = str(e)

        elif "creaConto" in request.form:
            nome = request.form["conto"]

            try:
                finanzeDB = FinanzeDB("database/database.sqlite")

                finanzeDB.insertConto(nome)

                finanzeDB.close()

                successo = "conto inserito"
            except Exception as e:
                errore = str(e)

    try:
        finanzeDB = FinanzeDB("database/database.sqlite")

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

    errore = None

    try:
        finanzeDB = FinanzeDB("database/database.sqlite")

        lista_categorie = finanzeDB.getAllCategorie()
        lista_conti = finanzeDB.getAllConti()

        finanzeDB.close()
    except Exception as e:
        errore = str(e)

    return render_template("lista.html", errore=errore, lista_categorie=lista_categorie, lista_conti=lista_conti)