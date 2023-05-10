from datetime import datetime, timedelta

MESES = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}

class Fecha():


    def __init__(self, dia, mes, anho, hora=0, minutos=0, segundos=0):
        self.dia = dia
        self.mes = mes
        self.anho = anho
        self.hora = hora
        self.minutos = minutos
        self.segundos = segundos

    def sql(texto:str):
        if type(texto) != str: raise TypeError("The type of the input is not a str")
        d = texto.split()
        f = d[0].split("-")
        if len(f) != 3: raise ValueError("The date format is not correct")
        anho = f.pop(0)
        if not anho.isdigit() or int(anho) < 1000: raise ValueError("The year is not correct")
        anho = int(anho)
        mes = f.pop(0)
        if not mes.isdigit() or int(mes) < 1 or int(mes) > 12: raise ValueError("The month is not correct")
        mes = int(mes)
        dia = f.pop(0)
        if not dia.isdigit() or int(dia) < 0 or int(dia) > 31: raise ValueError("The day is not correct")
        dia = int(dia)

        hora = 0
        min = 0
        seg = 0
        if len(d) == 2:
            f = d[1].split(":")
            if len(f) not in (2, 3): raise ValueError("The format of the hour is not correct")
            hora = f.pop(0)
            if not hora.isdigit() or int(hora) < 0 or int(hora) > 23: raise ValueError("The hour is not correct")
            hora = int(hora)
            min = f.pop(0)
            if not min.isdigit() or int(min) < 0 or int(min) > 59: raise ValueError("The minuts are not correct")
            min = int(min)
            if f:
                seg = f.pop(0)
                if not seg.isdigit() or int(seg) < 0 or int(seg) > 59: raise ValueError("The seconds are not correct")
                seg = int(seg)

        return Fecha(dia, mes, anho, hora, min, seg)
    
    def mesSTR(self):
        return MESES[self.mes]
    
    def hoy():
        dat = datetime.now()
        return Fecha(dat.day, dat.month, dat.year, dat.hour, dat.minute, dat.second)
    
    def formatoSQL(self):
        mes, dia, hora, min, seg = ("","","","","")
        if self.mes < 10: mes = "0"
        if self.dia < 10: dia = "0"
        if self.hora < 10: hora = "0"
        if self.minutos < 10: min = "0"
        if self.segundos < 10: seg = "0"
        return f"{self.anho}-{mes+str(self.mes)}-{dia+str(self.dia)} {hora+str(self.hora)}:{min+str(self.minutos)}:{seg+str(self.segundos)}"
    
    def quitaHora(self):
        self.hora = 0
        self.minutos = 0
        self.segundos = 0
    
    def infoMes(self):
        d = datetime(self.anho, self.mes, 1)
        if self.mes == 12: d2 = datetime(self.anho+1, 1, 1)
        else: d2 = datetime(self.anho, self.mes+1, 1)
        d2 = d2 - timedelta(days=1)
        return {"primDia":d.weekday(), "numDias":d2.day}

    def __str__(self):
        return f"Clase fecha: {self.anho}-{self.mes}-{self.dia} {self.hora}:{self.minutos}:{self.segundos}"
    
    def __add__(self, fecha):
        y, m, d, h, min, s = 0, 0, 0, 0, 0, 0
        s += self.segundos + fecha.segundos
        while s > 59:
            s -= 60
            min += 1
        min += self.minutos + fecha.minutos
        while min > 59:
            min -= 60
            h += 1
        h += self.hora + fecha.hora
        while h > 23:
            h -= 24
            d += 1
        d += self.dia + fecha.dia
        while d > 31:
            ########
            d -= 31
            m += 1
            #TODO
        m += self.mes + fecha.mes
        while m > 12:
            m -= 12
            y += 1
        y += self.anho + fecha.anho
        return Fecha(d, m, y, h, min, s)
    
    def __sub__(self, fecha):
        y, m, d, h, min, s = 0, 0, 0, 0, 0, 0
        s += self.segundos - fecha.segundos
        while s < 0:
            s += 60
            min -= 1
        min += self.minutos - fecha.minutos
        while min < 0:
            min += 60
            h -= 1
        h += self.hora - fecha.hora
        while h < 0:
            h += 24
            d -= 1
        d += self.dia - fecha.dia
        while d < 1:
            ########
            d += 31
            m -= 1
            #TODO
        m += self.mes - fecha.mes
        while m < 1:
            m += 12
            y -= 1
        y += self.anho - fecha.anho
        return Fecha(d, m, y, h, min, s)
    
if __name__ == "__main__":
    a = Fecha.sql("2023-1-03 12:30:12")
    print(Fecha.hoy() - Fecha(19, 0, 0))