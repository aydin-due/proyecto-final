import csv
import Levenshtein
import argparse
import os

class Buscador: 
    archivo = None
    frase = None
    limite = None
    listado = None

    def __init__(self, archivo, frase, limite) -> None:
        self.archivo = archivo
        self.frase = frase
        self.limite = float(limite)
    
    def buscar(self):
        listado = self.carga_csv()
        max_dist = 0
        if self.limite >= 10:
            self.limite=self.limite*.01
        elif self.limite >= 1:
            self.limite=self.limite*.1
        frases = self.filtrado(listado)
        return frases
    
    def carga_csv(self) -> list:
        lista = []
        try:
            with open(self.archivo,'r',encoding="UTF-8") as fh:
                lector_csv = csv.reader(fh)
                for linea in lector_csv:
                    lista.append(linea)
        except IOError as e:
            print(os.getcwd())
            print(e)
        return lista
    
    def filtrado(self, listado):
        distancias=[]
        peliculas=[]
        frases=[]
        for linea in listado:
            try:
                pelicula = linea[1]
                frase_lista = linea[0]
                año = linea[2]
                distancia = Levenshtein.ratio(frase_lista, self.frase)
                if distancia >= self.limite:
                    distancia = round(distancia,2)
                    frases.append(frase_lista)
                    res = [distancia, frase_lista, pelicula, año]
                    distancias.append(res)
                    if pelicula not in peliculas:
                        peliculas.append(pelicula)
            except IndexError as v:
                print(linea)
                print(v)
        return distancias
        '''
        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
        despliegue(distancias)
        print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")'''

#todo lo de abajo no se ocupa, lo dejo por si a caso
def carga_csv(archivo):
    lista = []
    try:
        with open(archivo,'r',encoding="UTF-8") as fh:
            lector_csv = csv.reader(fh)
            for linea in lector_csv:
                lista.append(linea)
    except IOError as e:
        print(os.getcwd())
        print(e)
    return lista

def filtrado(listado, limite, frase):
    distancias=[]
    peliculas=[]
    frases=[]
    for linea in listado:
        try:
            pelicula = linea[1]
            frase_lista = linea[0]
            año = linea[2]
            distancia = Levenshtein.ratio(frase_lista, frase)
            #if frase in frase1:
            if distancia >= limite:
                frases.append(frase_lista)
                res = (distancia, frase_lista, pelicula, año)
                distancias.append(res)
                if pelicula not in peliculas:
                    peliculas.append(pelicula)

        except IndexError as v:
            print(linea)
            print(v)
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    despliegue(distancias)
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    

def despliegue(listado):
    for elemento in listado:
        print(elemento)

def main(archivo,frase,limite):
    listado = carga_csv(archivo)
    max_dist = 0
    print("Frase a buscar: %s" % frase)
    if limite >= 10:
        limite=limite*.01
    elif limite >= 1:
        limite=limite*.1
    filtrado(listado,limite,frase)


if __name__ == "__main__":
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    frases = os.path.join(THIS_FOLDER, 'frases_celebres.csv')
    parse =argparse.ArgumentParser()
    parse.add_argument("-a","--archivo", dest="archivo", required=False, default=frases)
    parse.add_argument("-f", "--frase", dest="frase", required=False, default='todos estos momentos se perderan en el tiempo, como lagrimas bajo la lluvia')
    parse.add_argument("-l", "--limite", dest="limite", required=False, type=float,default=0.5)
    args = parse.parse_args()
    archivo = args.archivo
    frase = args.frase
    limite = args.limite
    main(archivo, frase, limite)