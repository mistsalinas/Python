
# Archivo principal
"""
El objetivo de este programa es hacer un cálculo de mis gastos mensuales,
con detalle de entradas, salidas, etc. Mes a mes.
Cada vez que inicia un mes tengo el saldo de los anteriores  y empiezo con ese monto.
"""

"""
Qué quise lograr con mis modificaciones:
    - Distinguir si se trata de un ingreso o egreso, personalizar el mensaje según corresponda.
    - Llevar un control de gastos diario, por cada movimiento actualizar el saldo en el momento.
    - Que el movimiento se guarde con fecha de registro.
    - Acumular mes a mes, sobrantes o deudas. Se cumple que cada día inicio con el saldo del día anterior así sea primero de mes.
    - Consultar los movimientos de un día particular, siempre que ese día tenga el registro.
    - Consultar movimientos de todo el mes.
    - La primera vez que cargo un movimiento en el día, ver el saldo inicial. Luego por cada ingreso en esa misma fecha sólo se muestra el movimiento y la actualización del saldo.
    - Contemplar la mayor cantidad de excepciones. 
"""

# Automatización de la fecha

from datetime import date


# Variables que voy a necesitar
fecha = str(date.today())
mes = int(fecha[5:7])
dia = fecha[8:]
fecha = f"{dia}/{mes}"

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
    def __init__(self, dinero, motivo, ingreso = False): # Añado parámetro para distinguir si se trata de ingreso o egreso
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

    rta = input("Para ver todos los movimientos de un mes presione 1. Para consultar por una fecha presione 2: ")
    
    # Imprimo todo lo que haya en el txt del mes elegido
    if rta == '1':
        try:
            mes = input("Ingrese el número de mes por el que desea consultar: ")
            with open(f"gastos_mes_{mes}.txt", "r") as f:
                lineas = f.readlines()
                for linea in lineas:
                    print(linea, end = "")
                
        except FileNotFoundError:
            print(f"No hay registros del mes: {mes}")
            
    # Imprimo sólo los movimientos de una fecha particular. Voy a usar como límite inicial y final las prosas que siempre son iguales, pero cambian la fecha
    elif rta == '2': 
        try:
            fecha_consulta = input(("Ingrese la fecha (dd/mm) de consulta: "))
            mes = int(fecha_consulta[3:])
            dia = int(fecha_consulta[:2])
            prosa_fecha_inicio = f"Movimientos del día {dia}/{mes}:\n"
            prosa_fecha_final = f"Movimientos del día {dia+1}/{mes}:\n"
            no_next = False
            try:
                with open(f"gastos_mes_{mes}.txt", "r") as f:
                    lineas = f.readlines()
                    try:
                        index_inicio = lineas.index(prosa_fecha_inicio)
                    except ValueError:
                        print("No posee registros del día ingresado")
                        consultar()
                    try:
                        index_final = lineas.index(prosa_fecha_final)  
                    except ValueError: # Puede pasar que quiera consultar por una fecha que se encuentre al final del archivo
                        no_next = True
                        index_final = len(lineas) - 1
                    lineas_consulta = lineas[index_inicio:index_final-1]
                    lineas_final = []
                    
                    # Acá intenté de limpiar los saltos de línea, no sé si lo hice de manera efectiva...
                    for linea in lineas_consulta:
                        lineas_final.append(linea.replace('\n', ""))
                    for linea in lineas_final:
                        if linea == "":
                            idx = lineas_final.index(linea)
                            del lineas_final[idx]
                            
                    # Que imprima todo lo que no diga saldo y que no sea un número, sólo gastos e ingresos
                    for linea in lineas_final:
                        if linea != "Saldo: ":
                            try:
                                float(linea)
                            except ValueError:
                                print(linea)
                                
                    # Opción de ver saldo inicial y final 
                    ver_saldo = input(f"Si desea ver el saldo inicial y final del día {fecha_consulta} ingrese 1, caso contrario ingrese otra letra.\n")
                    if ver_saldo == "1":
                        if no_next:
                            print(f"Saldo inicial:\n{lineas[index_inicio-1][33:]}\n"
                                  f"Saldo final:\n{lineas[index_final]}")
                        else:
                            print(f"Saldo inicial:\n{lineas[index_inicio-1][33:]}\n"
                                  f"Saldo final:\n{lineas[index_final-3]}")
                    f.close()
                    
            # Manejo de excepciones
            except FileNotFoundError:
                print(f"No existe un archivo del mes {mes} para el año actual")
        except ValueError:
            print("Ingrese una fecha válida.")
    else:
        print("Solicitud inválida")
    global accion
    accion = input("Para realizar otra consulta presione 2. Para registrar un movimiento presione 1. Para salir presione cualquier otra tecla:\n")


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
            final = len(lineas) # Asigno el final del archivo ni bien lo abro a una variable, para no imprimir todo cada vez que hago un movimiento
            
            if len(lineas) == 0: # Si el archivo está vacío estamos empezando de 0 o bien arrancando un nuevo mes
                try:
                    with open(f"gastos_mes_{mes-1}.txt", "r") as prev_f:
                        lineas = prev_f.readlines()
                        saldo_anterior = float(lineas[-1][:-3]) # Si es un nuevo mes, traigo el saldo final del anterior
                        prev_f.close()
                except FileNotFoundError: # Si no hay nada del mes anterior, arranco de 0
                    saldo_anterior = 0
            else:
                saldo_anterior = int(lineas[-1][:-3]) # Si el archivo no está vacío traigo el saldo del día anterior
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
            f.write(f"\nEl saldo inicial al día {fecha} es: {saldo_anterior}\n")
            f.write(prosa_fecha)
        f.seek(len(f.readlines()))
        for line in prosa_gastos:
            f.write(line + "\n")
        for line in prosa_ingresos:
            f.write(line + "\n")
        f.write("Saldo: \n" + str(saldo_mes) + "\n")
        f.seek(0)
        lineas = f.readlines()[final:]
        for linea in lineas:
            print(linea, end = "")
        f.seek(len(f.readlines()))
        f.close()
        
        global accion
        accion = input("Para registrar un movimiento presione 1. Para realizar una consulta presione 2. Para salir presione cualquier otra tecla:\n")

# Inicio del programa y definición de la acción del usuario
def inicio():
    global accion
    accion = input("Para registrar movimientos presione 1, para consultar presione 2. Para salir presione cualquier otra tecla:\n")
    while accion == '1' or accion == '2':
        if accion == "1":
            rta = input("¿Desea registrar un gasto o un ingreso? Presione 'g' para gasto e 'i' para ingreso.\n").lower()
            general(rta)
        elif accion == "2":
            consultar()
        else:
            break

inicio()
