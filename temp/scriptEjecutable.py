from os import path, system, remove
from shutil import rmtree, copy, copytree

# pyinstaller main.py --onefile --noconsole --icon=temp\icono.ico

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

DIR_MAIN = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\main.py"

DIR_ICONO = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\temp\\icono.ico"

DIR_DIST = "C:\\Pablo\\Casa\\Programacion\\Gimnasio\\dist"

def main():
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
    # Ejecutamos para generar el exe
    system(f"pyinstaller {DIR_MAIN} --onefile --noconsole --icon={DIR_ICONO}")
    # Copiamos el resto de archivos
    for arch in ARCHIVOS:
        copy(arch[0], DIR_DIST+arch[1])
    for dir in CARPETAS:
        copytree(dir[0], DIR_DIST+dir[1])

if __name__ == "__main__":
    main()