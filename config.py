import platform

def pathConverterDB():
    if platform.system()=="Linux":
        return "database/database.sqlite"
    elif platform.system()=="Windows":
        return "database\database.sqlite"
    else:
        return "database/database.sqlite"

pathDB = pathConverterDB()

