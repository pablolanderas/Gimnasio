from API import API #TODO: Eliminar
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QScrollArea, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPixmap, QIcon, QFont, QIntValidator
from functools import partial
from fecha import Fecha
from API import Constantes

def espaciadorVertical(): return QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
def espaciadorHorizontal(): return QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
def estilo(tam:int): return QFont("Helvetica Now", tam)
def secuenciaFunciones(primera, segunda): 
    primera()
    segunda(None)
AZUL_CLARO = "background-color: rgb(205, 241, 239)"
AZUL_OSCURO = "background-color:rgb(151, 189, 189)"
def generaWidget(height:int=None, width:int=None, estilo:str=None):
    w = QWidget()
    if height is not None: w.setFixedHeight(height)
    if width is not None: w.setFixedWidth(width)
    if estilo is not None: w.setStyleSheet(estilo)
    return w
def generaLabel(texto:str=None, estilo:str=None, font:QFont=None,
                height:int=None, width:int=None, alineamiento=Qt.AlignCenter):
    lab = QLabel()
    if texto is not None: lab.setText(texto)
    if estilo is not None: lab.setStyleSheet(estilo)
    if font is not None: lab.setFont(font)
    if height is not None: lab.setFixedHeight(height)
    if width is not None: lab.setFixedWidth(width)
    lab.setAlignment(alineamiento)
    return lab
def generaScroll(layout, estiloGroupBox="border: 0px solid black", estiloScroll="border: 0px solid black"):
    group = QGroupBox()
    group.setStyleSheet(estiloGroupBox)
    group.setLayout(layout)
    scroll = QScrollArea()
    scroll.setStyleSheet(estiloScroll)
    scroll.setWidget(group)
    scroll.setWidgetResizable(True)
    return scroll
def generaImagen(direccion:str):
    l = QLabel()
    p = QPixmap(direccion)
    l.setPixmap(p)
    return l

class MiVentana(QMainWindow):

    def __init__(self):
        super().__init__()
        self.elementoFlotante = None
        self.tamPrin = None
        self.tamEle = None

    def fijaRedimensionar(self, elemento, porPantalla, porPrincipio):
        self.elementoFlotante = elemento
        self.tamPrin = porPrincipio
        self.tamEle = porPantalla

    def desactivarRedimensionar(self):
        self.elementoFlotante = None

    def resizeEvent(self, event):
        if self.elementoFlotante is not None:
            h = self.height()
            w = self.width()
            self.elementoFlotante.setFixedHeight(int(h*self.tamEle))
            self.elementoFlotante.setFixedWidth(int(w*self.tamEle))
            self.elementoFlotante.move(int(w*self.tamPrin), int(h*self.tamPrin))
            self.elementoFlotante.raise_()

