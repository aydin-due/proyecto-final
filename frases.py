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