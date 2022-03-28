# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:52:02 2022

@author: estef
"""

import os
import sys
import random
from PyQt5.QtWidgets import QWidget,QDialog,QGroupBox,QSizePolicy,QFormLayout,QMessageBox,QCheckBox,QLabel,QLineEdit,QApplication,QHBoxLayout,QVBoxLayout,QPushButton
from PyQt5.QtCore import pyqtSignal,Qt,QSize
from PyQt5.QtGui import QFont
from Jugador import Jugador
from Pregunta import Pregunta

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.showMaximized()
        self.setWindowTitle('Juego preguntas y respuestas')
        self.setStyleSheet(""" color: #b1b1b1;background-color: #323232;""" )
        self.setGeometry(40,40,1000,700) 
        self.hboxPrincipal=QHBoxLayout()
        self.setLayout(self.hboxPrincipal)
        
        #VARIABLES PROYECTO
        self.nombreJugador=""
        self.puntaje=""
        self.puntajePartida=0
        self.ronda=1
        self.incremento=10
        self.opc=0
        self.banderaSiguiente=False
        self.banderaInicio=True
        self.estiloBotones="""color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);border-width: 1px;
        border-color: #1e1e1e;
        border-style: solid;
        border-radius: 6;
        padding: 3px;
        font-size: 15px;
        padding-left: 5px;
        padding-right: 5px;
        min-width: 40px;"""
        
        self.grupoBotones=QGroupBox()
       
        self.grupoBotones.setFixedSize(230, 350)
        self.vboxBotonesPrincipales=QVBoxLayout()
        
        #BOTONES PARA INICIAR JUEGO, INGRESAR USUARIO Y CONFIGURAR JUEGO
        self.botonIniciar=QPushButton("Iniciar Juego")
        self.botonIniciar.setStyleSheet(self.estiloBotones)
        self.botonIniciar.setFixedSize(200, 50)
        self.botonIniciar.clicked.connect(self.iniciar)
        self.vboxBotonesPrincipales.addWidget(self.botonIniciar)
        
        self.botonJugador=QPushButton("Ingresar Jugador")
        self.botonJugador.setStyleSheet(self.estiloBotones)
        self.botonJugador.setFixedSize(200, 50)
        self.botonJugador.clicked.connect(self.jugador)
        self.vboxBotonesPrincipales.addWidget(self.botonJugador)
        
        self.botonConfiguracion=QPushButton("Configurar Juego")
        self.botonConfiguracion.setStyleSheet(self.estiloBotones)
        self.botonConfiguracion.setFixedSize(200, 50)
        self.botonConfiguracion.clicked.connect(self.configuracion)
        self.vboxBotonesPrincipales.addWidget(self.botonConfiguracion)
        
        #AGREGO EL LAYOUT DE LOS BOTONES A LA PANTALLA PRINCIPAL
        self.grupoBotones.setLayout(self.vboxBotonesPrincipales)
        self.hboxPrincipal.addWidget(self.grupoBotones)
        
        
        self.show()
    
    def iniciar(self):
        if(self.banderaInicio==True):
            self.banderaInicio=False
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
                        self.labelJug=QLabel("JUGADOR: "+self.nombreJugador)
                        self.labelJug.setFont(QFont("Sanserif",10))
                        self.hboxInfoJugador.addWidget(self.labelJug)
                        self.labelPunt=QLabel("PUNTAJE MAXIMO OBTENIDO: "+str(self.puntaje))
                        self.labelPunt.setFont(QFont("Sanserif",10))
                        self.hboxInfoJugador.addWidget(self.labelPunt)
                        self.vboxJuego.addLayout(self.hboxInfoJugador)
                        self.labelPuntajePartida=QLabel("PUNTAJE PARTIDA: "+str(self.puntajePartida))
                        self.labelPuntajePartida.setFont(QFont("Sanserif",10))
                        self.vboxJuego.addWidget(self.labelPuntajePartida)
                        self.labelRonda=QLabel("RONDA: "+str(self.ronda))
                        self.labelRonda.setFont(QFont("Sanserif",10))
                        self.vboxJuego.addWidget(self.labelRonda)
                        
                        self.hboxPreguntasYRespuestas=QHBoxLayout()
                        
                        #GRUPO DONDE SE MUESTRA LA PREGUNTA CON LAS 4 OPCIONES DE RESPUESTA
                        self.grupoPreguntas=QGroupBox("PREGUNTAS Y RESPUESTAS")
                        self.vboxOpciones=QVBoxLayout()
                        self.grupoPreguntas.setLayout(self.vboxOpciones)
                        
                        self.preguntaRandom=random.randint(1,len(os.listdir("Categorias/"+"Categoria1")))
                        self.pregunta=open("Categorias/"+"Categoria1"+"/"+str(self.preguntaRandom)+".csv","r")
                        
                        self.labelPregunta=QLabel("Pregunta: "+self.pregunta.readline())
                        self.labelPregunta.setStyleSheet(""" font-size: 15px;color: #b1b1b1;""")
                        self.labelOpcion1=QLabel("Opción 1: "+self.pregunta.readline())
                        self.labelOpcion1.setStyleSheet(""" font-size: 15px;color: #b1b1b1;""")
                        self.labelOpcion2=QLabel("Opción 2: "+self.pregunta.readline())
                        self.labelOpcion2.setStyleSheet(""" font-size: 15px;color: #b1b1b1;""")
                        self.labelOpcion3=QLabel("Opción 3: "+self.pregunta.readline())
                        self.labelOpcion3.setStyleSheet(""" font-size: 15px;color: #b1b1b1;""")
                        self.labelOpcion4=QLabel("Opción 4: "+self.pregunta.readline())
                        self.labelOpcion4.setStyleSheet(""" font-size: 15px;color: #b1b1b1;""")
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
                        self.botonRetirarse.setStyleSheet(self.estiloBotones)
                        self.botonRetirarse.setFixedSize(200, 50)
                        self.botonRetirarse.clicked.connect(self.retirarse)
                        self.hboxBotones.addWidget(self.botonRetirarse)
                        self.botonGuardarRespuesta=QPushButton("Enviar")
                        self.botonGuardarRespuesta.setStyleSheet(self.estiloBotones)
                        self.botonGuardarRespuesta.setFixedSize(200, 50)
                        self.botonGuardarRespuesta.clicked.connect(self.enviar)
                        self.hboxBotones.addWidget(self.botonGuardarRespuesta)
                        self.botonSiguiente=QPushButton("Siguiente")
                        self.botonSiguiente.setStyleSheet(self.estiloBotones)
                        self.botonSiguiente.setFixedSize(200, 50)
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
        self.ronda=1
        self.incremento=10
        if(self.puntajePartida>self.puntaje):
            self.puntaje=self.puntajePartida
            self.puntajePartida=0
            documentoJugador=open("Jugadores/"+self.nombreJugador+"/"+self.nombreJugador+".csv","w")
            documentoJugador.write("Nombre,Puntaje\n")
            documentoJugador.write(self.nombreJugador+","+str(self.puntaje))
            documentoJugador.close()
        self.puntajePartida=0
        mensaje=QMessageBox(QMessageBox.Warning, "TE HAS RETIRADO", "Al retirarte tu acumulado no se pierde, vuelve a jugar para aumentarlo", buttons = QMessageBox.Ok, parent=self)
        mensaje.exec_()
        self.hboxInfoJugador.itemAt(0).widget().deleteLater()
        self.hboxInfoJugador.itemAt(1).widget().deleteLater()
        self.vboxJuego.itemAt(1).widget().deleteLater()
        self.vboxJuego.itemAt(2).widget().deleteLater()
        
        self.hboxPreguntasYRespuestas.itemAt(0).widget().deleteLater()
        self.hboxPreguntasYRespuestas.itemAt(1).widget().deleteLater()
        self.hboxBotones.itemAt(0).widget().deleteLater()
        self.hboxBotones.itemAt(1).widget().deleteLater()
        self.hboxBotones.itemAt(2).widget().deleteLater()
        self.banderaInicio=True
    
    def seguir(self):
        if(self.ronda!=1 and self.ronda<=5 and self.banderaSiguiente==True):
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
            self.labelRonda.setText("RONDA: "+str(self.ronda))
            self.banderaSiguiente=False
            
    def enviar(self):
        
        if(self.ronda==1):
           
            self.pregunta=open("Categorias/"+"Categoria"+str(self.ronda)+"/"+str(self.preguntaRandom)+".csv","r")
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            self.respuesta=int(self.pregunta.readline())
            
            self.pregunta.close()
            
            if(self.respuesta==self.opc):
                self.puntajePartida+=self.incremento
                self.labelPuntajePartida.setText("PUNTAJE PARTIDA: "+str(self.puntajePartida))
                self.incremento+=10
                self.ronda+=1
                
                mensaje=QMessageBox(QMessageBox.Information, "GANASTE", "Excelente respuesta, puedes elegir retirarte con tu acumulado o dar en siguiente y seguir jugando", buttons = QMessageBox.Ok, parent=self)
                mensaje.exec_()
            else:
                print("error")
                mensaje=QMessageBox(QMessageBox.Critical, "PERDISTE", "Respuesta equivocada, has perdido tu acumulado, sigue intentando", buttons = QMessageBox.Ok, parent=self)
                mensaje.exec_()
                self.banderaInicio=True
                self.ronda=1
                self.puntajePartida=0
                self.incremento=10
                
                
                self.hboxInfoJugador.itemAt(0).widget().deleteLater()
                self.hboxInfoJugador.itemAt(1).widget().deleteLater()
                self.vboxJuego.itemAt(1).widget().deleteLater()
                self.vboxJuego.itemAt(2).widget().deleteLater()
                
                self.hboxPreguntasYRespuestas.itemAt(0).widget().deleteLater()
                self.hboxPreguntasYRespuestas.itemAt(1).widget().deleteLater()
                self.hboxBotones.itemAt(0).widget().deleteLater()
                self.hboxBotones.itemAt(1).widget().deleteLater()
                self.hboxBotones.itemAt(2).widget().deleteLater()
            self.banderaSiguiente=True
                
        
        elif(self.ronda<=5 and self.ronda!=1):
            
            self.pregunta=open("Categorias/"+"Categoria"+str(self.ronda)+"/"+str(self.preguntaRandom)+".csv","r")
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            print(self.pregunta.readline())
            self.respuesta=int(self.pregunta.readline())
           
            self.pregunta.close()
            if(self.respuesta==self.opc):
                self.puntajePartida+=self.incremento
                self.labelPuntajePartida.setText("PUNTAJE PARTIDA: "+str(self.puntajePartida))
                self.incremento+=10
                
                 
                if (self.ronda!=5):
                    mensaje=QMessageBox(QMessageBox.Information, "GANASTE", "Excelente respuesta, puedes elegir retirarte con tu acumulado o dar en siguiente y seguir jugando", buttons = QMessageBox.Ok, parent=self)
                    mensaje.exec_()
                    
                if(self.ronda==5):
                    self.ronda=0
                    self.incremento=10
                    self.puntaje=self.puntajePartida
                    
                    self.puntajePartida=0
                    documentoJugador=open("Jugadores/"+self.nombreJugador+"/"+self.nombreJugador+".csv","w")
                    documentoJugador.write("Nombre,Puntaje\n")
                    documentoJugador.write(self.nombreJugador+","+str(self.puntaje))
                    documentoJugador.close()
                    
                    mensaje=QMessageBox(QMessageBox.Warning, "GANASTE", "Has ganado el juego!!", buttons = QMessageBox.Ok, parent=self)
                    mensaje.exec_()
                    self.hboxInfoJugador.itemAt(0).widget().deleteLater()
                    self.hboxInfoJugador.itemAt(1).widget().deleteLater()
                    self.vboxJuego.itemAt(1).widget().deleteLater()
                    self.vboxJuego.itemAt(2).widget().deleteLater()
                    
                    self.hboxPreguntasYRespuestas.itemAt(0).widget().deleteLater()
                    self.hboxPreguntasYRespuestas.itemAt(1).widget().deleteLater()
                    self.hboxBotones.itemAt(0).widget().deleteLater()
                    self.hboxBotones.itemAt(1).widget().deleteLater()
                    self.hboxBotones.itemAt(2).widget().deleteLater()
                self.ronda+=1
                
            else:
                
                mensaje=QMessageBox(QMessageBox.Critical, "PERDISTE", "Respuesta equivocada, has perdido tu acumulado, sigue intentando", buttons = QMessageBox.Ok, parent=self)
                mensaje.exec_()
                
                self.ronda=1
                self.puntajePartida=0
                self.incremento=10
                
                
                self.hboxInfoJugador.itemAt(0).widget().deleteLater()
                self.hboxInfoJugador.itemAt(1).widget().deleteLater()
                self.vboxJuego.itemAt(1).widget().deleteLater()
                self.vboxJuego.itemAt(2).widget().deleteLater()
                
                self.hboxPreguntasYRespuestas.itemAt(0).widget().deleteLater()
                self.hboxPreguntasYRespuestas.itemAt(1).widget().deleteLater()
                self.hboxBotones.itemAt(0).widget().deleteLater()
                self.hboxBotones.itemAt(1).widget().deleteLater()
                self.hboxBotones.itemAt(2).widget().deleteLater()

            self.banderaSiguiente=True
           

