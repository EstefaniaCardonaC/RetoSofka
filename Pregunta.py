# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 15:07:08 2022

@author: estef
"""
import os
class Pregunta():
    def __init__(self,categoria,pregunta,opc1,opc2,opc3,opc4,respuesta):
        self.categoria=categoria
        self.pregunta=pregunta
        self.opcion1=opc1
        self.opcion2=opc2
        self.opcion3=opc3
        self.opcion4=opc4
        self.respuesta=respuesta
        
        if(os.path.exists("Categorias")==False):
            os.mkdir("Categorias")
        
        if(os.path.exists("Categorias/"+"Categoria"+str(self.categoria))==False):
            os.mkdir("Categorias/"+"Categoria"+str(self.categoria))
        
        self.preguntas=os.listdir("Categorias/"+"Categoria"+str(self.categoria))
        self.numeroPregunta=len(self.preguntas)+1
        self.archivoPregunta=open("Categorias/"+"Categoria"+str(self.categoria)+"/"+str(self.numeroPregunta)+".csv","w")
        self.archivoPregunta.write(str(self.pregunta)+"\n")
        self.archivoPregunta.write(str(self.opcion1)+"\n")
        self.archivoPregunta.write(str(self.opcion2)+"\n")
        self.archivoPregunta.write(str(self.opcion3)+"\n")
        self.archivoPregunta.write(str(self.opcion4)+"\n")
        self.archivoPregunta.write(str(self.respuesta))
        self.archivoPregunta.close()