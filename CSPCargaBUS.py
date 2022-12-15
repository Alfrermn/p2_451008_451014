import sys
from pathlib import Path
from constraint import *

"PATH, si no lo cargas con pycharm, probablemente tengas que cambiar el path a donde lo tengas y con el nombre que tengas"
Path= str(Path.home()) + "/PycharmProjects/Parte1/CSP-tests/"

"Clase para establecer los dominios"
class Dominios():
    def __init__(self, tupla):
        self.problema = Problem()
        "Lista que sacamos de los archivos con los pasajeros"
        self.tupla = tupla
        "Listas alumnos mov_reducida, totales, hermanos y problemáticos"
        self.lista_reducidos=[]
        self.lista_alumnos_totales= []
        self.lista_alumnos_hermanos=[]
        self.lista_alumnos_problematicos=[]

    """Esta función sirve básicamente para contar el número de alumnos de cada tipo e incluirlos en las listas y para formar los dominios.
    Con los dominios nos referimos a los posibles lugares donde pueden ir"""
    def cuenta_alumnos(self):
        "Abrimos la tupla que es una lista de listas, donde cada lista contiene los datos de un alumno"
        for i in range(len(self.tupla)):
            """Cada lista que abra será un alumno nuevo, por lo que los alumnos totales aumentarán en 1.
            i=0 en la primera iteración al ser listas, por lo que ponemos i+1."""
            self.lista_alumnos_totales.append(i+1)
            "Si el alumno es conflictivo, lo añadimos a la lista de alumnos conflictivos"
            if self.tupla[i][2]=="C":
                self.lista_alumnos_problematicos.append(i+1)
            "Si el alumno tiene movilidad reducida"
            if self.tupla[i][3]=="R":
                "Añadimos al alumno a la lista de movilidad reducida"
                self.lista_reducidos.append(i+1)
                "Y además tiene hermanos"
                if self.tupla[i][4]!=0:
                    """Las siguientes 4 líneas sirven para añadir a los hermanos en una misma lista dentro de la lista
                    de hermanos, es decir, [1,3],[3,1] significa que la persona 1 es hermano de la 3"""
                    lista_apoyo=[]
                    lista_apoyo.append(i+1)
                    lista_apoyo.append(self.tupla[i][4])
                    self.lista_alumnos_hermanos.append(lista_apoyo)
                    "Comprobamos si están en el mismo ciclo, si lo están:"
                    if self.tupla[i][1]== (self.tupla[(self.tupla[i][4]-1)][1]):
                        "Miramos a ver en que ciclo está"
                        if tupla[i][1]==1:
                            "Si está en el ciclo 1 añadimos los posibles dominios"
                            self.problema.addVariable(self.tupla[i][0],[1,2,3,4,13,14,15,16])
                        else:
                            "Está en el cilo 2 y añadimos los posibles dominios"
                            self.problema.addVariable(self.tupla[i][0],[17,18,19,20])
                    else:
                        "No están en el mismo ciclo, por lo que irá al primero"
                        self.problema.addVariable(self.tupla[i][0],[1,2,3,4,13,14,15,16])
                else:
                    "Si no tiene hermanos, simplemente comprueba el ciclo que tiene y añade su dominio"
                    if self.tupla[i][1] == 1:
                        self.problema.addVariable(self.tupla[i][0], [1, 2, 3, 4, 13, 14, 15, 16])
                    else:
                        self.problema.addVariable(self.tupla[i][0], [17, 18, 19, 20])
            else:
                "Si no tiene movilidad reducida hace exactamente lo mismo que las de arriba, cambiando los dominios."
                if self.tupla[i][4]!=0:
                    lista_apoyo = []
                    lista_apoyo.append(i + 1)
                    lista_apoyo.append(self.tupla[i][4])
                    self.lista_alumnos_hermanos.append(lista_apoyo)
                    # Comprobamos si están en el mismo ciclo
                    if self.tupla[i][1] == (self.tupla[(self.tupla[i][4]-1)][1]):
                        # Miramos a ver en que ciclo están
                        if self.tupla[i][1] == 1:
                            self.problema.addVariable(self.tupla[i][0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
                        else:
                            self.problema.addVariable(self.tupla[i][0], [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
                    else:
                        self.problema.addVariable(self.tupla[i][0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
                else:
                    if self.tupla[i][1] == 1:
                        self.problema.addVariable(self.tupla[i][0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
                    else:
                        self.problema.addVariable(self.tupla[i][0], [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
        return self.lista_alumnos_problematicos, self.lista_alumnos_hermanos, self.lista_alumnos_totales, self.lista_reducidos


    #####RESTRICCIONES#####
    "Comprueba si los alguno de los hermanos tiene movilidad reducida, si no tiene movilidad reducida, se añade la restricción de que vayan juntos."
    def comprobar_hermanos(self, lista_hermanos, lista_personas_mov_reducida):
        grupo1=0
        grupo2=1
        for i in lista_hermanos:
            reducida=True
            for j in lista_personas_mov_reducida:
                if i[0]==j or i[1]==j:
                    reducida=False

            for b in range(len(self.tupla)):
                if i[0]==self.tupla[b][0]:
                    grupo1=self.tupla[b][1]
                if i[1]==self.tupla[b][0]:
                    grupo2=self.tupla[b][1]

            if reducida:
                if grupo1==grupo2:
                    self.problema.addConstraint(Dominios.restriccion_hermanos_juntos, (i[0],i[1]))
                elif grupo1 > grupo2:
                    self.problema.addConstraint(Dominios.restriccion_hermanos_juntos_ciclo_distinto, (i[0], i[1]))
                else:
                    self.problema.addConstraint(Dominios.restriccion_hermanos_juntos_ciclo_distinto, (i[1], i[0]))

    "No pueden estar separados por el pasillo, y si uno está a la derecha (%2==0), el otro tiene que estar a la izq"
    @staticmethod
    def restriccion_hermanos_juntos(x,y):
        if x==y+1 and x%2==0:
            return True
        if y==x+1 and y%2==0:
            return True
        else:
            return False
    "No pueden estar separados por el pasillo y si tienen ciclos distintos, el de mayor tiene que estar al lado del pasillo."
    @staticmethod
    def restriccion_hermanos_juntos_ciclo_distinto(x,y):
        if x== y + 1 and (x%4)==2 and (x%2)==0:
            return True
        elif x== y -1 and (x%4)==3 and (x%2)==1:
            return True
        else:
            return False
    """Miramos si los hermanos son problemático, si no son problemáticos añadimos la restricción, además, comprobamos que"
    si un alumno es conflictivo no puede ir cerca de un alumno de movilidad reducida"""
    def comprobar_conflictivas(self, lista_hermanos, lista_alumnos_problematicos, lista_reducida):
        for i in lista_alumnos_problematicos:
            for j in lista_alumnos_problematicos:
                hermanos = False
                for z in lista_hermanos:
                    if i==z[0] and j==z[1]:
                        hermanos=True
                if hermanos==False and i!=j:
                    self.problema.addConstraint(Dominios.restriccion_conflictivas, (i,j))
        for i in lista_alumnos_problematicos:
            for j in lista_reducida:
                hermanos = False
                for z in lista_hermanos:
                    if i==z[0] and j==z[1]:
                        hermanos=True
                if hermanos==False and i!=j:
                    self.problema.addConstraint(Dominios.restriccion_conflictivas, (i,j))
    "Indica las posiciones de un alumno problemático con respecto a otro, como si fuera en buscaminas (8 alrededor)"
    @staticmethod
    def restriccion_conflictivas(x,y):
        "Ventanas de izquierda y derecha, que solo tienen restringidos ciertos sitios para la otra persona"
        if x%4==0:
            if (x-1==y) or (x-4==y) or (x+4==y) or (x-5==y) or (x+3==y):
                return False
            else:
                return True
        elif x%4==1:
            if (x + 1 == y) or (x - 4 == y) or (x + 5 == y) or (x + 4 == y) or (x - 3 == y):
                return False
            else:
                return True
        else:
            "No está en ninguna ventana, no puede haber nadie cerca"
            if (x + 1 == y) or (x - 1 == y) or (x + 3 == y) or (x + 4 == y) or (x - 3 == y) or (x - 4 == y) or (x + 5 == y) or (x - 5 == y):
                return False
            else:
                return True

    "Esto sirve para añadir la restricción de que si los alumnos tienen movilidad reducida vayan solos"
    def comprobar_mov_reducida(self, lista_mov_reducida, lista_total):
        for i in lista_mov_reducida:
            for j in lista_total:
                self.problema.addConstraint(Dominios.restriccion_solos, (i,j))

    "Según el lado de la ventana donde esten, no puede haber nadie a su lado"
    @staticmethod
    def restriccion_solos(x,y):
        if x%2==0 and x!=y+1:
            return True
        if x%2==1 and x!=y-1:
            return True
        else:
            return False

"Esta función coge los valores del archivo entrada y los guarda en una lista de listas, con cada lista siendo un pasajero"
def sacar_valores_tupla(archivo):
    """Es difícil de explicar, pero para que funcione, si el número de pasajeros es 5, las lineas del archivo de entrada
    han de ser 6, dejando la sexta vacía"""
    with open(archivo, "r") as file:
        x=file.read()
    tupla = []
    tupla1=[]
    contador = 0
    contador2 = 1
    for i in x:
        if i == "\n":
            contador2 += 1
            tupla1=[]
            contador = 0
        if i != "," and i != "\n":
            if contador2 < 10:
                if contador == 0:
                    tupla1.append(i)
                    contador += 1
                elif contador == 2:
                    tupla1.append(i)
                    contador+=1
                elif contador==3:
                    tupla1.append(i)
                    contador+=1
                elif contador>3:
                    k=tupla1.pop()
                    x=tupla1.pop()
                    z=tupla1.pop()
                    anadir= z+x+k
                    tupla.append(anadir)
                else:
                    contador+=1
            elif contador2>=10:
                if contador == 0:
                    tupla1.append(i)
                    contador += 1
                elif contador ==1:
                    tupla1.append(i)
                    contador+=1
                elif contador == 3:
                    tupla1.append(i)
                    contador += 1
                elif contador ==4:
                    tupla1.append(i)
                    contador += 1
                elif contador>=4:
                    k = tupla1.pop()
                    x = tupla1.pop()
                    z = tupla1.pop()
                    a= tupla1.pop()
                    anadir = z + x + k + a
                    tupla.append(anadir)
                else:
                    contador+=1
            else:
                continue
    if contador2 == 32:
        tupla.append(tupla1)
        contador2 += 1

    file.close()
    return tupla

"""Esta función sirve para lo mismo que lo de arriba, pero sirve para el output, extrayendo el ID,si es conflictivo o no
y si tiene mov. reducida o no la tiene"""
def extraer_tupla(archivo):
    with open(archivo, "r") as file:
        x= file.read()
    tupla= []
    contador=0
    tupla1 = []
    contador2=1
    for i in x:
        if i=="\n":
                contador2+=1
                tupla.append(tupla1)
                contador=0
                tupla1 = []
        if i!="," and i!="\n":
            if contador2<10:
                if contador==0 or contador==1:
                    i= int(i)
                    tupla1.append(i)
                    contador+=1
                elif contador==4:
                    j=int(i)
                    tupla1.append(j)
                    contador += 1
                elif contador==5:

                        x=tupla1.pop()
                        x=str(x)
                        y=x+i
                        y=int(y)
                        tupla1.append(y)
                        contador += 1
                else:
                    tupla1.append(i)
                    contador+=1
            else:
                if contador==0:
                    tupla1.append(contador2)
                    contador += 1
                elif contador==5:
                    j=int(i)

                    tupla1.append(j)
                    contador += 1
                elif contador==6:

                    x = tupla1.pop()
                    x = str(x)
                    y = x + i
                    y = int(y)

                    tupla1.append(y)
                    contador += 1
                elif contador==2:
                        i=int(i)
                        tupla1.append(i)
                        contador += 1
                elif contador==3 or contador==4:
                    tupla1.append(i)
                    contador+=1
                else:
                    contador+=1
    if contador2 == 32:
        tupla.append(tupla1)
        contador2 += 1

    file.close()
    return tupla

"Esto produce el archivo resultado de la forma indicada en la práctica"
def obtener_archivo_resultado(archivo):
    final= archivo + ".output"
    with open (final, "w") as file:
        file.write("Número de soluciones:" + str(len(Calculo_alumnos.problema.getSolutions())) + "\n")
        counter=0
        k= sacar_valores_tupla(archivo)
        for i in Calculo_alumnos.problema.getSolutions():
            keys= i.keys()
            sorted_keys= sorted(keys)
            sorteds = {}
            lista_apoyo=[]
            for llave in sorted_keys:
                lista_apoyo.append(i[llave])
            counter2=0
            for llave2 in k:
                sorteds[llave2] = lista_apoyo[counter2]
                counter2+=1
            if counter<3:
                file.write(str(sorteds)+"\n")
                counter+=1
            else:
                break
    file.close()


"Recibimos el archivo a través de consola, para ello simplemente usamos python CSPCargaBUS.py alumnosXX"
archivo= Path+ sys.argv[1]
"Sacamos la lista de listas del archivo introducido"
tupla= extraer_tupla(archivo)
"Calculamos los dominios"
Calculo_alumnos = Dominios(tupla)
"Calculamos cuantos alumnos de cada tipo hay"
alumnos_problematicos, hermanos, alumnos_totales, alumnos_mov_red = Calculo_alumnos.cuenta_alumnos()
"Añadimos las restricciones"
Calculo_alumnos.comprobar_hermanos(hermanos, alumnos_mov_red)
Calculo_alumnos.comprobar_conflictivas(hermanos, alumnos_problematicos, alumnos_mov_red)
Calculo_alumnos.comprobar_mov_reducida(alumnos_mov_red, alumnos_totales)
Calculo_alumnos.problema.addConstraint(AllDifferentConstraint(), Calculo_alumnos.problema._variables)
"Imprimimos el archivo resultado"
obtener_archivo_resultado(archivo)