class GUI(QApplication):

    def __init__(self, API:API, automatico:bool =True):
        self.API = API
        self.DIR_IMAGES = self.API.constantes.DIR_IMAGENES
        super().__init__([])
        self.window = MiVentana()
        self.window.show()
        self.window.setWindowTitle("Gimnasio")
        img = QPixmap(f"{self.DIR_IMAGES}\\icono.png")
        ico = QIcon(img)
        self.window.setWindowIcon(ico)
        self.setWindowIcon(ico)
        self.abriertoPopUp = False

        if automatico: self.abreInicio()

    def reiniciaVentana(self):
        try: self.widgetPrincipal.deleteLater()
        except: pass
        self.widgetPrincipal = QWidget()
        self.window.setCentralWidget(self.widgetPrincipal)

    def abreInicio(self):
        if self.abriertoPopUp: return None
        self.reiniciaVentana()
        layout = QHBoxLayout()
        self.widgetPrincipal.setLayout(layout)

        loImg = QVBoxLayout()
        img = QLabel()
        imgP = QPixmap(f"{self.DIR_IMAGES}\\menu.png")
        img.setPixmap(imgP)

        loImg.addItem(espaciadorVertical())
        loImg.addWidget(img)
        loImg.addItem(espaciadorVertical())

        loMenu = QVBoxLayout()
        fontMenu = QFont("Helvetica Now", 30)
        styleMenu = "color: black; background-color:rgb(151, 189, 189)"
        wMenu = 700
        hMenu = 80

        funLabMenu = lambda x: generaLabel(x, styleMenu, fontMenu, hMenu, wMenu)
        historial = funLabMenu("Historial")
        historial.mousePressEvent = lambda x : self.abreHistorial()
        ejercicios = funLabMenu("Ejercicios")
        ejercicios.mousePressEvent = lambda x : self.abreEjercicios()
        rutina = funLabMenu("Rutinas")
        rutina.mousePressEvent = lambda x : self.abreRutinas()
        entrenamiento = funLabMenu("Crear entrenamiento")
        entrenamiento.mousePressEvent = lambda x : self.abreNuevoEntrenamiento()

        loMenu.addItem(espaciadorVertical())
        loMenu.addWidget(historial)
        loMenu.addItem(QSpacerItem(0, 50))
        loMenu.addWidget(ejercicios)
        loMenu.addItem(QSpacerItem(0, 50))
        loMenu.addWidget(rutina)
        loMenu.addItem(QSpacerItem(0, 50))
        loMenu.addWidget(entrenamiento)
        loMenu.addItem(espaciadorVertical())

        layout.addItem(espaciadorHorizontal())
        layout.addLayout(loImg)
        layout.addItem(QSpacerItem(200, 0))
        layout.addLayout(loMenu)
        layout.addItem(espaciadorHorizontal())

    def creaTitulo(self, layout:QVBoxLayout):
        widget = QWidget()
        lo = QHBoxLayout()
        widget.setLayout(lo)
        widget.setFixedHeight(160)
        img = QLabel()
        imgP = QPixmap(f"{self.DIR_IMAGES}\\retroceder.png")
        img.setPixmap(imgP)
        img.mousePressEvent = lambda x : self.abreInicio()

        lo.addItem(QSpacerItem(15,0))
        lo.addWidget(img)
        lo.addItem(espaciadorHorizontal())

        layout.addWidget(widget)
        return lo

    def abreEjercicios(self, posMus:int =1, evento=None):
        self.reiniciaVentana()
        layout = QVBoxLayout()
        self.widgetPrincipal.setLayout(layout)
        layoutup = self.creaTitulo(layout)

        botAdd = generaLabel("Nuevo ejercicio", "background-color:rgb(131, 182, 215); border: 3px solid black;", 
                             estilo(20), 90, 280)
        botAdd.mousePressEvent = lambda x: self.abreCrearEjer(posMus)
        layoutup.addWidget(botAdd)
        layoutup.addItem(QSpacerItem(40,0))

        lo = QHBoxLayout()
        widget = QWidget()
        loSup = QVBoxLayout()
        widget.setStyleSheet("background-color:rgb(131, 182, 215); border: 3px solid black")
        widget.setLayout(loSup)
        lo.addItem(QSpacerItem(50,0))
        lo.addWidget(widget)
        lo.addItem(QSpacerItem(50,0))

        loMenu = QHBoxLayout()
        widgetMenu = QWidget()
        widgetMenu.setStyleSheet("border: 0px solid black; background-color: rgb(205, 241, 239)")
        layoutEjer = QVBoxLayout()
        #######
        groupBox = QGroupBox()
        groupBox.setStyleSheet("border: 0px solid black")
        groupBox.setLayout(layoutEjer)
        scroll = QScrollArea()
        scroll.setStyleSheet("border: 0px solid black")
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        lolo = QHBoxLayout()
        lolo.addWidget(scroll)
        widgetMenu.setLayout(lolo)

        loSup.addItem(QSpacerItem(0, 10))
        loSup.addLayout(loMenu)
        loSup.addWidget(widgetMenu)
        loSup.addItem(QSpacerItem(0, 10))
        loSup.setSpacing(0)
        font = QFont("Helvetica Now", 20)

        musculos = {}

        loMenu.addItem(QSpacerItem(30, 0))
        for indx, mus in self.API.musculos.items():
            musculos[indx] = generaLabel(mus, "border: 0px solid black", font, 80)
            musculos[indx].mousePressEvent = partial(self.abreEjercicios, indx)
            loMenu.addWidget(musculos[indx])
        loMenu.addItem(QSpacerItem(30, 0))
        musculos[posMus].setStyleSheet("background-color:rgb(205, 241, 239); border: 0px")

        dat = self.API.obtenEntrenamientosDeMusculo(posMus)
        cont = 0
        datos = [[]]
        for d in dat:
            if cont == 3: datos.append([])
            datos[-1].append(d)
            cont += 1
            if cont == 4: cont = 1

        style = "background-color:rgb(255, 255, 255)"
        font = QFont("Helvetica Now", 15)

        layoutEjer.addItem(QSpacerItem(0, 20))

        for x, lista in enumerate(datos):
                l = QHBoxLayout()
                l.addItem(espaciadorHorizontal())
                for y, (id, nom, idMusc, musc) in enumerate(lista):
                    lab = generaLabel(nom, style, font, 80, 500)
                    lab.mousePressEvent = partial(self.abrePestanhaEjercicio, id)
                    l.addWidget(lab)
                    if y != 3: l.addItem(QSpacerItem(30, 0))
                if len(lista) < 2: l.addItem(QSpacerItem(540, 0))
                if len(lista) < 3: l.addItem(QSpacerItem(535,0))
                l.addItem(espaciadorHorizontal())

                layoutEjer.addLayout(l)
                layoutEjer.addItem(QSpacerItem(0, 20))

        widgetMenu.setStyleSheet("background-color:rgb(205, 241, 239); border: 0px")

        layout.addLayout(lo)
        layout.addItem(QSpacerItem(0, 50))

    def ventanaEmergente(self):
        widget = QWidget(self.window)
        widget.setFixedWidth(int(self.window.width()*0.9))
        widget.setFixedHeight(int(self.window.height()*0.9))
        widget.setStyleSheet("background-color:rgb(40, 170, 170)")
        widget.move(int(self.window.width()*0.05), int(self.window.height()*0.05))
        widget.raise_()
        widget.show()
        self.window.fijaRedimensionar(widget, 0.9, 0.05)
        self.abriertoPopUp = True
        return widget

    def fijarBotonCerrar(self, widget:QWidget, layout:QVBoxLayout):
        def cerrar(widget:QWidget):
            widget.deleteLater()
            self.window.desactivarRedimensionar()
            self.abriertoPopUp = False

        layout.addItem(QSpacerItem(0, 30))
        l = QHBoxLayout()
        l.addItem(espaciadorHorizontal())
        f = QLabel()
        fp = QPixmap(f"{self.DIR_IMAGES}\\cerrar.png")
        f.setPixmap(fp)
        f.mousePressEvent = lambda x : cerrar(widget)
        l.addWidget(f)
        l.addItem(QSpacerItem(30, 0))
        layout.addLayout(l)
        return f

    def abrePestanhaEjercicio(self, idEjercicio, evento = None):
        def pulsadoEliminar(idEjer:int, widget:QWidget):
            d = self.API.eliminaEjercicio(idEjer)
            widget.deleteLater()
            self.abreEjercicios(d["idMusculo"])
            self.abriertoPopUp = False
        def pulsadoCancelar(layout:QHBoxLayout, idEjer:int, widget:QWidget):
            layout.itemAt(3).widget().deleteLater()
            pap = QLabel()
            papP = QPixmap(f"{self.DIR_IMAGES}\\papelera.png")
            pap.setPixmap(papP)
            pap.mousePressEvent = lambda x: pulsPapelera(layout, idEjer, widget)
            layout.insertWidget(3, pap)
        def pulsPapelera(layout:QHBoxLayout, idEjer:int, widget:QWidget):
            layout.itemAt(3).widget().deleteLater()
            wid = QWidget()
            lo = QHBoxLayout()
            wid.setLayout(lo)
            wid.setStyleSheet("background-color: white")
            layout.insertWidget(3, wid)
            wid.setFixedWidth(800)
            l = QLabel("¿Estas seguro de eliminar el ejercicio?")
            l.setFont(estilo(15))
            elim = generaLabel("Eliminar", "background-color: red", estilo(15), width=130)
            elim.mousePressEvent = lambda x : pulsadoEliminar(idEjer, widget)
            can = generaLabel("Cancelar", "background-color: rgb(131, 182, 215)", estilo(15), width=130)
            can.mousePressEvent = lambda x: pulsadoCancelar(layout, idEjercicio, widget)
            lo.addItem(QSpacerItem(10,0))
            lo.addWidget(l)
            lo.addItem(QSpacerItem(10, 0))
            lo.addWidget(elim)
            lo.addItem(QSpacerItem(10, 0))
            lo.addWidget(can)

        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)

        datos = self.API.obtenEjercicio(idEjercicio)[0]
        
        nomb = generaLabel(datos["nomEjercicio"], font=estilo(30))

        loInfo = QHBoxLayout()
        historial = QWidget()
        historial.setStyleSheet("background-color: white")
        historial.setFixedHeight(500)
        historial.setFixedWidth(400)
        loH = QVBoxLayout()
        historial.setLayout(loH)
        tHist = generaLabel("Ultimos registros", font=estilo(20))
        loH.addItem(QSpacerItem(0, 10))
        loH.addWidget(tHist)
        h = self.API.obtenUltEntrenosEjer(idEjercicio)
        loH.addItem(QSpacerItem(0, 20))
        for dic in h[:6]:
            loH.addItem(QSpacerItem(0, 12))
            l = generaLabel(dic["fecha"][:10], "background-color: rgb(131, 182, 215)",
                            estilo(15), 45)
            loH.addWidget(l)
        loH.addItem(espaciadorVertical())
        img = QLabel()
        imgp = QPixmap(f"{self.DIR_IMAGES}\\menu.png").scaled(400, 400)
        img.setPixmap(imgp)
        loInfo.addItem(espaciadorHorizontal())
        loInfo.addWidget(historial)
        loInfo.addItem(espaciadorHorizontal())
        loInfo.addWidget(img)
        loInfo.addItem(espaciadorHorizontal())

        loPap = QHBoxLayout()
        ajt = QLabel()
        ajtP = QPixmap(f"{self.DIR_IMAGES}\\ajustes.png")
        ajt.setPixmap(ajtP)
        pap = QLabel()
        papP = QPixmap(f"{self.DIR_IMAGES}\\papelera.png")
        pap.setPixmap(papP)
        pap.mousePressEvent = lambda x: pulsPapelera(loPap, idEjercicio, widget)
        loPap.addItem(QSpacerItem(10, 0))
        loPap.addWidget(ajt)
        loPap.addItem(espaciadorHorizontal())
        loPap.addWidget(pap)
        loPap.addItem(QSpacerItem(10, 0))
        
        layout.addWidget(nomb)
        layout.addItem(espaciadorVertical())
        layout.addLayout(loInfo)
        layout.addItem(espaciadorVertical())
        layout.addLayout(loPap)
        layout.addItem(QSpacerItem(0, 10))

    def abreCrearEjer(self, idMus:int =1):
        def escribeError(textoError:str, layout:QVBoxLayout):
            if layout.count() == 6:
                item = layout.itemAt(4).widget()
                item.setText(textoError)
            else: #5
                l = generaLabel(textoError, "color: red", estilo(20), 100)
                layout.insertWidget(4, l)
        def pulsadoAceptar(wmusculo:QComboBox, nombre:QLineEdit, layoutR:QVBoxLayout, widget:QWidget):
            idMusculo = wmusculo.currentIndex() + 1
            nombre = nombre.text()
            if not self.API.nombreEjerValido(nombre): 
                if nombre == "": escribeError("Escribe un nombre", layoutR)
                else: escribeError("Nombre ya existe", layoutR)
                return None
            self.API.anhadeEjercicio(idMusculo, nombre)
            widget.deleteLater()
            self.abriertoPopUp = False
            self.abreEjercicios(idMusculo)

        widget = self.ventanaEmergente()
        layoutGeneral = QVBoxLayout()
        widget.setLayout(layoutGeneral)
        self.fijarBotonCerrar(widget, layoutGeneral)

        layoutTitulo = QHBoxLayout()
        labelTitulo = generaLabel("Nuevo ejercicio", "background-color: white",
                                  estilo(25), 70, 450)
        layoutTitulo.addItem(espaciadorHorizontal())
        layoutTitulo.addWidget(labelTitulo)
        layoutTitulo.addItem(espaciadorHorizontal())

        layoutInfoYFoto = QHBoxLayout()
        layoutInfo = QVBoxLayout()
        layoutFoto = QVBoxLayout()
        layoutInfoYFoto.addLayout(layoutInfo)
        layoutInfoYFoto.addLayout(layoutFoto)

        layoutHMusculo = QHBoxLayout()
        labelMusculo = generaLabel("Musculo", "background-color: white",
                                   estilo(18), 45, 150)
        comboMusculo = QComboBox()
        comboMusculo.setFixedWidth(400)
        comboMusculo.setFixedHeight(45)
        comboMusculo.setStyleSheet("background-color: white")
        comboMusculo.addItems(self.API.musculos.values())
        comboMusculo.setFont(estilo(15))
        comboMusculo.setCurrentIndex(idMus-1)
        layoutHMusculo.addItem(espaciadorHorizontal())
        layoutHMusculo.addWidget(labelMusculo)
        layoutHMusculo.addItem(QSpacerItem(10, 0))
        layoutHMusculo.addWidget(comboMusculo)
        layoutHMusculo.addItem(espaciadorHorizontal())
        layoutNombreEjer = QHBoxLayout()
        labelNombre = generaLabel("Nombre", "background-color: white",
                                  estilo(18), 45, 150)
        entradaNombre = QLineEdit()
        entradaNombre.setFixedWidth(400)
        entradaNombre.setFixedHeight(45)
        entradaNombre.setStyleSheet("background-color: white")
        entradaNombre.setFont(estilo(15))
        layoutNombreEjer.addItem(espaciadorHorizontal())
        layoutNombreEjer.addWidget(labelNombre)
        layoutNombreEjer.addItem(QSpacerItem(10, 0))
        layoutNombreEjer.addWidget(entradaNombre)
        layoutNombreEjer.addItem(espaciadorHorizontal())

        layoutInfo.addItem(espaciadorVertical())
        layoutInfo.addLayout(layoutHMusculo)
        layoutInfo.addItem(QSpacerItem(0, 30))
        layoutInfo.addLayout(layoutNombreEjer)
        layoutInfo.addItem(espaciadorVertical())

        labelFoto = QLabel()
        fotop = QPixmap(f"{self.DIR_IMAGES}\\menu.png")
        labelFoto.setPixmap(fotop)
        layoutCentrarFoto = QHBoxLayout()
        layoutCentrarFoto.addItem(espaciadorHorizontal())
        layoutCentrarFoto.addWidget(labelFoto)
        layoutCentrarFoto.addItem(espaciadorHorizontal())
        botonCamImagen = QLabel()
        imagenp = QPixmap(f"{self.DIR_IMAGES}\\imagen.png")
        botonCamImagen.setPixmap(imagenp)
        botonCamImagen.setStyleSheet("background-color: white")
        layoutCentrarCamImagen = QHBoxLayout()
        layoutCentrarCamImagen.addItem(espaciadorHorizontal())
        layoutCentrarCamImagen.addWidget(botonCamImagen)
        layoutCentrarCamImagen.addItem(espaciadorHorizontal())
        layoutFoto.addLayout(layoutCentrarFoto)
        layoutFoto.addItem(QSpacerItem(0, 10))
        layoutFoto.addLayout(layoutCentrarCamImagen)

        layoutAceptar = QHBoxLayout()
        botonAceptar = generaLabel("Guardar", "background-color: rgb(205, 241, 239); border: 1px solid black",
                                   estilo(20), 80, 240)
        botonAceptar.mousePressEvent = lambda x: pulsadoAceptar(comboMusculo, entradaNombre, layoutInfo, widget)
        layoutAceptar.addItem(espaciadorHorizontal())
        layoutAceptar.addWidget(botonAceptar)
        layoutAceptar.addItem(espaciadorHorizontal())

        layoutGeneral.addLayout(layoutTitulo)
        layoutGeneral.addItem(espaciadorVertical())
        layoutGeneral.addLayout(layoutInfoYFoto)
        layoutGeneral.addItem(espaciadorVertical())
        layoutGeneral.addLayout(layoutAceptar)
        layoutGeneral.addItem(QSpacerItem(0, 75))

    def abreNuevoEntrenamiento(self, datos=None, evento=None):
        def cambiaDia(layout:QHBoxLayout, datos:dict, dia:int, evento=None):
            datos["fecha"] = Fecha(dia,  datos["fecha"].mes, datos["fecha"].anho)
            generaCalendario(layout, datos)
        def sigCal(layout:QHBoxLayout, datos:dict):
            t = datos["fecha"] + Fecha(0, 1, 0)
            datos["fecha"] = Fecha(1, t.mes, t.anho)
            generaCalendario(layout, datos)
        def antCal(layout:QHBoxLayout, datos:dict):
            t = datos["fecha"] - Fecha(0, 1, 0)
            datos["fecha"] = Fecha(1, t.mes, t.anho)
            generaCalendario(layout, datos)
        def generaCalendario(layout:QHBoxLayout, datos:dict):
            layout.itemAt(1).widget().deleteLater()
            widget = QWidget()
            widget.setFixedHeight(500)
            widget.setFixedWidth(500)
            widget.setStyleSheet("background-color: rgb(131, 182, 215); border-radius: 5px")
            layout.insertWidget(1, widget)

            layoutCal = QVBoxLayout()
            widget.setLayout(layoutCal)

            layoutMes = QHBoxLayout()
            botonMesAnt = generaLabel("<", AZUL_CLARO, estilo(16), 48, 48)
            botonMesAnt.mousePressEvent = lambda x : antCal(layout, datos)
            labelAnhoYMes = generaLabel(f"{datos['fecha'].anho} {datos['fecha'].mesSTR()}", 
                                        AZUL_CLARO, estilo(16), 48, 256)
            bontonMesSig = generaLabel(">", AZUL_CLARO, estilo(16), 48, 48)
            bontonMesSig.mousePressEvent = lambda x : sigCal(layout, datos)
            layoutMes.addWidget(botonMesAnt)
            layoutMes.addItem(espaciadorHorizontal())
            layoutMes.addWidget(labelAnhoYMes)
            layoutMes.addItem(espaciadorHorizontal())
            layoutMes.addWidget(bontonMesSig)

            widgetDias = QWidget()
            widgetDias.setStyleSheet("background-color: white")
            layoutDias = QVBoxLayout()
            widgetDias.setLayout(layoutDias)
            info = datos["fecha"].infoMes()
            dias = []
            WL = 60
            HL = WL
            for i in range(info["primDia"]):
                dias.append(QWidget())
                dias[i].setFixedHeight(HL)
                dias[i].setFixedWidth(WL)
            for dia in range(info["numDias"]):
                pos = dia + info["primDia"]
                dia += 1
                dias.append(generaLabel(str(dia), AZUL_CLARO, estilo(18), HL, WL))
                if dia == datos["fecha"].dia: dias[pos].setStyleSheet("background-color: rgb(131, 182, 215)")
                dias[pos].mousePressEvent = partial(cambiaDia, layout, datos, dia)

            cont = 0
            layoutTemp = None
            while cont < len(dias):
                if cont % 7 == 0:
                    if layoutTemp is not None: 
                        layoutTemp.addItem(espaciadorHorizontal())
                        layoutDias.addLayout(layoutTemp)
                        layoutTemp.addItem(espaciadorHorizontal())
                    layoutTemp = QHBoxLayout()
                layoutTemp.addWidget(dias[cont])
                cont += 1
            layoutTemp.addItem(espaciadorHorizontal())
            layoutDias.addLayout(layoutTemp)

            layoutCal.addLayout(layoutMes)
            layoutCal.addItem(espaciadorVertical())
            layoutCal.addWidget(widgetDias)
        def generaEjercicios(layout:QVBoxLayout, datos:dict):
            while not layout.isEmpty():
                it = layout.itemAt(0)
                if it.widget() is None: layout.removeItem(0)
                else: layout.removeWidget(it.widget())
            layout.addItem(QSpacerItem(0, 20))
            for idEjer in datos["ejer"].keys():
                lo = QHBoxLayout()
                dat = self.API.obtenEjercicio(idEjer)
                lab = generaLabel(dat[0]["nomEjercicio"], AZUL_CLARO,
                                  estilo(15), 70, 500)
                lab.mousePressEvent = partial(self.abreEjercicioEntrenamiento, datos, idEjer)
                lo.addItem(espaciadorHorizontal())
                lo.addWidget(lab)
                lo.addItem(espaciadorHorizontal())
                layout.addLayout(lo)
                layout.addItem(QSpacerItem(0, 20))
            layout.addItem(espaciadorVertical())
        def pulsadoAceptar():
            idEntr = self.API.anahadeEntrenamiento(datos["fecha"].formatoSQL())
            array = []
            for idEjer, ser in datos["ejer"].items():
                for peso, repes, tipo in ser:
                    array.append([idEjer, idEntr, peso, repes, tipo])
            self.API.anhadeSeries(array)
            self.abreInicio()

        self.reiniciaVentana()
        layout = QVBoxLayout()
        self.widgetPrincipal.setLayout(layout)
        self.creaTitulo(layout)

        if datos is None: 
            datos = {"fecha":Fecha.hoy(), "ejer":{}} # ejer -> [{idEjer: [(peso, repes, tipo)]}]
            datos["fecha"].quitaHora()

        layoutGeneral = QHBoxLayout()

        layoutEjerYAdd = QVBoxLayout()

        layoutScroll = QHBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: rgb(131, 182, 215)")
        scroll.setFixedHeight(650)
        scroll.setFixedWidth(600)
        groupBox = QGroupBox()
        scroll.setWidget(groupBox)
        layoutEjer = QVBoxLayout()
        layoutEjer.addWidget(QWidget())
        layoutEjer.addItem(QSpacerItem(1, 1))
        groupBox.setLayout(layoutEjer)
        generaEjercicios(layoutEjer, datos)
        layoutScroll.addItem(espaciadorHorizontal())
        layoutScroll.addWidget(scroll)
        layoutScroll.addItem(espaciadorHorizontal())

        layoutAnhadirYRutina = QHBoxLayout()
        labelAnhadir = generaLabel("Nuevo", "background-color: rgb(131, 182, 215)",
                                   estilo(25), 90, 280)
        labelAnhadir.mousePressEvent = lambda x : self.abreVentanaAnhadirEjercicio(datos)
        labelRutina = generaLabel("Fijar rutina", "background-color: rgb(131, 182, 215)",
                                  estilo(25), 90, 280)
        labelRutina.mousePressEvent = lambda x: self.abreInsertarRutina(datos)
        layoutAnhadirYRutina.addItem(espaciadorHorizontal())
        layoutAnhadirYRutina.addWidget(labelRutina)
        layoutAnhadirYRutina.addItem(QSpacerItem(40, 0))
        layoutAnhadirYRutina.addWidget(labelAnhadir)
        layoutAnhadirYRutina.addItem(espaciadorHorizontal())

        layoutEjerYAdd.addLayout(layoutScroll)
        layoutEjerYAdd.addItem(QSpacerItem(0, 20))
        layoutEjerYAdd.addLayout(layoutAnhadirYRutina)

        layoutCalYCon = QVBoxLayout()

        layoutCalendario = QVBoxLayout()
        widgetCalendario = QWidget()
        layoutCalendario.addItem(espaciadorVertical())
        layoutCalendario.addWidget(widgetCalendario)
        layoutCalendario.addItem(espaciadorVertical())
        generaCalendario(layoutCalendario, datos)

        layoutConfirmar = QHBoxLayout()
        labelConfirmar = generaLabel("Confirmar", "background-color: rgb(131, 182, 215)",
                                     estilo(25), 90, 300)
        w = QWidget()
        w.setFixedHeight(90)
        w.setFixedWidth(1)
        layoutConfirmar.addItem(espaciadorHorizontal())
        layoutConfirmar.addWidget(w)
        layoutConfirmar.addWidget(labelConfirmar)
        w = QWidget()
        w.setFixedHeight(90)
        w.setFixedWidth(1)
        layoutConfirmar.addWidget(w)
        layoutConfirmar.addItem(espaciadorHorizontal())
        if len(datos["ejer"]) == 0: labelConfirmar.hide()
        else:
            for v in datos["ejer"].values():
                if len(list(filter(lambda x: None in x, v))) != 0 or len(v) == 0:
                    labelConfirmar.hide()
                    break
        labelConfirmar.mousePressEvent = lambda x : pulsadoAceptar()

        layoutCalYCon.addItem(QSpacerItem(0, 50))
        layoutCalYCon.addLayout(layoutCalendario)
        layoutCalYCon.addItem(espaciadorVertical())
        layoutCalYCon.addLayout(layoutConfirmar)

        layoutGeneral.addItem(espaciadorHorizontal())
        layoutGeneral.addLayout(layoutEjerYAdd)
        layoutGeneral.addItem(espaciadorHorizontal())
        layoutGeneral.addLayout(layoutCalYCon)
        layoutGeneral.addItem(espaciadorHorizontal())

        #layout.addItem(espaciadorVertical())
        layout.addLayout(layoutGeneral)
        layout.addItem(espaciadorVertical())

    def abreVentanaAnhadirEjercicio(self, datos:dict, idEjer=1):
        def pulsadoAceptar(marcado, datos:dict,evento=None):
            if marcado:
                datos["ejer"][marcado[0]] = []
            widget.deleteLater()
            self.abriertoPopUp = False
            self.abreNuevoEntrenamiento(datos)
        def pulsadoEjer(idMusculo:int, layout:QVBoxLayout, marcado:list, nuevo:int, widgetAcep:QWidget,evento=None):
            if marcado:del marcado[0]
            marcado.append(nuevo)
            widgetAcep.show()
            muestraEjercicios(idMusculo, layout, marcado, widgetAcep)
        def muestraEjercicios(idMusculo:int, layout:QVBoxLayout, marcado:list, widgetAcep:QWidget):
            while layout.count() > 2:
                l = layout.itemAt(1).layout()
                while not l.isEmpty():
                    w = l.itemAt(0)
                    if w.widget() is None: l.removeItem(w)
                    else: l.removeWidget(w.widget())
                layout.removeItem(l)
                l.deleteLater()
            layout.removeItem(layout.itemAt(0))
            layout.removeItem(layout.itemAt(0))
            dat = self.API.obtenEntrenamientosDeMusculo(idMusculo)
            widgets = []
            WT = 350
            if marcado: selec = marcado[0]
            else: selec = -1
            for index, (idEjer, nom, p, o) in enumerate(dat):
                widgets.append(generaLabel(nom, "background-color:white",
                                           estilo(15), 80, WT))
                widgets[index].mousePressEvent = partial(pulsadoEjer, idMusculo, layout, marcado, idEjer, widgetAcep)
                if idEjer == selec: widgets[index].setStyleSheet(AZUL_OSCURO)
            cont = len(widgets)
            while (cont % 3) != 0:
                widgets.append(QWidget())
                widgets[cont].setFixedWidth(WT)
                cont += 1
            layout.addItem(QSpacerItem(0, 50))
            for i in range(0, len(widgets), 3):
                l = QHBoxLayout()
                l.addItem(espaciadorHorizontal())
                l.addWidget(widgets[i])
                l.addItem(QSpacerItem(40, 0))
                l.addWidget(widgets[i+1])
                l.addItem(QSpacerItem(40, 0))
                l.addWidget(widgets[i+2])
                l.addItem(espaciadorHorizontal())
                layout.addLayout(l)
            layout.addItem(QSpacerItem(0, 50))
            layout.setSpacing(20)
        def cambiaMusculo(idMusculo:int, musculos:list[QWidget], marcado:list, layoutEjer:QVBoxLayout, widgetAcep:QWidget,evento=None):
            for indx, w in enumerate(musculos):
                if indx == idMusculo-1: w.setStyleSheet(AZUL_CLARO)
                else: w.setStyleSheet(AZUL_OSCURO)
            muestraEjercicios(idMusculo, layoutEjer, marcado, widgetAcep)
        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)
        marcado = []

        layoutContEjer = QHBoxLayout()
        widgetEjercicios = QWidget()
        widgetEjercicios.setStyleSheet(AZUL_OSCURO)
        widgetEjercicios.setFixedHeight(int(900*0.65))
        widgetEjercicios.setFixedWidth(int(1728*0.90))
        layoutContEjer.addItem(espaciadorHorizontal())
        layoutContEjer.addWidget(widgetEjercicios)
        layoutContEjer.addItem(espaciadorHorizontal())

        layoutWidEjer = QVBoxLayout()
        layoutWidEjer.setSpacing(0)
        widgetEjercicios.setLayout(layoutWidEjer)
        layoutMusculos = QHBoxLayout()
        scroll = QScrollArea()
        scroll.setStyleSheet(f"border: 0px solid black;{AZUL_CLARO}")
        scroll.setWidgetResizable(True)
        groupBox = QGroupBox()
        scroll.setWidget(groupBox)
        layoutEjer = QVBoxLayout()
        groupBox.setLayout(layoutEjer)
        layoutWidEjer.addLayout(layoutMusculos)
        layoutWidEjer.addWidget(scroll)

        layoutConfirmar = QHBoxLayout()
        bontonConfirmar = generaLabel("Confirmar", AZUL_CLARO, estilo(20), 70, 300)
        bontonConfirmar.mousePressEvent = partial(pulsadoAceptar, marcado, datos)
        bontonConfirmar.hide()
        layoutConfirmar.addItem(espaciadorHorizontal())
        widgetBorrar = QWidget()
        widgetBorrar.setFixedHeight(70)
        widgetBorrar.setFixedWidth(1)
        layoutConfirmar.addWidget(widgetBorrar)
        layoutConfirmar.addWidget(bontonConfirmar)
        widgetBorrar = QWidget()
        widgetBorrar.setFixedHeight(70)
        widgetBorrar.setFixedWidth(1)
        layoutConfirmar.addWidget(widgetBorrar)
        layoutConfirmar.addItem(espaciadorHorizontal())

        layoutMusculos.addItem(espaciadorHorizontal())
        layoutMusculos.setSpacing(0)
        widgetsMusculos = []
        for id, nom in self.API.musculos.items():
            widgetsMusculos.append(generaLabel(nom, None, estilo(20), 60, 195))
            widgetsMusculos[id-1].mousePressEvent = partial(cambiaMusculo, id, widgetsMusculos, marcado, layoutEjer, bontonConfirmar)
            if id == idEjer: widgetsMusculos[id-1].setStyleSheet(f"border: 0px solid black; {AZUL_CLARO}")
            layoutMusculos.addWidget(widgetsMusculos[id-1])
        layoutMusculos.addItem(espaciadorHorizontal())

        muestraEjercicios(1, layoutEjer, marcado, bontonConfirmar)

        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutContEjer)
        layout.addItem(QSpacerItem(0, 50))
        layout.addLayout(layoutConfirmar)
        layout.addItem(QSpacerItem(0, 50))

    def abreInsertarRutina(self, datos:dict):
        def puladoEjer(layout:QVBoxLayout, IdPulsado:int, guardado:list, rutinas:list[QWidget], dicRut:dict, widgetAcept:QWidget,evento=None):
            if guardado: del guardado[0]
            guardado.append(IdPulsado)
            pos = 0
            while layout.count() > 1: layout.removeWidget(layout.itemAt(1).widget())
            if not layout.isEmpty(): layout.removeItem(layout.itemAt(0))
            for pos, l in enumerate(rutinas):
                if dicRut[pos] == IdPulsado: l.setStyleSheet(f"{AZUL_CLARO}; border: 2px solid black")
                else: l.setStyleSheet(AZUL_CLARO)
            dat = self.API.obtenRutina(IdPulsado)
            for d in dat["ejercicios"]:
                l = generaLabel(f"{d['nomEjer']} X{d['numSer']}", AZUL_CLARO,
                                estilo(15), 60)
                layout.addWidget(l)
            layout.addItem(espaciadorVertical())
            widgetAcept.show()
        def pulsadoAcept(widget:QWidget, guardado:list, datos:dict):
            widget.deleteLater()
            self.abriertoPopUp = False
            idRut = guardado[0]
            dat = self.API.obtenRutina(idRut)
            datos["ejer"] = {}
            for d in dat["ejercicios"]:
                datos["ejer"][d["idEjer"]] = [[None, None, None] for i in range(d["numSer"])]
            self.abreNuevoEntrenamiento(datos)
        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)
        guardado = []

        layoutDatos = QHBoxLayout()
        scrollRutinas = QScrollArea()
        scrollRutinas.setFixedHeight(550)
        scrollRutinas.setFixedWidth(500)
        scrollRutinas.setStyleSheet(AZUL_OSCURO)
        scrollRutinas.setWidgetResizable(True)
        groupRutinas = QGroupBox()
        layoutRutinas = QVBoxLayout()
        scrollRutinas.setWidget(groupRutinas)
        groupRutinas.setLayout(layoutRutinas)
        scrollEjer = QScrollArea()
        scrollEjer.setFixedHeight(550)
        scrollEjer.setFixedWidth(500)
        scrollEjer.setStyleSheet(AZUL_OSCURO)
        scrollEjer.setWidgetResizable(True)
        groupEjer = QGroupBox()
        layoutEjer = QVBoxLayout()
        scrollEjer.setWidget(groupEjer)
        groupEjer.setLayout(layoutEjer)
        layoutDatos.addItem(espaciadorHorizontal())
        layoutDatos.addWidget(scrollRutinas)
        layoutDatos.addItem(espaciadorHorizontal())
        layoutDatos.addWidget(scrollEjer)
        layoutDatos.addItem(espaciadorHorizontal())

        layoutConfirmar = QHBoxLayout()
        botonConfirmar = generaLabel("Confirmar", AZUL_CLARO, estilo(20), 90, 250)
        botonConfirmar.hide()
        botonConfirmar.mousePressEvent = lambda x : pulsadoAcept(widget, guardado, datos)
        layoutConfirmar.addItem(espaciadorHorizontal())
        w = QWidget()
        w.setFixedHeight(90)
        w.setFixedWidth(1)
        layoutConfirmar.addWidget(w)
        layoutConfirmar.addWidget(botonConfirmar)
        w = QWidget()
        w.setFixedHeight(90)
        w.setFixedWidth(1)
        layoutConfirmar.addWidget(w)
        layoutConfirmar.addItem(espaciadorHorizontal())

        layoutRutinas.setSpacing(20)
        layoutEjer.setSpacing(20)
        dat = self.API.obtenRutina()
        rutinas = []
        dicRutinas = {}
        for index, dic in enumerate(dat):
            dicRutinas[index] = dic["id"]
            rutinas.append(generaLabel(dic["nombre"], AZUL_CLARO, estilo(15), 60))
            rutinas[index].mousePressEvent = partial(puladoEjer, layoutEjer, dic["id"], guardado, rutinas, dicRutinas, botonConfirmar)
            layoutRutinas.addWidget(rutinas[index])
        layoutRutinas.addItem(espaciadorVertical())

        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutDatos)
        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutConfirmar)
        layout.addItem(QSpacerItem(0, 50))

    def abreEjercicioEntrenamiento(self, datos, idEjercicio, evento=None, peso=[], repes=[], tipoS:list[QLabel]=[]):
        def guardaDatos(layout, evento=None, widget:QWidget=None):
            if len(peso) != len(repes): raise IndexError("No son de la misma logitud los elementos")
            for pos in range(len(peso)):
                if peso[pos].text() != "": datos["ejer"][idEjercicio][pos][0] = peso[pos].text()
                else : datos["ejer"][idEjercicio][pos][0] = None
                if repes[pos].text() != "": datos["ejer"][idEjercicio][pos][1] = repes[pos].text()
                else: datos["ejer"][idEjercicio][pos][1] = None
                if tipoS[pos].text() == " N ": datos["ejer"][idEjercicio][pos][2] = "n"
                elif tipoS[pos].text() == " D ": datos["ejer"][idEjercicio][pos][2] = "d"
            if widget is None: muestraSeries(layout)
            else:
                widget.deleteLater()
                self.abriertoPopUp = False
                self.abreNuevoEntrenamiento(datos)
        def eliminaSerie(pos:int, peso:list[QLineEdit], repes:list[QLineEdit], layout, evento=None):
            del datos["ejer"][idEjercicio][pos]
            del peso[pos]
            del repes[pos]
            guardaDatos(layout)
        def eliminarYCerrar(widget:QWidget):
            del datos["ejer"][idEjercicio]
            widget.deleteLater()
            self.abriertoPopUp = False
            self.abreNuevoEntrenamiento(datos)
        def pulsadoTipoSerie(pos:int, layout, evento=None):
            if tipoS[pos].text() == " N ": tipoS[pos].setText(" D ")
            elif tipoS[pos].text() == " D ": tipoS[pos].setText(" N ")
            guardaDatos(layout)
        def pulsadoAnhadirSerie(layout:QVBoxLayout):            
            datos["ejer"][idEjercicio].append([None, None, None])
            guardaDatos(layout)
        def muestraSeries(layout:QVBoxLayout, evento=None):
            while not layout.isEmpty():
                layout.removeWidget(layout.itemAt(0).widget())
            while peso: del peso[0]
            while repes: del repes[0]
            while tipoS: del tipoS[0]
            for indx, (pesoAnt, repesAnt, tipo) in enumerate(datos["ejer"][idEjercicio]):
                w = QWidget()
                w.setStyleSheet(AZUL_CLARO)
                w.setFixedHeight(80)
                lay = QHBoxLayout()
                w.setLayout(lay)
                pos = generaLabel(f"Serie {indx+1}:", font=estilo(15))
                peso.append(QLineEdit())
                peso[indx].setFixedWidth(60)
                peso[indx].setStyleSheet("background-color: white")
                peso[indx].setFont(estilo(15))
                peso[indx].setValidator(QIntValidator())
                if pesoAnt is not None: peso[indx].setText(pesoAnt)
                lpeso = generaLabel("Kg X ", font=estilo(15))
                repes.append(QLineEdit())
                repes[indx].setFixedWidth(60)
                repes[indx].setStyleSheet("background-color: white")
                repes[indx].setFont(estilo(15))
                repes[indx].setValidator(QIntValidator())
                if repesAnt is not None: repes[indx].setText(repesAnt)
                lrepes = generaLabel(" repeticiones ", font=estilo(15))
                if tipo is None:
                    datos["ejer"][idEjercicio][indx][2] = "n"
                    tipo = "n"
                if tipo == "n": t = " N "
                elif tipo == "d": t = " D "
                tipoS.append(generaLabel(t, font=estilo(18), width=60))
                if tipo == "n": tipoS[indx].setStyleSheet("border: 2px solid black; border-radius: 10px")
                elif tipo == "d": tipoS[indx].setStyleSheet(f"border: 2px solid black; border-radius: 10px; {AZUL_OSCURO}")
                tipoS[indx].mousePressEvent = partial(pulsadoTipoSerie, indx, layout)
                borrar = generaLabel("X", "background-color:red",
                                     estilo(18), 50, 60)
                borrar.mousePressEvent = partial(eliminaSerie, indx, peso, repes, layout)
                lay.addWidget(pos)
                lay.addWidget(peso[indx])
                lay.addWidget(lpeso)
                lay.addWidget(repes[indx])
                lay.addWidget(lrepes)
                lay.addWidget(tipoS[indx])
                lay.addItem(espaciadorHorizontal())
                lay.addWidget(borrar)
                layout.insertWidget(layout.count()-1, w)
            botonNuevo = generaLabel("+", None, estilo(40), 80)
            botonNuevo.mousePressEvent = lambda x : pulsadoAnhadirSerie(layout)
            layout.insertWidget(layout.count()-1, botonNuevo)                
        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        botonCerrar = self.fijarBotonCerrar(widget, layout)

        info = self.API.obtenEjercicio(idEjercicio)[0]

        tituloVent = generaLabel(info["nomEjercicio"], None, estilo(25))

        layoutWidget = QHBoxLayout()
        widgetSeries = QWidget()
        layoutWidget.addItem(espaciadorHorizontal())
        layoutWidget.addWidget(widgetSeries)
        layoutWidget.addItem(espaciadorHorizontal())
        widgetSeries.setStyleSheet(AZUL_OSCURO)
        widgetSeries.setFixedHeight(600)
        widgetSeries.setFixedWidth(670)
        scroll = QScrollArea()
        group = QGroupBox()
        scroll.setWidgetResizable(True)
        scroll.setWidget(group)
        layoutSeries = QVBoxLayout()
        layoutSeries.setSpacing(10)
        layoutExt = QVBoxLayout()
        layoutExt.addItem(QSpacerItem(0, 20))
        layoutExt.addWidget(scroll)
        layoutExt.addItem(QSpacerItem(0, 20))
        group.setLayout(layoutSeries)
        widgetSeries.setLayout(layoutExt)
        layoutSeries.addItem(espaciadorVertical())
        muestraSeries(layoutSeries)
        botonCerrar.mousePressEvent = lambda x: guardaDatos(layout, widget=widget)
        
        layoutBorrar = QHBoxLayout()
        img = QLabel()
        imgP = QPixmap(f"{self.DIR_IMAGES}\\papelera.png")
        img.setPixmap(imgP)
        img.mousePressEvent = lambda x : eliminarYCerrar(widget)
        layoutBorrar.addItem(espaciadorHorizontal())
        layoutBorrar.addWidget(img)
        layoutBorrar.addItem(QSpacerItem(20, 0))

        layout.addWidget(tituloVent)
        layout.addItem(QSpacerItem(0, 30))
        layout.addLayout(layoutWidget)
        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutBorrar)
        layout.addItem(QSpacerItem(0, 20))

    def abreRutinas(self, evento=None):
        self.reiniciaVentana()
        layout = QVBoxLayout()
        self.widgetPrincipal.setLayout(layout)
        self.creaTitulo(layout)

        layoutWidRutinas = QHBoxLayout()
        widgetRutinas = QWidget()
        widgetRutinas.setStyleSheet(AZUL_OSCURO)
        widgetRutinas.setFixedHeight(600)
        widgetRutinas.setFixedWidth(500)
        layoutWidRutinas.addItem(espaciadorHorizontal())
        layoutWidRutinas.addWidget(widgetRutinas)
        layoutWidRutinas.addItem(espaciadorHorizontal())
        layoutContRutinas = QVBoxLayout()
        scroll = QScrollArea()
        group = QGroupBox()
        layoutRutinas = QVBoxLayout()
        scroll.setWidget(group)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 0px")
        group.setLayout(layoutRutinas)
        widgetRutinas.setLayout(layoutContRutinas)
        layoutContRutinas.addItem(QSpacerItem(0, 20))
        layoutContRutinas.addWidget(scroll)
        layoutContRutinas.addItem(QSpacerItem(0, 20))

        datos = self.API.obtenRutina()
        layoutRutinas.setSpacing(10)
        for dic in datos:
            lab = generaLabel(dic["nombre"], AZUL_CLARO, estilo(15), 60)
            lab.mousePressEvent = partial(self.abreInfoRutina, dic["id"])
            layoutRutinas.addWidget(lab)

        layoutNueva = QHBoxLayout()
        botonNueva = generaLabel("Nueva rutina", AZUL_OSCURO, estilo(20), 80, 500)
        botonNueva.mousePressEvent = lambda x : self.abreNuevaRutina()
        layoutNueva.addItem(espaciadorHorizontal())
        layoutNueva.addWidget(botonNueva)
        layoutNueva.addItem(espaciadorHorizontal())

        layout.addLayout(layoutWidRutinas)
        layout.addItem(QSpacerItem(0, 30))
        layout.addLayout(layoutNueva)
        layout.addItem(espaciadorVertical())

    def abreInfoRutina(self, idRutina:int=None, evento=None):
        def pulsadoCancelar(layout:QHBoxLayout, widget):
            layout.removeWidget(layout.itemAt(1).widget())
            b = generaImagen(f"{self.DIR_IMAGES}\\papelera.png")
            b.mousePressEvent = lambda x : pulsadoPapelera(layout=layout, widget=widget)
            layout.insertWidget(1, b)
        def pulsadoBorrar(widget:QWidget):
            widget.deleteLater()
            self.abriertoPopUp = False
            self.API.eliminaRutina(idRutina)
            self.abreRutinas()
        def pulsadoNuevoEjer(widget:QWidget):
            widget.deleteLater()
            self.abreAnhadirEjercicioRutina(idRutina=idRutina)
        def reabreVentana(widget:QWidget, enveto=None):
            widget.deleteLater()
            self.abreInfoRutina(idRutina)
        def eliminaEjer(evento=None, widget:QWidget=None, idEjer:int=None):
            self.API.eliminaEjercicioRutina(idRutina, idEjer)
            reabreVentana(widget)
        def cambiadoNumSeries(evento=None, idEjer=None, lineEdit:QLineEdit=None):
            if lineEdit.text() == "": nuevo = None
            else: nuevo = int(lineEdit.text())
            self.API.fijaSeriresEjercicioRutina(nuevo, idRutina, idEjer)
        def pulsadoPapelera(evento=None, layout:QHBoxLayout=None, widget=None): 
            layout.removeWidget(layout.itemAt(1).widget())
            cont = generaWidget(90, 850, AZUL_CLARO)
            layout.insertWidget(1, cont)
            lay = QHBoxLayout()
            cont.setLayout(lay)
            lay.addItem(QSpacerItem(20, 0))
            lay.addWidget(generaLabel("¿Estas seguro de eliminar la rutina?", None, estilo(15)))
            lay.addItem(espaciadorHorizontal())
            botAceptar = generaLabel("Eliminar", "background-color:red", estilo(15), 60, 180)
            botAceptar.mousePressEvent = lambda x : pulsadoBorrar(widget)
            lay.addWidget(botAceptar)
            botCancelar = generaLabel("Cancelar", AZUL_OSCURO, estilo(15), 60, 180)
            botCancelar.mousePressEvent = lambda x : pulsadoCancelar(layout, widget)
            lay.addWidget(botCancelar)
        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)
        datos = self.API.obtenRutina(idRutina)

        titulo = generaLabel(datos["nombre"], None, estilo(25))

        layoutContEjer = QHBoxLayout()
        widgetEjer = generaWidget(500, 1000, AZUL_OSCURO)
        layoutContEjer.addItem(espaciadorHorizontal())
        layoutContEjer.addWidget(widgetEjer)
        layoutContEjer.addItem(espaciadorHorizontal())

        layoutWidEjer = QVBoxLayout()
        widgetEjer.setLayout(layoutWidEjer)
        layoutEjer = QVBoxLayout()
        scroll = generaScroll(layoutEjer)
        layoutWidEjer.addItem(QSpacerItem(0, 20))
        layoutWidEjer.addWidget(scroll)
        layoutWidEjer.addItem(QSpacerItem(0, 20))

        layoutEjer.setSpacing(15)
        lineEdits = []
        for index, dic in enumerate(datos["ejercicios"]):
            wid = generaWidget(90, None, AZUL_CLARO)
            layoutEjer.addWidget(wid)
            l = QHBoxLayout()
            wid.setLayout(l)
            l.addWidget(generaLabel(f"{dic['nomEjer']} X ", None, estilo(15)))
            lineEdits.append(QLineEdit())
            lineEdits[index].setFixedWidth(40)
            lineEdits[index].setFixedHeight(40)
            lineEdits[index].setAlignment(Qt.AlignCenter)
            lineEdits[index].setStyleSheet("background-color: white")
            lineEdits[index].setFont(estilo(15))
            lineEdits[index].setValidator(QIntValidator(0, 99))
            lineEdits[index].textChanged.connect(partial(cambiadoNumSeries, idEjer=dic["idEjer"], lineEdit=lineEdits[index]))
            if dic["numSer"] is not None: lineEdits[index].setText(str(dic["numSer"]))
            l.addWidget(lineEdits[index])
            l.addItem(espaciadorHorizontal())
            b = generaLabel("DEL", "background-color:red", estilo(17), 50, 80)
            b.mousePressEvent = partial(eliminaEjer, widget=widget, idEjer=dic["idEjer"])
            l.addWidget(b)
        botonNuevo = generaLabel("+", None, estilo(30), 70)
        botonNuevo.mousePressEvent = lambda x : pulsadoNuevoEjer(widget)
        layoutEjer.addWidget(botonNuevo)
        layoutEjer.addItem(espaciadorVertical())

        layoutBorrar = QHBoxLayout()
        layoutBorrar.addItem(espaciadorHorizontal())
        botonBorrar = generaImagen(f"{self.DIR_IMAGES}\\papelera.png")
        botonBorrar.mousePressEvent = lambda x : pulsadoPapelera(layout=layoutBorrar, widget=widget)
        layoutBorrar.addWidget(botonBorrar)
        layoutBorrar.addItem(QSpacerItem(30, 0))

        layout.addWidget(titulo)
        layout.addItem(QSpacerItem(0, 30))
        layout.addLayout(layoutContEjer)
        layout.addItem(QSpacerItem(0, 30))
        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutBorrar)
        layout.addItem(QSpacerItem(0, 30))

    def abreNuevaRutina(self):
        def comprobarTexto(lineEdit:QLineEdit, botonAceptar:QLabel):
            if lineEdit.text() != "":
                if botonAceptar.isHidden():
                    botonAceptar.show()
            else: botonAceptar.hide()
        def pulsadoAceptar(lineEdit:QLineEdit, widget:QWidget):
            idNuevo = self.API.anahdeRutina(lineEdit.text(), [])
            widget.deleteLater()
            self.abreRutinas()
            self.abreInfoRutina(idNuevo)
        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)

        layNombre = QHBoxLayout()
        labNombre = generaLabel("Nombre:", None, estilo(30))
        entradaNombre = QLineEdit()
        entradaNombre.setStyleSheet("background-color: white")
        entradaNombre.setFont(estilo(30))
        entradaNombre.setFixedWidth(700)
        layNombre.addItem(espaciadorHorizontal())
        layNombre.addWidget(labNombre)
        layNombre.addItem(QSpacerItem(50, 0))
        layNombre.addWidget(entradaNombre)
        layNombre.addItem(espaciadorHorizontal())

        layAceptar = QHBoxLayout()
        botonAceptar = generaLabel("Aceptar", AZUL_CLARO, estilo(25), 100, 250)
        botonAceptar.hide()
        botonAceptar.mousePressEvent = lambda x : pulsadoAceptar(entradaNombre, widget)
        entradaNombre.textChanged.connect(lambda x: comprobarTexto(entradaNombre, botonAceptar))
        layAceptar.addItem(espaciadorHorizontal())
        layAceptar.addWidget(botonAceptar)
        layAceptar.addItem(QSpacerItem(0, 100))
        layAceptar.addItem(espaciadorHorizontal())

        layout.addItem(espaciadorVertical())
        layout.addLayout(layNombre)
        layout.addItem(espaciadorVertical())
        layout.addLayout(layAceptar)
        layout.addItem(espaciadorVertical())

    def abreAnhadirEjercicioRutina(self, evento=None, idRutina:int=None):
        def pulsadoEjercicio(punteroSeleccion:list, seleccionado, labels:list[QLabel], pos, botonAceptar:QLabel, evento=None):
            if botonAceptar.isHidden(): botonAceptar.show()
            while punteroSeleccion: del punteroSeleccion[0]
            punteroSeleccion.append(seleccionado)
            for i in range(len(labels)):
                if type(labels[i]) == QLabel:
                    if i != pos: labels[i].setStyleSheet("background-color: white")
                    else: labels[i].setStyleSheet(AZUL_OSCURO)
        def muestraEjercicios(punteroSeleccion:list, botonAceptar:QLabel, evento=None, idMusculo=None, widget=None, layout:QHBoxLayout=None):
            #Elimina y crea el widget
            if widget is not None: widget.deleteLater()
            widgetContenedorEjer = generaWidget(height=650, width=1600, estilo=AZUL_OSCURO)
            layout.insertWidget(1, widgetContenedorEjer)

            #Crea los layouts
            layoutHWidget = QHBoxLayout()
            layoutElemWidget = QVBoxLayout()
            layoutHWidget.addItem(QSpacerItem(30, 0))
            layoutHWidget.addLayout(layoutElemWidget)
            layoutHWidget.addItem(QSpacerItem(30, 0))
            layoutMusculos = QHBoxLayout()
            widgetEjercicios = generaWidget(estilo=AZUL_CLARO)
            widgetContenedorEjer.setLayout(layoutHWidget)
            layoutElemWidget.setSpacing(0)
            layoutElemWidget.addItem(QSpacerItem(0, 30))
            layoutElemWidget.addLayout(layoutMusculos)
            layoutElemWidget.addWidget(widgetEjercicios)
            layoutElemWidget.addItem(QSpacerItem(0, 30))
            layoutContScroll = QVBoxLayout()
            layoutEjercicios = QVBoxLayout()
            scroll = generaScroll(layoutEjercicios)
            widgetEjercicios.setLayout(layoutContScroll)
            layoutContScroll.addItem(QSpacerItem(0, 20))
            layoutContScroll.addWidget(scroll)
            layoutContScroll.addItem(QSpacerItem(0, 20))

            #Colocar el nombre del musculo
            layoutMusculos.setSpacing(0)
            layoutMusculos.addItem(espaciadorHorizontal())
            for id, nom in self.API.musculos.items():
                if id == idMusculo: est = AZUL_CLARO
                else: est = None
                lab = generaLabel(nom, est, estilo(20), 60, 200)
                lab.mousePressEvent = partial(muestraEjercicios, punteroSeleccion, botonAceptar, idMusculo=id, 
                                              widget=widgetContenedorEjer, layout=layuotWidget)
                layoutMusculos.addWidget(lab)
            layoutMusculos.addItem(espaciadorHorizontal())

            #Hace los label de los ejercicios
            datos = self.API.obtenEntrenamientosDeMusculo(idMusculo)
            labels = []
            for index, (id, nom, idMus, nomMus) in enumerate(datos):
                if punteroSeleccion and id == punteroSeleccion[0]: est = AZUL_OSCURO
                else: est = "background-color: white"
                labels.append(generaLabel(nom, est, estilo(15), 80, 420))
                labels[index].mousePressEvent = partial(pulsadoEjercicio, punteroSeleccion, id, labels, index, botonAceptar)
            while len(labels) % 3 != 0: labels.append(generaWidget(80, 420))
            
            #Muestra los ejercicios
            layoutEjercicios.setSpacing(30)
            for i in range(0, len(labels), 3):
                l = QHBoxLayout()
                l.addItem(espaciadorHorizontal())
                l.addWidget(labels[i])
                l.addItem(espaciadorHorizontal())
                l.addWidget(labels[i+1])
                l.addItem(espaciadorHorizontal())
                l.addWidget(labels[i+2])
                l.addItem(espaciadorHorizontal())
                layoutEjercicios.addLayout(l)
        def pulsadoAceptar(punteroSeleccion:list, widget:QWidget):
            self.API.anhadeEjercicioRutina(idRutina, punteroSeleccion[0])
            widget.deleteLater()
            self.abreInfoRutina(idRutina)

        widget = self.ventanaEmergente()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.fijarBotonCerrar(widget, layout)

        layuotWidget = QHBoxLayout()
        widgetContenedorEjer = generaWidget(height=650, width=1600, estilo=AZUL_OSCURO)
        layuotWidget.addItem(espaciadorHorizontal())
        layuotWidget.addWidget(widgetContenedorEjer)
        layuotWidget.addItem(espaciadorHorizontal())

        punteroSeleccion = []

        layoutConfirmar = QHBoxLayout()
        botonConfirmar = generaLabel("Confirmar", AZUL_OSCURO, estilo(20), 80, 180)
        botonConfirmar.hide()
        botonConfirmar.mousePressEvent = lambda x : pulsadoAceptar(punteroSeleccion, widget)
        layoutConfirmar.addItem(espaciadorHorizontal())
        layoutConfirmar.addWidget(botonConfirmar)
        layoutConfirmar.addItem(espaciadorHorizontal())

        muestraEjercicios(punteroSeleccion, botonConfirmar,idMusculo=1, widget=widgetContenedorEjer, layout=layuotWidget)

        layout.addItem(QSpacerItem(0, 10))
        layout.addLayout(layuotWidget)
        layout.addItem(espaciadorVertical())
        layout.addLayout(layoutConfirmar)
        layout.addItem(espaciadorVertical())

    def preguntaPrimeraVez():
        app = QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("¿Es la primera vez que ejecutas este programa?")
        msg_box.setWindowTitle("Pregunta")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        respuesta = msg_box.exec_()
        while app.hasPendingEvents():
            app.processEvents()
        return respuesta == QMessageBox.Yes
    
    def muestraError(error:str):
        app = QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()
        while app.hasPendingEvents():
            app.processEvents()

    def abreHistorial(self):
        self.reiniciaVentana()
        layout = QVBoxLayout()
        self.widgetPrincipal.setLayout(layout)
        self.creaTitulo(layout)
        layout.addItem(espaciadorVertical())
        layout.addWidget(generaLabel("POR IMPLEMENTAR", AZUL_OSCURO, estilo(40), 300))
        layout.addItem(espaciadorVertical())

if __name__ == "__main__":
    dirMain = __file__[:-7]
    api = API(dirMain, test=True)
    gui = GUI(api, False)
    gui.abreRutinas()
    gui.exec_()