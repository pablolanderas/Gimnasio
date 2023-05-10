from os import path, system, remove, rename, chdir
from shutil import rmtree, copy, copytree
from sys import argv

DIR_MAIN = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\main.py"

DIR_ICONO = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\temp\\icono.ico"

DIR_DIST = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\dist"

DIR_PROYECTO = "C:\\Pablo\\Casa\\Programacion\\Gimnasio"

ARCHIVOS = [
    ("C:\\Pablo\\Casa\\Programacion\\Gimnasio\\scriptSQL.sql", "\\scriptSQL.sql")
]

CARPETAS = [
    ("C:\\Pablo\\Casa\\Programacion\\Gimnasio\\images", "\\images")
]

ELIMINAR = [
    "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\__pycache__",
    "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\build",
    "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\dist",
    "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\main.spec"
]

RENOMBRAR = [
    ("C:\\Pablo\\Casa\\Programacion\\Gimnasio\\dist\\main.exe", "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\dist\\Gimnasio.exe")
]

def main():
    argumentos = argv[1:]
    # Comprobamos si hay algun archivo incorrecto
    error = False
    for arch in ARCHIVOS:
        if not path.isfile(arch[0]):
            print(f"[ERROR]: El archivo {arch[0]} no existe")
            error = True
    for dir in CARPETAS:
        if not path.isdir(dir[0]):
            print(f"[ERROR]: La carpeta {dir[0]} no existe")
            error = True
    if error: return 0
    # Borramos los archivos en caso de existir
    for arch in ELIMINAR:
        if path.exists(arch):
            if path.isfile(arch): remove(arch)
            else: rmtree(arch)
    print("[INFO]: Se han eliminado los datos")
    if "-r" in argumentos: return 0
    # Ejecutamos para generar el exe
    chdir(DIR_PROYECTO)
    system(f"pyinstaller {DIR_MAIN} --onefile --noconsole --icon={DIR_ICONO}")
    # Copiamos el resto de archivos
    for arch in ARCHIVOS:
        copy(arch[0], DIR_DIST+arch[1])
    for dir in CARPETAS:
        copytree(dir[0], DIR_DIST+dir[1])
    print("[INFO]: Se han movido los datos")
    # Renombramos los archivos
    for nom, renom in RENOMBRAR:
        if path.isfile(nom): rename(nom, renom)
        else: print(f"[ERROR]: No se ha podido renombrar {nom}")
    print("[INFO]: Se han renombrado los datos")

if __name__ == "__main__":
    main()