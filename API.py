from sqlite3 import connect
from fecha import Fecha
from pprint import pprint
from sys import argv
from os import path


class Constantes():
    def __init__(self, dirrecionIni) -> None:
        self.DIR_PROGRAMA = dirrecionIni
        self.DIR_DB = f"{self.DIR_PROGRAMA}\\DB"
        self.DIR_DB_PRUEBA = f"{self.DIR_PROGRAMA}\\DBtest"
        self.DIR_SCRIPT_DB = f"{self.DIR_PROGRAMA}\\scriptSQL.sql"
        self.DIR_IMAGENES = f"{self.DIR_PROGRAMA}\\images"
        self.MUSCULOS = ["Pecho", "Hombro", "Espalda", "Biceps", 
                    "Triceps", "Pierna", "Gemelo"]

class API():

    def __init__(self, dirMain:str, test:bool=False):
        self.constantes = Constantes(dirMain)
        self.test = test
        if test:
            if path.exists(self.constantes.DIR_DB_PRUEBA): 
                self.database = connect(self.constantes.DIR_DB_PRUEBA)
                self.BDencendida = True
            else: self.BDencendida = False
        else: 
            if path.exists(self.constantes.DIR_DB):
                self.database = connect(self.constantes.DIR_DB)
                self.BDencendida = True
            else: self.BDencendida = False
        if self.BDencendida:
            self.cursor = self.database.cursor()
        self.musculos = {}
        for i, m in enumerate(self.constantes.MUSCULOS): self.musculos[i+1] = m

    def iniciaDB(self, forzado:bool = False):
        if not forzado and input("Estas seguro de reiniciar la bd(s): ") != "s":
            print("Se ha cancelado el reinicio")
            return 0
        if not self.BDencendida:
            if self.test: self.database = connect(self.constantes.DIR_DB_PRUEBA)            
            else: self.database = connect(self.constantes.DIR_DB)
            self.BDencendida = True
            self.cursor = self.database.cursor()
        with open(self.constantes.DIR_SCRIPT_DB, "r") as file: script = file.read()
        self.database.executescript(script)
        for m in self.constantes.MUSCULOS:
            self.cursor.execute(f"insert into Musculo values (null, '{m}')")
        self.database.commit()

    def versionBD(self):
        try:
            self.cursor.execute("select max(version) from version")
            return self.cursor.fetchall()[0][0]
        except: return "No hay version"

    def anhadeEjercicio(self, idMusculo:int, nombre:str):
        if idMusculo not in self.musculos.keys(): raise ValueError("Incorrect musculo id")
        self.cursor.execute(f"select * from Ejercicio where Nombre = '{nombre}'")
        if len(self.cursor.fetchall()) != 0: raise ValueError("The ejercicio is already in the database")
        self.cursor.execute(f"insert into Ejercicio values (null, {idMusculo}, '{nombre}')")
        self.cursor.execute("select * from V_Ult_Ejercicio")
        self.database.commit()
        return self.cursor.fetchall()[0][0]

    def obtenEjercicio(self, id:int =None):
        if id is None: self.cursor.execute("select * from V_Ejercicio")
        else:
            if type(id) != int: raise TypeError("The type of the id is no a int")
            self.cursor.execute(f"select * from V_Ejercicio where ID = {id}")
            return [{"idEjercicio":i, "nomEjercicio":n, "idMusculo":m, "nomMusculo":k} for i, n, m, k in self.cursor.fetchall()]
    
    def eliminaEjercicio(self, id:int):
        self.cursor.execute(f"select * from Ejercicio where ID = {id}")
        d = self.cursor.fetchall()
        if len(d) == 0: raise ValueError("The ejercicio does not exist")
        self.cursor.execute(f"delete from Ejercicio where ID = {id}")
        self.database.commit()
        for id, idMus, Nom in d:
            return {"id":id, "idMusculo":idMus, "nombre":Nom}

    def anahadeEntrenamiento(self, fecha:str):
        try: fecha = Fecha.sql(fecha)
        except: raise TypeError("The format of the date is incorrect")
        self.cursor.execute(f"insert into Entrenamiento values (null, '{fecha.formatoSQL()}')")
        self.cursor.execute("select * from V_Ult_Entrenamiento")
        self.database.commit()
        return self.cursor.fetchall()[0][0]
    
    def eliminaEntrenamiento(self, idEntrenamiento:int):
        self.cursor.execute(f"select Fecha from Entrenamiento where ID = {idEntrenamiento}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The Entrenamiento does not exist")
        self.cursor.execute(f"delete from Serie where ID_Entreamiento = {idEntrenamiento}")
        self.cursor.execute(f"delete from Entrenamiento where ID = {idEntrenamiento}")
        self.database.commit()

    def obtenEntrenamiento(self, id:int =None):
        if id is None: self.cursor.execute("select * from V_Entrenamiento")
        else:
            if type(id) != int: raise TypeError("The type of the id is not a int")
            self.cursor.execute(f"select * from V_Entrenamiento where ID_Entrenamiento = {id}")
        return [{"idEntrenamiento":e, "ejerNombre":n, "idMusculo":m, "peso":p, "repeticiones":r, "tipo":t} for e, n, m, p, r, t in self.cursor.fetchall()]
    
    def obtenEntrenamientosDeMusculo(self, id:int):
        if id not in self.musculos.keys(): raise ValueError("Incorrect musculo id")
        self.cursor.execute(f"select * FROM V_Ejercicio where IDMusculo = {id}")
        return self.cursor.fetchall()
    
    def anhadeSeries(self, listaSeries:list[int, int, float, int, str]): #idEjercicio, idEntrenamiento, peso, repeticiones, tipo
        for idEjercicio, idEntrenamiento, peso, repeticiones, tipo in listaSeries:
            self.cursor.execute(f"insert into Serie values (null, {idEjercicio}, {idEntrenamiento}, {peso}, {repeticiones}, '{tipo}')")
        self.database.commit()

    def obtenUltEntrenosEjer(self, idEjer:int):
        self.cursor.execute("select ID from Ejercicio")
        d = map(lambda x: x[0], self.cursor.fetchall())
        if idEjer not in d: raise ValueError("Incorrect ejercicio id")
        self.cursor.execute(f"SELECT * FROM V_Ult_Entrenos_Ejercicio where IDEjer = {idEjer}")
        d = self.cursor.fetchall()
        ant = -1
        for i in reversed(range(len(d))):
            if ant == d[i][0]: 
                del d[i]
            else: 
                ant = d[i][0]
        return [{"idEntr":e, "fecha":f, "idEjer":i} for e, f, i in d]
    
    def nombreEjerValido(self, nombEjer:str):
        self.cursor.execute(f"select ID from Ejercicio where Nombre = '{nombEjer}'")
        return len(self.cursor.fetchall()) == 0 and nombEjer != ""
    
    def anahdeRutina(self, nombre:str, listaEjer:list[int, int]): #listaEjer[idEjer, numSeries]
        self.cursor.execute("select Nombre from Rutina")
        d = map(lambda x: x[0], self.cursor.fetchall())
        if nombre in d: raise ValueError("The nombre already exists")
        self.cursor.execute(f"insert into Rutina values (null, '{nombre}')")
        self.cursor.execute("select * from V_Ult_Rutina")
        idRut = self.cursor.fetchall()[0][0]
        self.cursor.execute("select ID from Ejercicio")
        d = map(lambda x: x[0], self.cursor.fetchall())
        for idEjer, numSer in listaEjer:
            if idEjer not in d: raise ValueError(f"The idEjer {idEjer} does not exist")
            self.cursor.execute(f"insert into EjerRutina values (null, {idRut}, {idEjer}, {numSer})")
        self.database.commit()
        return idRut
    
    def eliminaRutina(self, idRutina:int):
        self.cursor.execute(f"select ID from Rutina where ID = {idRutina}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The ID does not exist")
        self.cursor.execute(f"delete from EjerRutina where ID_Rutina = {idRutina}")
        self.cursor.execute(f"delete from Rutina where ID = {idRutina}")
        self.database.commit()

    def eliminaEjercicioRutina(self, idRutina:int, idEjercicio:int):
        self.cursor.execute(f"select ID from Rutina where ID = {idRutina}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The ID does not exist")
        self.cursor.execute(f"select ID_Rutina from V_Rutinas where ID_Rutina = {idRutina} and ID_Ejercicio = {idEjercicio}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The rutine does not have the execise")
        self.cursor.execute(f"delete from EjerRutina where ID_Rutina = {idRutina} and ID_Ejercicio = {idEjercicio}")
        self.database.commit()

    def fijaSeriresEjercicioRutina(self, numSeries:int ,idRutina:int, idEjercicio:int):
        self.cursor.execute(f"select ID from Rutina where ID = {idRutina}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The ID does not exist")
        self.cursor.execute(f"select ID_Rutina from V_Rutinas where ID_Rutina = {idRutina} and ID_Ejercicio = {idEjercicio}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The rutine does not have the execise")
        if numSeries == None: numSeries = "null"
        self.cursor.execute(f"update EjerRutina set Series = {numSeries} where ID_Rutina = {idRutina} and ID_Ejercicio = {idEjercicio}")
        self.database.commit()

    def anhadeEjercicioRutina(self, idRutina:int, idEjercicio:int):
        self.cursor.execute(f"select ID from Rutina where ID = {idRutina}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The rutine does not exist")
        self.cursor.execute(f"select ID from Ejercicio where ID = {idEjercicio}")
        if len(self.cursor.fetchall()) == 0: raise ValueError("The execise does not exist")
        self.cursor.execute(f"insert into EjerRutina values (null, {idRutina}, {idEjercicio}, null)")

    def obtenRutina(self, idRutina:int =None):
        if idRutina is not None:
            self.cursor.execute(f"select Nombre from Rutina where ID = {idRutina}")
            d = self.cursor.fetchall()
            if len(d) == 0: raise ValueError("The ID is incorrect")
            resp = {"id":idRutina, "nombre": d[0][0], "ejercicios":[]}
            self.cursor.execute(f"select * from V_Rutinas where ID_Rutina = {idRutina} order by ID_Union")
            d = self.cursor.fetchall()
            if len(d) == 0: return resp
            for idRut, nomRut, idEjer, nomEjer, numSer, idUnion in d:
                resp["ejercicios"].append({"idEjer":idEjer, "nomEjer":nomEjer, "numSer":numSer})
            return resp
        else:
            self.cursor.execute("select * from Rutina")
            datos = self.cursor.fetchall()
            idRutinas = set(map(lambda x: x[0], datos))
            lista = []
            for idRut in idRutinas:
                lista.append(self.obtenRutina(idRut))
            return lista
                


