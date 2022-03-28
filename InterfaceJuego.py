# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:52:02 2022

@author: estef
"""

import os
import time
import sys
import random
from PyQt5.QtWidgets import QWidget,QDialog,QGroupBox,QTableWidget,QTableWidgetItem,QSizePolicy,QFormLayout,QMessageBox,QCheckBox,QLabel,QDateEdit,QLineEdit,QComboBox,QApplication,QHBoxLayout,QVBoxLayout,QPushButton
from PyQt5.QtCore import pyqtSignal,QThread,QDateTime,Qt,QSize,QDate
from PyQt5.QtGui import QFont,QIcon,QPixmap,QImage,QColor,QPainter,QPen,QBrush
from Jugador import Jugador
from Pregunta import Pregunta

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.nombreJugador=""
        self.puntaje=""
        self.puntajePartida=0
        self.ronda=1
        self.incremento=10
        self.opc=0
        self.showMaximized()
        self.setWindowTitle('Juego preguntas y respuestas')
        self.setGeometry(40,40,1400,700) 
        self.hboxPrincipal=QHBoxLayout()
        self.setLayout(self.hboxPrincipal)
        
        
        self.grupoBotones=QGroupBox()
       
        self.grupoBotones.setFixedSize(230, 350)
        self.vboxBotonesPrincipales=QVBoxLayout()
        
        #BOTONES PARA INICIAR JUEGO, INGRESAR USUARIO Y CONFIGURAR JUEGO
        self.botonIniciar=QPushButton("Iniciar Juego")
        self.botonIniciar.clicked.connect(self.iniciar)
        self.vboxBotonesPrincipales.addWidget(self.botonIniciar)
        
        self.botonJugador=QPushButton("Ingresar Jugador")
        self.botonJugador.clicked.connect(self.jugador)
        self.vboxBotonesPrincipales.addWidget(self.botonJugador)
        
        self.botonConfiguracion=QPushButton("Configurar Juego")
        self.botonConfiguracion.clicked.connect(self.configuracion)
        self.vboxBotonesPrincipales.addWidget(self.botonConfiguracion)
        
        #AGREGO EL LAYOUT DE LOS BOTONES A LA PANTALLA PRINCIPAL
        self.grupoBotones.setLayout(self.vboxBotonesPrincipales)
        self.hboxPrincipal.addWidget(self.grupoBotones)
        
        
        self.show()
    
    def iniciar(self):
        if(os.path.exists("Categorias")==False or os.path.exists("Categorias/"+"Categoria1")==False or os.path.exists("Categorias/"+"Categoria2")==False or os.path.exists("Categorias/"+"Categoria3")==False or os.path.exists("Categorias/"+"Categoria4")==False or os.path.exists("Categorias/"+"Categoria5")==False):
            mensaje=QMessageBox(QMessageBox.Warning, "Advertencia", "Debe configurar las preguntas para iniciar el juego", buttons = QMessageBox.Ok, parent=self)
            mensaje.exec_()
        else:
            if(len(os.listdir("Categorias/"+"Categoria1"))<=4 or len(os.listdir("Categorias/"+"Categoria2"))<=4 or len(os.listdir("Categorias/"+"Categoria3"))<=4 or len(os.listdir("Categorias/"+"Categoria4"))<=4 or len(os.listdir("Categorias/"+"Categoria5"))<=4):
                mensaje=QMessageBox(QMessageBox.Warning, "Advertencia", "Cada categoria debe contar con minimo 5 preguntas\n Categoria 1: "+str(len(os.listdir("Categorias/"+"Categoria1")))
                                    +"\n Categoria 2: "+str(len(os.listdir("Categorias/"+"Categoria2")))
                                    +"\n Categoria 3: "+str(len(os.listdir("Categorias/"+"Categoria3")))
                                    +"\n Categoria 4: "+str(len(os.listdir("Categorias/"+"Categoria4")))
                                    +"\n Categoria 5: "+str(len(os.listdir("Categorias/"+"Categoria5"))), buttons = QMessageBox.Ok, parent=self)
                mensaje.exec_()
                
            else:
                if(self.nombreJugador==""):
                    mensaje=QMessageBox(QMessageBox.Warning, "Advertencia", "Debe ingresar el nombre del jugador", buttons = QMessageBox.Ok, parent=self)
                    mensaje.exec_()
                else:
                    self.vboxJuego=QVBoxLayout()
                    self.hboxInfoJugador=QHBoxLayout()
                    self.hboxInfoJugador.addWidget(QLabel("JUGADOR: "+self.nombreJugador))
                    self.hboxInfoJugador.addWidget(QLabel("PUNTAJE MAXIMO OBTENIDO: "+str(self.puntaje)))
                    self.vboxJuego.addLayout(self.hboxInfoJugador)
                    self.labelPuntajePartida=QLabel("PUNTAJE PARTIDA: "+str(self.puntajePartida))
                    self.vboxJuego.addWidget(self.labelPuntajePartida)
                    
                    self.hboxPreguntasYRespuestas=QHBoxLayout()
                    
                    #GRUPO DONDE SE MUESTRA LA PREGUNTA CON LAS 4 OPCIONES DE RESPUESTA
                    self.grupoPreguntas=QGroupBox("PREGUNTAS Y RESPUESTAS")
                    self.vboxOpciones=QVBoxLayout()
                    self.grupoPreguntas.setLayout(self.vboxOpciones)
                    
                    self.preguntaRandom=random.randint(1,len(os.listdir("Categorias/"+"Categoria1")))
                    self.pregunta=open("Categorias/"+"Categoria1"+"/"+str(self.preguntaRandom)+".csv","r")
                    
                    self.labelPregunta=QLabel("Pregunta: "+self.pregunta.readline())
                    self.labelOpcion1=QLabel("Opción 1: "+self.pregunta.readline())
                    self.labelOpcion2=QLabel("Opción 2: "+self.pregunta.readline())
                    self.labelOpcion3=QLabel("Opción 3: "+self.pregunta.readline())
                    self.labelOpcion4=QLabel("Opción 4: "+self.pregunta.readline())
                    self.pregunta.close()
                    
                    self.vboxOpciones.addWidget(self.labelPregunta)
                    self.vboxOpciones.addWidget(self.labelOpcion1)
                    self.vboxOpciones.addWidget(self.labelOpcion2)
                    self.vboxOpciones.addWidget(self.labelOpcion3)
                    self.vboxOpciones.addWidget(self.labelOpcion4)
                    
                    self.hboxPreguntasYRespuestas.addWidget(self.grupoPreguntas)
                    
                    #GRUPO DONDE SE DEBE ELEGIR LA RESPUESTA
                    self.grupoOpcionesRespuesta=QGroupBox("ELIJA LA RESPUESTA A LA PREGUNTA")
                    self.vboxOpcionesRespuesta=QVBoxLayout()
                    self.grupoOpcionesRespuesta.setLayout(self.vboxOpcionesRespuesta)
                    self.opcion1=QCheckBox("Opción 1")
                    self.opcion1.stateChanged.connect(self.validacion)
                    self.vboxOpcionesRespuesta.addWidget(self.opcion1)
                    self.opcion2=QCheckBox("Opción 2")
                    self.opcion2.stateChanged.connect(self.validacion)
                    self.vboxOpcionesRespuesta.addWidget(self.opcion2)
                    self.opcion3=QCheckBox("Opción 3")
                    self.opcion3.stateChanged.connect(self.validacion)
                    self.vboxOpcionesRespuesta.addWidget(self.opcion3)
                    self.opcion4=QCheckBox("Opción 4")
                    self.opcion4.stateChanged.connect(self.validacion)
                    self.vboxOpcionesRespuesta.addWidget(self.opcion4)
                    
                    self.hboxPreguntasYRespuestas.addWidget(self.grupoOpcionesRespuesta)
                    
                    self.hboxPrincipal.addLayout(self.vboxJuego)
                    
                    self.vboxJuego.addLayout(self.hboxPreguntasYRespuestas)
                    
                    
                    #GRUPO BOTONES RETIRARSE Y ENVIAR
                    self.hboxBotones=QHBoxLayout()
                    self.botonRetirarse=QPushButton("Retirarse")
                    self.botonRetirarse.clicked.connect(self.retirarse)
                    self.hboxBotones.addWidget(self.botonRetirarse)
                    self.botonGuardarRespuesta=QPushButton("Enviar")
                    self.botonGuardarRespuesta.clicked.connect(self.enviar)
                    self.hboxBotones.addWidget(self.botonGuardarRespuesta)
                    self.botonSiguiente=QPushButton("Siguiente")
                    self.botonSiguiente.clicked.connect(self.seguir)
                    self.hboxBotones.addWidget(self.botonSiguiente)
                    
                    self.vboxJuego.addLayout(self.hboxBotones)
                    
                        
    def jugador(self):
        self.ventanaInfoJugador=IngresarJugador()
        self.ventanaInfoJugador.sJugador.connect(self.infoJugador)
        self.ventanaInfoJugador.show()
    def infoJugador(self,nombre,puntaje):
        self.nombreJugador=nombre
        self.puntaje=puntaje
    def configuracion(self):
        self.ventanaConfiguracion=Configuracion()
        self.ventanaConfiguracion.show()
        
    def validacion(self,estado):
        if estado==Qt.Checked:
            if (self.sender()==self.opcion1):
                self.opcion2.setChecked(False)
                self.opcion3.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=1
            elif (self.sender()==self.opcion2):
                self.opcion1.setChecked(False)
                self.opcion3.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=2
            elif (self.sender()==self.opcion3):
                self.opcion1.setChecked(False)
                self.opcion2.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=3
            elif (self.sender()==self.opcion4):
                self.opcion1.setChecked(False)
                self.opcion2.setChecked(False)
                self.opcion3.setChecked(False)
                self.opc=4
    def retirarse(self):
        pass
    
    def seguir(self):
        if(self.ronda!=1 and self.ronda<=5):
            self.preguntaRandom=random.randint(1,len(os.listdir("Categorias/"+"Categoria"+str(self.ronda))))
            self.pregunta=open("Categorias/"+"Categoria"+str(self.ronda)+"/"+str(self.preguntaRandom)+".csv","r")
            self.labelPregunta.setText("Pregunta: "+self.pregunta.readline())
            self.labelOpcion1.setText("Opción 1: "+self.pregunta.readline())
            self.labelOpcion2.setText("Opción 2: "+self.pregunta.readline())
            self.labelOpcion3.setText("Opción 3: "+self.pregunta.readline())
            self.labelOpcion4.setText("Opción 4: "+self.pregunta.readline())
            self.opcion1.setChecked(False)
            self.opcion2.setChecked(False)
            self.opcion3.setChecked(False)
            self.opcion4.setChecked(False)
            
    def enviar(self):
        
        if(self.ronda<=5):
            self.preguntaRandom=random.randint(1,len(os.listdir("Categorias/"+"Categoria"+str(self.ronda))))
            self.pregunta=open("Categorias/"+"Categoria"+str(self.ronda)+"/"+str(self.preguntaRandom)+".csv","r")
            self.pregunta.readline()
            self.pregunta.readline()
            self.pregunta.readline()
            self.pregunta.readline()
            self.pregunta.readline()
            if(int(self.pregunta.readline())==self.opc):
                self.puntajePartida+=self.incremento
                self.labelPuntajePartida.setText("PUNTAJE PARTIDA: "+str(self.puntajePartida))
                self.incremento+=10
                self.ronda+=1
                self.pregunta.close() 
                print(self.puntajePartida)
                
            else:
                self.ronda=1
                self.puntajePartida=0
                self.incremento=10
                
                print("perdiste")
                self.preguntaRandom=random.randint(1,len(os.listdir("Categorias/"+"Categoria1")))
                self.pregunta=open("Categorias/Categoria1"+"/"+str(self.preguntaRandom)+".csv","r")
                self.labelPregunta.setText("Pregunta: "+self.pregunta.readline())
                self.labelOpcion1.setText("Opción 1: "+self.pregunta.readline())
                self.labelOpcion2.setText("Opción 2: "+self.pregunta.readline())
                self.labelOpcion3.setText("Opción 3: "+self.pregunta.readline())
                self.labelOpcion4.setText("Opción 4: "+self.pregunta.readline())
                self.pregunta.close() 
             
           

class IngresarJugador(QWidget):
    sJugador=pyqtSignal(str,int)
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.puntaje=0
        self.nombre=""
        self.vboxInfoUsuario=QVBoxLayout()
        
        #FORMULARIO INFO JUGADOR
        self.labelNombre=QLabel("Ingrese el nombre de usuario")
        self.vboxInfoUsuario.addWidget(self.labelNombre)
        self.lineEditNombre=QLineEdit()
        self.vboxInfoUsuario.addWidget(self.lineEditNombre)
        self.botonGuardarInfoUsuario=QPushButton("Guardar")
        self.botonGuardarInfoUsuario.clicked.connect(self.guardar)
        self.vboxInfoUsuario.addWidget(self.botonGuardarInfoUsuario)
        self.setLayout(self.vboxInfoUsuario)
        
    
    def guardar(self):
        self.nombre=self.lineEditNombre.text()
        
        #SE VERIFICA SI EL USUARIO EXISTE
        if(os.path.exists("Jugadores/"+self.nombre)==False):
            self.jugador=Jugador(self.nombre,self.puntaje)
            self.sJugador.emit(self.nombre,self.puntaje)
        
        elif(os.path.exists("Jugadores/"+self.nombre)==True):
            self.docJugador=open("Jugadores/"+self.nombre+"/"+self.nombre+".csv","r")
            self.docJugador.readline()
            self.infoJugador=self.docJugador.readline().split(",")
            self.puntaje=self.infoJugador[1]
            
            self.nombreJugadorExistente=QLabel(self.infoJugador[0])
            self.puntajeJugadorExistente=QLabel(self.infoJugador[1])
            
            self.vboxInfoUsuario.addWidget(QLabel("Usuario existente"))
            self.vboxInfoUsuario.addWidget(self.nombreJugadorExistente)
            self.vboxInfoUsuario.addWidget(QLabel("Puntaje Máximo Obtenido"))
            self.vboxInfoUsuario.addWidget(self.puntajeJugadorExistente)
            self.sJugador.emit(self.infoJugador[0],int(self.puntaje))
        
class Configuracion(QWidget):
    def __init__(self):
        super().__init__()
        self.opc=0
        self.cat=0
        self.setGeometry(100,100,600,600)
        self.vboxConfiguracion=QVBoxLayout()
        self.hboxPreguntas=QHBoxLayout()
        self.vboxConfiguracion.addLayout(self.hboxPreguntas)
        
        #OPCIONES PARA ELEGIR A QUE CATEGORIA SE VAN AGREGAR PREGUNTAS
        #SEGUN DIFICULTAD
        
        self.grupoCategorias=QGroupBox("Elija la categoria de la pregunta")
        self.vboxCategorias=QVBoxLayout()
        self.grupoCategorias.setLayout(self.vboxCategorias)
        
        
        self.categoria1=QCheckBox("Categoria 1")
        self.categoria1.stateChanged.connect(self.verificacionCategorias)
        self.categoria2=QCheckBox("Categoria 2")
        self.categoria2.stateChanged.connect(self.verificacionCategorias)
        self.categoria3=QCheckBox("Categoria 3")
        self.categoria3.stateChanged.connect(self.verificacionCategorias)
        self.categoria4=QCheckBox("Categoria 4")
        self.categoria4.stateChanged.connect(self.verificacionCategorias)
        self.categoria5=QCheckBox("Categoria 5")
        self.categoria5.stateChanged.connect(self.verificacionCategorias)
        
        self.vboxCategorias.addWidget(self.categoria1)
        self.vboxCategorias.addWidget(self.categoria2)
        self.vboxCategorias.addWidget(self.categoria3)
        self.vboxCategorias.addWidget(self.categoria4)
        self.vboxCategorias.addWidget(self.categoria5)
        
        self.hboxPreguntas.addWidget(self.grupoCategorias)
        
        #LAYOUT PARA INGRESO DE PREGUNTAS Y RESPUESTAS
        self.grupoPreguntas=QGroupBox("Ingrese la pregunta con sus correspondientes 4 respuestas")
        self.vboxPreguntasYRespuestas=QVBoxLayout()
        self.grupoPreguntas.setLayout(self.vboxPreguntasYRespuestas)
        
        self.hboxPreguntasYOpciones=QHBoxLayout()
        self.vboxPreguntasYRespuestas.addLayout(self.hboxPreguntasYOpciones)
        
        self.formularioPregunta=QFormLayout()
        
        self.linePregunta=QLineEdit()
        self.formularioPregunta.addRow(QLabel("Pregunta"),self.linePregunta)
        
        self.lineOpcion1=QLineEdit()
        self.formularioPregunta.addRow(QLabel("Opción 1"),self.lineOpcion1)
        
        self.lineOpcion2=QLineEdit()
        self.formularioPregunta.addRow(QLabel("Opción 2"),self.lineOpcion2)
        
        self.lineOpcion3=QLineEdit()
        self.formularioPregunta.addRow(QLabel("Opción 3"),self.lineOpcion3)
        
        self.lineOpcion4=QLineEdit()
        self.formularioPregunta.addRow(QLabel("Opción 4"),self.lineOpcion4)
        
        self.formularioPregunta.setAlignment(Qt.AlignCenter)
        self.vboxPreguntasYRespuestas.addLayout(self.formularioPregunta)
        
        self.hboxPreguntas.addWidget(self.grupoPreguntas)
        
        
        #OPCIONES RESPUESTA
        self.grupoRespuestas=QGroupBox("Elija una respuesta para su pregunta")
        self.vboxRespuestas=QVBoxLayout()
        self.grupoRespuestas.setLayout(self.vboxRespuestas)
        
        self.opcion1=QCheckBox("Opción 1")
        self.opcion1.stateChanged.connect(self.verificacionRespuestas)
        self.opcion2=QCheckBox("Opción 2")
        self.opcion2.stateChanged.connect(self.verificacionRespuestas)
        self.opcion3=QCheckBox("Opción 3")
        self.opcion3.stateChanged.connect(self.verificacionRespuestas)
        self.opcion4=QCheckBox("Opción 4")
        self.opcion4.stateChanged.connect(self.verificacionRespuestas)
        
        self.vboxRespuestas.addWidget(self.opcion1)
        self.vboxRespuestas.addWidget(self.opcion2)
        self.vboxRespuestas.addWidget(self.opcion3)
        self.vboxRespuestas.addWidget(self.opcion4)
        
        self.hboxPreguntas.addWidget(self.grupoRespuestas)
        
        self.botonGuardar=QPushButton("Guardar Pregunta")
        self.botonGuardar.clicked.connect(self.guardar)
        self.vboxConfiguracion.addWidget(self.botonGuardar)
        
        self.setLayout(self.vboxConfiguracion)
    
    #FUNCION PARA DEJAR ELEGIR SOLO UNA CATEGORIA
    def verificacionCategorias(self,estado):
        if estado==Qt.Checked:
            if (self.sender()==self.categoria1):
                self.categoria2.setChecked(False)
                self.categoria3.setChecked(False)
                self.categoria4.setChecked(False)
                self.categoria5.setChecked(False)
                self.cat=1
            elif (self.sender()==self.categoria2):
                self.categoria1.setChecked(False)
                self.categoria3.setChecked(False)
                self.categoria4.setChecked(False)
                self.categoria5.setChecked(False)
                self.cat=2
            elif (self.sender()==self.categoria3):
                self.categoria1.setChecked(False)
                self.categoria2.setChecked(False)
                self.categoria4.setChecked(False)
                self.categoria5.setChecked(False)
                self.cat=3
            elif (self.sender()==self.categoria4):
                self.categoria1.setChecked(False)
                self.categoria2.setChecked(False)
                self.categoria3.setChecked(False)
                self.categoria5.setChecked(False)
                self.cat=4
            elif (self.sender()==self.categoria5):
                self.categoria1.setChecked(False)
                self.categoria2.setChecked(False)
                self.categoria3.setChecked(False)
                self.categoria4.setChecked(False)
                self.cat=5
    
    #FUNCION PARA ELEGIR SOLO UNA RESPUESTA
    def verificacionRespuestas(self,estado):
        if estado==Qt.Checked:
            if (self.sender()==self.opcion1):
                self.opcion2.setChecked(False)
                self.opcion3.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=1
            elif (self.sender()==self.opcion2):
                self.opcion1.setChecked(False)
                self.opcion3.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=2
            elif (self.sender()==self.opcion3):
                self.opcion1.setChecked(False)
                self.opcion2.setChecked(False)
                self.opcion4.setChecked(False)
                self.opc=3
            elif (self.sender()==self.opcion4):
                self.opcion1.setChecked(False)
                self.opcion2.setChecked(False)
                self.opcion3.setChecked(False)
                self.opc=4
                
    
    def guardar(self):
        if(self.cat!=0 and self.opc!=0 and self.linePregunta.text()!="" and self.lineOpcion1.text()!="" and self.lineOpcion2.text()!="" and self.lineOpcion3.text()!="" and self.lineOpcion4.text()!=""):
            self.pregunta=Pregunta(self.cat,self.linePregunta.text(),self.lineOpcion1.text(),self.lineOpcion2.text(),self.lineOpcion3.text(),self.lineOpcion4.text(),self.opc)
            mensaje=QMessageBox(QMessageBox.Information, "Preguntas", "La pregunta fue guardada con éxito", buttons = QMessageBox.Ok, parent=self)
            mensaje.exec_()
        else:
            mensaje=QMessageBox(QMessageBox.Warning, "Preguntas", "Ingrese todos los campos requeridos", buttons = QMessageBox.Ok, parent=self)
            mensaje.exec_()
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Interface()
    sys.exit(app.exec_())
        