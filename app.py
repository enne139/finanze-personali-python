from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime


from classi.FinanzeDB import FinanzeDB

from config import pathDB


finanzeDB = FinanzeDB(pathDB)
finanzeDB.creaTabelle()
finanzeDB.close()

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
@app.route("/home.html", methods=["POST", "GET"])
def home():

    errore = None

    liste = {}

    liste["tipologie"] = [ ["0", "analisi mensile"], ["1", "analisi annuale"], ["2", "analisi totale"] ]

    dati = {}

    dati["id_conto"] = "-1"
    dati["id_tipologia"] = "0"

    # estrazione elenco categorie e conti
    try:
        finanzeDB = FinanzeDB(pathDB)

        liste['categorie'] = finanzeDB.getAllCategorie()
        liste['conti'] = finanzeDB.getAllConti()

        finanzeDB.close()
    except Exception as e:
        return render_template("home.html", liste=liste, dati=dati,errore=str(e))

    # ottenimento parametro relativo al conto
    id_conto = request.args.get('Sconto')
    
    # controllo se esistente e non uguale a quello di default
    if id_conto is not None and id_conto!="-1":

        trovato = False

        # controlla se ha un valore di accettabile
        for row in liste["conti"]:
            if row[0]==id_conto:
                trovato = True
                break
        
        if not trovato:
            return render_template("home.html", liste=liste, dati=dati,errore="conto non valido")

        dati["id_conto"] = id_conto

    # ottenimento parametro relativo al tipologia vista
    id_tipologia = request.args.get('Stipologia')

    # controllo se esistente
    if id_tipologia is not None:

        trovato = False

        # controlla se ha un valore di accettabile
        for row in liste["tipologie"]:
            if row[0]==id_tipologia:
                trovato = True
                break
        
        if not trovato:
            return render_template("home.html", liste=liste, dati=dati,errore="vista non trovata non valido")

        dati["id_tipologia"] = id_tipologia

    if dati["id_tipologia"] == "0":
        dati["mese"] = datetime.today().strftime("%Y-%m")

        mese = request.args.get('Smese')

        if mese is not None:
            dati["mese"] = mese

        dati["GUsc"] = {"categorie" : [], "valori" : []}
        dati["GEnt"] = {"categorie" : [], "valori" : []}

        try:
            finanzeDB = FinanzeDB(pathDB)
            
            params = [ dati["mese"]+"-01",  dati["mese"]+"-01" ]
            query = """
SELECT  
    SUM(T.importo),
    categorie.nome_categoria AS categoria
FROM transazioni AS T
JOIN categorie ON categorie.uuid_categoria=T.uuid_categoria
WHERE date(?, 'start of month','-1 days') < T.data_transazione AND  T.data_transazione < date(?, 'start of month','+1 months')
"""
            if dati["id_conto"]!="-1" :
                query += """ AND T.uuid_conto=?"""
                params.append(dati["id_conto"])
            query +="""
GROUP BY T.uuid_categoria
""" 
            for row in finanzeDB.executeFetchAll(query, params):
                if row[0]>0:
                    dati["GEnt"]["categorie"].append(row[1])
                    dati["GEnt"]["valori"].append(row[0])
                else:
                    dati["GUsc"]["categorie"].append(row[1])
                    dati["GUsc"]["valori"].append(-row[0])

            finanzeDB.close()
        except Exception as e:
            return render_template("home.html", liste=liste, dati=dati,errore=str(e))
        
        dati["BUsc"] = {"giorni" : [], "valori" : []}
        dati["BEnt"] = {"giorni" : [], "valori" : []}

        gironi = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for i in range(1, gironi[(datetime.strptime(dati["mese"],'%Y-%m').month)-1]+1):
            dati["BUsc"]["giorni"].append(i)
            dati["BUsc"]["valori"].append(0)
            dati["BEnt"]["giorni"].append(i)
            dati["BEnt"]["valori"].append(0)

        if datetime.strptime(dati["mese"],'%Y-%m').month==2:
            dati["BUsc"]["giorni"].pop()
            dati["BUsc"]["valori"].pop()
            dati["BEnt"]["giorni"].pop()
            dati["BEnt"]["valori"].pop()

        try:
            finanzeDB = FinanzeDB(pathDB)
            
            params = [ dati["mese"]+"-01",  dati["mese"]+"-01" ]
            query = """
SELECT  
    SUM(T.importo),
    strftime("%d",data_transazione)
FROM transazioni AS T
WHERE date(?, 'start of month','-1 days') < T.data_transazione AND  T.data_transazione < date(?, 'start of month','+1 months') AND 
	T.importo > 0
"""
            if dati["id_conto"]!="-1" :
                query += """ AND T.uuid_conto=?"""
                params.append(dati["id_conto"])
            query +="""
GROUP BY T.data_transazione
""" 
            for row in finanzeDB.executeFetchAll(query, params):
                dati["BEnt"]["valori"][int(row[1])] = row[0]

            params = [ dati["mese"]+"-01",  dati["mese"]+"-01" ]
            query = """
SELECT  
    SUM(T.importo),
    strftime("%d",data_transazione)
FROM transazioni AS T
WHERE date(?, 'start of month','-1 days') < T.data_transazione AND  T.data_transazione < date(?, 'start of month','+1 months') AND 
	T.importo < 0
"""
            if dati["id_conto"]!="-1" :
                query += """ AND T.uuid_conto=?"""
                params.append(dati["id_conto"])
            query +="""
GROUP BY T.data_transazione
""" 

            for row in finanzeDB.executeFetchAll(query, params):
                dati["BUsc"]["valori"][int(row[1])] = -row[0]

            finanzeDB.close()
        except Exception as e:
            return render_template("home.html", liste=liste, dati=dati,errore=str(e))
        
        return render_template("components/analisiMensile.html", liste=liste, dati=dati, errore=errore)

    return render_template("home.html", liste=liste, dati=dati, errore="errore pagina errata")

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