if __name__ == "__main__":
    dirM = __file__[:-7]
    if len(argv) > 1:
        if argv[1] == "-v":
            t = API(dirM, test=True)
            print(f"Verison test: {t.versionBD()}")
            n = API(dirM, test=False)
            print(f"Version normal: {n.versionBD()}")            
    else:
        a = API(dirM, test=True)
        a.iniciaDB()
        ejer = a.anhadeEjercicio(1, "Crull de biceps")
        ejer = a.anhadeEjercicio(1, "Peso muerto rumano")
        ejer = a.anhadeEjercicio(1, "c")
        ejer = a.anhadeEjercicio(1, "d")
        ejer = a.anhadeEjercicio(1, "e")
        ejer = a.anhadeEjercicio(1, "f")
        ejer = a.anhadeEjercicio(1, "g")
        ejer = a.anhadeEjercicio(1, "h")
        ejer = a.anhadeEjercicio(1, "i")
        ejer = a.anhadeEjercicio(1, "j")
        ejer = a.anhadeEjercicio(1, "k")
        ejer = a.anhadeEjercicio(1, "l")
        ejer = a.anhadeEjercicio(1, "m")
        ejer = a.anhadeEjercicio(1, "n")
        ejer = a.anhadeEjercicio(1, "o")
        ejer = a.anhadeEjercicio(1, "p")
        ejer = a.anhadeEjercicio(1, "q")
        ejer = a.anhadeEjercicio(1, "r")
        ejer = a.anhadeEjercicio(1, "s")
        ejer = 1
        entre = a.anahadeEntrenamiento("2023-5-12")
        a.anhadeSeries([
            (ejer, entre, 20, 12, "n"),
            (ejer, entre, 20, 11, "n"),
            (ejer, entre, 20, 10, "n"),
            (ejer, entre, 20, 8, "n")
        ])
        entre = a.anahadeEntrenamiento("2023-5-10")
        a.anhadeSeries([(ejer, entre, 20, 12, "n")])
        entre = a.anahadeEntrenamiento("2023-5-13")
        a.anhadeSeries([(ejer, entre, 20, 12, "n")])
        entre = a.anahadeEntrenamiento("2023-5-11")
        a.anhadeSeries([(ejer, entre, 20, 12, "n")])
        entre = a.anahadeEntrenamiento("2023-5-14")
        a.anhadeSeries([(ejer, entre, 20, 12, "n")])
        entre = a.anahadeEntrenamiento("2023-5-15")
        a.anhadeSeries([(ejer, entre, 20, 12, "n")])
        a.anhadeSeries([(ejer+1, entre, 20, 12, "n")])
        pprint(a.obtenEntrenamientosDeMusculo(1))
        print(a.obtenUltEntrenosEjer(ejer))
        print(len(a.obtenUltEntrenosEjer(ejer)))
        print(a.nombreEjerValido(""))
        print(a.nombreEjerValido("s"))
        print(a.nombreEjerValido("t"))
        rut = a.anahdeRutina("nombreRutina1", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina2", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina3", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina4", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina5", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina6", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina7", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina8", [(1,5), (2,6)])
        rut = a.anahdeRutina("nombreRutina9", [(1,5), (2,6), (3,3), (4,4), (5,5), (6,6), (7,7)])
        pprint(a.obtenRutina())
        a.eliminaEjercicioRutina(1, 2)