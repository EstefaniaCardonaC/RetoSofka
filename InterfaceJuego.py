# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:52:02 2022

@author: estef
"""

import os
import time
import sys
from PyQt5.QtWidgets import QWidget,QDialog,QGroupBox,QSizePolicy,QFormLayout,QMessageBox,QCheckBox,QLabel,QDateEdit,QLineEdit,QComboBox,QApplication,QHBoxLayout,QVBoxLayout,QPushButton
from PyQt5.QtCore import pyqtSignal,QThread,QDateTime,Qt,QSize,QDate
from PyQt5.QtGui import QFont,QIcon,QPixmap,QImage,QColor,QPainter,QPen,QBrush
from Jugador import Jugador

class Interface(QWidget):
    def __init__(self):
        super().__init__()
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
        pass
    
    def jugador(self):
        self.ventanaInfoJugador=IngresarJugador()
        self.ventanaInfoJugador.show()
    def configuracion(self):
        pass

class IngresarJugador(QWidget):
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
        if(os.path.exists("Jugadores/"+self.nombre)==False):
            self.jugador=Jugador(self.nombre,self.puntaje)
        
        if(os.path.exists("Jugadores/"+self.nombre)==True):
            self.docJugador=open("Jugadores/"+self.nombre+"/"+self.nombre+".csv","r")
            self.docJugador.readline()
            self.infoJugador=self.docJugador.readline().split(",")
            self.nombreJugadorExistente=QLabel(self.infoJugador[0])
            self.puntajeJugadorExistente=QLabel(self.infoJugador[1])
            
            self.vboxInfoUsuario.addWidget(QLabel("Usuario existente"))
            self.vboxInfoUsuario.addWidget(self.nombreJugadorExistente)
            self.vboxInfoUsuario.addWidget(QLabel("Puntaje Máximo Obtenido"))
            self.vboxInfoUsuario.addWidget(self.puntajeJugadorExistente)
        
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Interface()
    sys.exit(app.exec_())
        