class IngresarJugador(QWidget):
    sJugador=pyqtSignal(str,int)
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,400,200)
        self.setStyleSheet(""" color: #b1b1b1;background-color: #323232;""" )
        self.puntaje=0
        self.nombre=""
        self.estiloBotones="""color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);border-width: 1px;
        border-color: #1e1e1e;
        border-style: solid;
        border-radius: 6;
        padding: 3px;
        font-size: 15px;
        padding-left: 5px;
        padding-right: 5px;
        min-width: 40px;"""
        self.estiloLine="""
                        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
                        padding: 1px;
                        border-style: solid;
                        border: 1px solid #1e1e1e;
                        border-radius: 5;
                        border-width:0px;
                        min-width: 40px;
                        """
        self.vboxInfoUsuario=QVBoxLayout()
        
        #FORMULARIO INFO JUGADOR
        self.labelNombre=QLabel("Ingrese el nombre de usuario")
        self.vboxInfoUsuario.addWidget(self.labelNombre)
        self.lineEditNombre=QLineEdit()
        self.lineEditNombre.setStyleSheet(self.estiloLine)
        self.vboxInfoUsuario.addWidget(self.lineEditNombre)
        self.botonGuardarInfoUsuario=QPushButton("Guardar")
        self.botonGuardarInfoUsuario.setStyleSheet(self.estiloBotones)
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
        self.estiloBotones="""color: #b1b1b1;background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);border-width: 1px;
        border-color: #1e1e1e;
        border-style: solid;
        border-radius: 6;
        padding: 3px;
        font-size: 15px;
        padding-left: 5px;
        padding-right: 5px;
        min-width: 40px;"""
        self.estiloLine="""
                        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
                        padding: 1px;
                        border-style: solid;
                        border: 1px solid #1e1e1e;
                        border-radius: 5;
                        border-width:0px;
                        min-width: 40px;
                        """
        self.setGeometry(100,100,600,600)
        self.setStyleSheet(""" color: #b1b1b1;background-color: #323232;""" )
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
        self.linePregunta.setStyleSheet(self.estiloLine)
        self.formularioPregunta.addRow(QLabel("Pregunta"),self.linePregunta)
        
        self.lineOpcion1=QLineEdit()
        self.lineOpcion1.setStyleSheet(self.estiloLine)
        self.formularioPregunta.addRow(QLabel("Opción 1"),self.lineOpcion1)
        
        self.lineOpcion2=QLineEdit()
        self.lineOpcion2.setStyleSheet(self.estiloLine)
        self.formularioPregunta.addRow(QLabel("Opción 2"),self.lineOpcion2)
        
        self.lineOpcion3=QLineEdit()
        self.lineOpcion3.setStyleSheet(self.estiloLine)
        self.formularioPregunta.addRow(QLabel("Opción 3"),self.lineOpcion3)
        
        self.lineOpcion4=QLineEdit()
        self.lineOpcion4.setStyleSheet(self.estiloLine)
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
        self.botonGuardar.setStyleSheet(self.estiloBotones)
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
            self.opcion1.setChecked(False)
            self.opcion2.setChecked(False)
            self.opcion3.setChecked(False)
            self.opcion3.setChecked(False)
            self.categoria1.setChecked(False)
            self.categoria2.setChecked(False)
            self.categoria3.setChecked(False)
            self.categoria4.setChecked(False)
            self.linePregunta.setText("")
            self.lineOpcion1.setText("")
            self.lineOpcion2.setText("")
            self.lineOpcion3.setText("")
            self.lineOpcion4.setText("")
            
        else:
            mensaje=QMessageBox(QMessageBox.Warning, "Preguntas", "Ingrese todos los campos requeridos", buttons = QMessageBox.Ok, parent=self)
            mensaje.exec_()
            
            
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Interface()
    sys.exit(app.exec_())
        