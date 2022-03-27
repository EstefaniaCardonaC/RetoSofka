# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 18:43:53 2022

@author: estef
"""

import os

class Jugador():
    def __init__(self,nombre,puntaje):
        self.nombre=nombre
        self.puntaje=puntaje
        
        if(os.path.exists("Jugadores")==False):
            os.mkdir("Jugadores")
        os.mkdir("Jugadores/"+self.nombre)
        
        documentoJugador=open("Jugadores/"+self.nombre+"/"+self.nombre+".csv","w")
        documentoJugador.write("Nombre,Puntaje\n")
        documentoJugador.write(self.nombre+","+str(self.puntaje))
        documentoJugador.close()


        