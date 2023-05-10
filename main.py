from GUI import GUI
from API import API
from sys import argv

def main():
    t = argv[0].split("\\")
    dirMain = ""
    while len(t) > 2:
        dirMain = dirMain + f"{t.pop(0)}\\"
    dirMain = dirMain + f"{t[0]}"
    print("La direccion de main es:", dirMain)
    api = API(dirMain)
    if not api.BDencendida:
        print("No existe la base de datos")        
        if not GUI.preguntaPrimeraVez():
            GUI.muestraError("No se ha encontrado la base de datos")
            return -1
        else:
            api.iniciaDB(forzado=True)
            print("Se ha creado la base de datos")
    else: print("Existe la base de datos")
    gui = GUI(api)
    gui.exec_()



if __name__ == "__main__":
    main()