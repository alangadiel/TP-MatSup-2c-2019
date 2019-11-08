import sys
import re
import math
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QTableWidgetItem, QLineEdit, QMessageBox, QAbstractItemView
import numpy as np
import sympy as sym

modo = ["Lagrange","NG Progresivo", "NG Regresivo"]

mostrarPasos = []


xi = []
yi = []

qtCreatorFile = "interface.ui" # Nombre del archivo aquí

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class FINTER(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.modoSeleccionado = 1
        self.setupUi(self)
        self.agregar.clicked.connect(self.agregar_app)
        self.especializarPunto.clicked.connect(self.especializarPunto_app)
        self.mostrarPasos.clicked.connect(self.mostrarPasos_app)
        self.cambiarModo.clicked.connect(self.cambiarModo_app)
        self.finalizar.clicked.connect(self.finalizar_app)
        self.quitar.clicked.connect(self.quitar_app)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 106)
        self.tableWidget.setColumnWidth(1, 106)
        self.tableWidget.setHorizontalHeaderLabels(("x","F(x)"))
        # Deshabilitar edición
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.modoInterpolacion.setText(modo[self.modoSeleccionado])


    def generarPolinomio(self):
        #no se como generar un switch en python 
        if self.modoSeleccionado == 0: 
            self.interpolacion_lagrange()
        elif self.modoSeleccionado == 1:
            self.interpolacion_NGProg()
        else:
            self.interpolacion_NGReg()
    
    def agregar_app(self):
        x, okPressed1 = QInputDialog.getInt(self, "Agregar punto","Punto x:", 0, 0, 100000, 1)  
        y, okPressed2 = QInputDialog.getInt(self, "Agregar punto","Punto y:", 0, 0, 100000, 1)    
        if okPressed2 and okPressed1:
            try:
                xi.append(float(x))
                yi.append(float(y))
                row = len(xi)
                self.tableWidget.setRowCount(row-1)
                punto = QTableWidgetItem(str(x))
                imagen = QTableWidgetItem(str(y))
                self.tableWidget.insertRow(row-1)
                self.tableWidget.setItem(row-1, 0, punto)
                self.tableWidget.setItem(row-1, 1, imagen)
                self.generarPolinomio()
            except:
                msgBox = QMessageBox.critical(self,"Datos incorrectos","Vuelva a intentarlo")

    def quitar_app(self):
        if len(yi) != 0:
            try:
                xi.pop()
                yi.pop()
                row = len(xi)
                self.tableWidget.removeRow(row)
                self.tableWidget.setRowCount(row)
                if len(xi) != 0:
                    self.generarPolinomio()
                else:
                    self.polinomio.setText("")
            except:    
                msgBox = QMessageBox.critical(self,"Error","Error al eliminar")        
        else:
            QMessageBox.about(self, "Mensaje","La lista esta vacia")

    def mostrarPasos_app(self):
        if len(mostrarPasos) > 0:
            if self.modoSeleccionado == 0:
                self.mostrarLagrange()
            elif self.modoSeleccionado == 1: 
                self.mostrarNGP()
            else: 
                self.mostrarNGR()
        else:
            QMessageBox.about(self, "Mensaje","No hay ningun polinomio todavia")

    def mostrarLagrange(self):
        string = "grado polinomio: " + str(self.obtenerGradoPolinomio(self.polinomio.text())) + "\n"
        string += "Es equiespaciado: " + self.puntosEquidistantes() + "\n"
        for i in range(len(mostrarPasos)):        
            string += "L" + str(i) + ": " + str(mostrarPasos[i]) + "\n"
        QMessageBox.about(self, "Mostrar Pasos", string)
    
    def mostrarNGR(self):
        string = "grado polinomio: " + str(self.obtenerGradoPolinomio(self.polinomio.text())) + "\n"
        string += "Es equiespaciado: " + self.puntosEquidistantes() + "\n\n"
        for i in range(len(mostrarPasos[0])):        
            string += "b" + str(i) + ": " + str(mostrarPasos[0][i]) + "\n"
        QMessageBox.about(self, "mostrarPasos", string)
    
    def mostrarNGP(self):
        string = "grado polinomio: " + str(self.obtenerGradoPolinomio(self.polinomio.text())) + "\n"
        string += "Es equiespaciado: " + self.puntosEquidistantes() + "\n\n"
        print(mostrarPasos[0])
        for i in range(len(mostrarPasos[0])):       
            string += "a" + str(i) + ": " + str(mostrarPasos[0][i]) + "\n"
        QMessageBox.about(self, "mostrarPasos", string)
    

    def especializarPunto_app(self):
        if  len(mostrarPasos) > 0:
            punto, okPressed = QInputDialog.getText(self, "Especializar en un punto","Punto:", QLineEdit.Normal, "")
            if okPressed and punto:
                funcion = self.polinomio.text()
                funcion = sym.lambdify('x',funcion)
                QMessageBox.about(self, "Punto de especializacion", "El punto es " + str(funcion(int(punto))))
        else: 
            QMessageBox.about(self, "Mensaje","No hay ningun polinomio todavia")


    def cambiarModo_app(self):
        index = self.modoSeleccionado
        item, okPressed = QInputDialog.getItem(self, "Cambiar de modo","Modo:", modo, index, False)
        if okPressed:
            self.modoSeleccionado = modo.index(item)
            self.modoInterpolacion.setText(modo[self.modoSeleccionado])
            self.generarPolinomio()

    def finalizar_app(self):
        sys.exit(app.exec_())

    def interpolacion_lagrange(self):
        n = len(xi)
        x = sym.Symbol('x')
        mostrarPasos.clear()
        # Polinomio
        polinomio = 0
        for i in range(0,n,1):
            # Termino de Lagrange
            termino = 1
            for j  in range(0,n,1):
                if (j!=i):
                    termino = termino*(x-xi[j])/(xi[i]-xi[j])
            polinomio = polinomio + termino*yi[i]
            if len(xi) == 1:
                mostrarPasos.append(termino)
            else:
                mostrarPasos.append(termino.expand()) 
        #Si es un solo elemento el expand me llora por eso el if
        # Simplifica el polinomio obtenido
        if len(xi) > 1:
            polinomio = polinomio.expand() 
        self.polinomio.setText(str(polinomio))
        print(polinomio)
        # para evaluacion numérica
        especializacionEnPunto = sym.lambdify(x,polinomio)
    
        
    def interpolacion_NGReg(self):
        n = len(xi)
        x = sym.Symbol('x')
        a = []
        termino = yi
        mostrarPasos.clear()
        #Inicialzo a con los valores de la imagen(yi)
        for i in range(n):
            a.append(yi[i])

        #Va generando las distintas columnas de orden n en el vector a (Voy sobrescribiendo)
        #En aux voy agregando los valores que voy a necesitar 

        aux =[]
        aux.append(a[n-1])
        for j in range(1, n):
            #Hago las diferencia finita entre yi y yi+1
            for i in range(n-1, j-1, -1):
                a[i] = float(a[i]-a[i-1])/float(xi[i]-xi[i-j])
            aux.append(a[n-1])
            print(aux)

        #generar el polinomio
        mostrarPasos.append(aux)
        
        #Genero el polinomio 
        polinomio = aux[0]
        termino = 1

        #Recorre el vector de bn y los multiplica por sus (x - xn) pertenecientes
        for h in range (1, len(aux), 1):
            #Genero el termino y despues lo sumo
            for k in range(0, h, 1):
                termino *= (x-xi[n-k-1])
            termino *= aux[h]
            polinomio += termino
            #Lo inicializo para la proxima pasada 
            termino = 1
        #por el expand si es un solo elemento

        if len(xi) > 1:
            polinomio = polinomio.expand() 
        # Escribo el polinomio y pongo la funcion para la especializacion de un punto     
        self.polinomio.setText(str(polinomio))
        especializacionEnPunto = sym.lambdify(x,polinomio)

    def interpolacion_NGProg(self):
        n = len(xi)
        x = sym.Symbol('x')
        a = []
        termino = yi
        mostrarPasos.clear()

        #Inicializo a con los valores de la imagen(yi)
        for i in range(n):
            a.append(yi[i])

        aux = []
        
        #Genero las columnas de orden n con las diferencias finitas en el vector a (Voy sobrescribiendo)
        #En aux guardo los valores que voy a necesitar
        for j in range(1, n):
            #Lo uso para sacar los an en un vector aparte
            aux.append(a[0])
            #Aca hago las diferencias finitas 
            for i in range(0, n-j, 1):
                a[i] = float(a[i+1]-a[i])/float(xi[i+j]-xi[i])
        aux.append(a[0])
        mostrarPasos.append(aux)
        
        #Genero el polinomio 
        polinomio = aux[0]
        termino = 1
        #Recorro el vector a tantas veces como elementos tenga
        for h in range (1, len(aux), 1):
            #Dependiendo de cual es la posicion de el elemento
            #Lo multiplico por (x-xn)
            for k in range(0, h, 1):
                termino *= (x-xi[k])
            termino *= aux[h]
            #Le sumo el termino al polinomio
            #print(polinomio)
            polinomio += termino
            #Lo inicializo para la proxima vuelta
            termino = 1

        #Le paso los valores a mostrarPasos para poder mostrarlos 
        #y doy vuelta la lista poque esta al reves
        if len(xi) > 1:
            polinomio = polinomio.expand() 
        #Seteo la info en el el cuadro de texto del polinomio y pongo la funcion para especializar el punto
        self.polinomio.setText(str(polinomio))
        especializacionEnPunto = sym.lambdify(x,polinomio)

    def obtenerGradoPolinomio(self , polinomio):
        pos = polinomio.find("**")
        resultado = "0"
        if pos == -1:
            pos = polinomio.find("x")
            if pos != -1:
                resultado = "1"
        else:
            resultado = polinomio[pos+2:pos+3]
        return resultado

    def puntosEquidistantes(self):
        resultado = True
        if len(xi) > 2:
            # -3 porque tomo el elemento i y dos mas sino me rompe el array
            for i in range(0, len(xi)-2, 1):
                difx1 = xi[i] - xi[i+1]
                difx2 = xi[i+1] - xi[i+2]
                dify1 = yi[i] - yi[i+1]
                dify2 = yi[i+1] - yi[i+2]
                if difx1 != difx2 or dify1 != dify2:
                    resultado = False
        return str(resultado)
                
            
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = FINTER()
    window.show()
    sys.exit(app.exec_())
