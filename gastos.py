# coding=utf-8
# Archivo principal
"""
El objetivo de este programa es hacer un cálculo de mis gastos mensuales,
con detalle de entradas, salidas, etc. Mes a mes.
Cada vez que inicia un mes tengo el saldo de los anteriores  y empiezo con ese monto.
"""

# Automatización de la fecha
from datetime import date

fecha = str(date.today())
mes = int(fecha[5:7])
dia = fecha[8:]
fecha = f"{dia}/{mes}"

# Variables que voy a necesitar
saldo_mes = 0
meses = {1: "enero",
         2: "febrero",
         3: "marzo",
         4: "abril",
         5: "mayo",
         6: "junio",
         7: "julio",
         8: "agosto",
         9: "septiembre",
         10: "octubre",
         11: "noviembre",
         12: "diciembre"}


# Clases que voy a necesitar
class Gastos_e_ingresos:
    def __init__(self, dinero, motivo, ingreso = False):
        self.dinero = dinero
        self.motivo = motivo
        self.ingreso = ingreso

    def __str__(self):
        if self.ingreso:
            return f"Ingreso de {self.dinero} en {self.motivo}"
        else:
             return f"Gasto de {self.dinero} en {self.motivo}"

# Funciones
def consultar():
    fecha_consulta = input(("Ingrese la fecha (dd/mm) de consulta: "))
    mes = int(fecha_consulta[3:])
    dia = int(fecha_consulta[:2])
    prosa_fecha_inicio = f"Movimientos del día {dia}/{mes}:\n"
    prosa_fecha_final = f"Movimientos del día {dia+1}/{mes}:\n"
    try:
        with open(f"gastos_mes_{mes}.txt", "r") as f:
            lineas = f.readlines()
            index_inicio = lineas.index(prosa_fecha_inicio)
            index_final = lineas.index(prosa_fecha_final)
            lineas_consulta = lineas[index_inicio:index_final-2]
            lineas_final = []

            for linea in lineas_consulta:
                lineas_final.append(linea.replace('\n', ""))
            for linea in lineas_final:
                if linea == "":
                    idx = lineas_final.index(linea)
                    del lineas_final[idx]
            for linea in lineas_final:
                if linea != "Saldo nuevo: ":
                    try:
                        float(linea)
                    except ValueError:
                        print(linea)
            ver_saldo = input(f"Si desea ver el saldo inicial y final del día {fecha_consulta} ingrese 1, caso contrario ingrese otra letra.\n")
            if ver_saldo == "1":
                print(f"Saldo inicial:\n{lineas[index_inicio-2]}\n"
                      f"Saldo final:\n{lineas[index_final-2]}")

            f.close()
    except FileNotFoundError:
        print(f"No existe un archivo del mes {mes} para el año actual")

def general(rta):
    lista_gastos = []
    lista_ingresos = []
    prosa_ingresos = []
    prosa_gastos = []
    ingresos = 0
    salidas = 0
    if mes in meses:
        with open(f"gastos_mes_{mes}.txt", "a+") as f:
            f.seek(0)
            lineas = f.readlines()
            if len(lineas) == 0:
                try:
                    with open(f"gastos_mes_{mes-1}.txt", "r") as prev_f:
                        lineas = prev_f.readlines()
                        saldo_anterior = int(lineas[-1][:-3])
                        prev_f.close()
                except FileNotFoundError:
                    saldo_anterior = 0
            else:
                saldo_anterior = int(lineas[-1][:-3])
            f.close()
        nombre_mes = meses[mes]
        print(f"Ingresos y gastos del mes de {nombre_mes}")

        while rta == "g" or rta == "i":
            if rta == "g":
                monto = float(input("Ingrese el monto: "))
                razon = input("Ingrese en qué se gasto: ")
                gasto = Gastos_e_ingresos(monto, razon)
                gasto.__str__()
                lista_gastos.append(monto)
                prosa_gastos.append(gasto.__str__())
                rta = input("¿Desea ingresar otro monto? Presione g por i por ingresos, cualquier otra tecla por no.\n").lower()
            if rta == "i":
                monto = float(input("Ingrese el monto: "))
                razon = input("Ingrese a qué se debe: ")
                ingreso = Gastos_e_ingresos(monto, razon, True)
                ingreso.__str__()
                lista_ingresos.append(monto)
                prosa_ingresos.append(ingreso.__str__())
                rta = input("¿Desea ingresar otro monto? Presione g por i por ingresos, cualquier otra tecla por no.\n").lower()

    else:
        print("Debe ingresar un número entre 1 y 12.")

    for i in lista_ingresos:
        ingresos += i
    for j in lista_gastos:
        salidas += j
    saldo_mes = saldo_anterior + ingresos - salidas
    prosa_fecha = f"Movimientos del día {fecha}:\n"
    with open(f"gastos_mes_{mes}.txt", "a+") as f:
        f.seek(0)
        if prosa_fecha not in f.readlines():
            f.seek(len(f.readlines()))
            f.write(f"\nEl saldo al día {fecha} es: {saldo_anterior}\n\n")
            f.write(prosa_fecha)
        f.seek(len(f.readlines()))
        for line in prosa_gastos:
            f.write(line + "\n")
        for line in prosa_ingresos:
            f.write(line + "\n")
        f.write("Saldo nuevo: \n" + str(saldo_mes) + "\n")
        f.seek(0)
        lineas = f.readlines()
        for linea in lineas:
            print(linea, end = "")
        f.seek(len(f.readlines()))
        f.close()

while True:
    accion = input("Para ingresar movimientos presione 1, para consultar movimientos presione 2. Para salir presione cualquier otra tecla")
    if accion == "1":
        rta = input("¿Desea ingresar un gasto o un ingreso? Presione g para gasto e i para ingreso.\n").lower()
    elif accion == "2":
        consultar()
    else:
        break


