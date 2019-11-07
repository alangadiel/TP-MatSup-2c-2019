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
        if okPressed2 and okPressed1 and x and y:
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
                self.generarPolinomio()
            except:    
                msgBox = QMessageBox.critical(self,"Datos incorrectos","Vuelva a intentarlo")        
        else:
            QMessageBox.about(self, "Mensaje","La lista esta vacia")

    def mostrarPasos_app(self):
        if len(mostrarPasos) > 0:
            if self.modoSeleccionado == 0:
                self.mostrarLagrange()
            else: 
                self.mostrarNGP()
        else:
            QMessageBox.about(self, "Mensaje","No hay ningun polinomio todavia")

    def mostrarLagrange(self):
        string = ""
        for i in range(len(mostrarPasos)):        
            string += "L" + str(i) + ": " + str(mostrarPasos[i]) + "\n"
        QMessageBox.about(self, "Mostrar Pasos", string)
    
    def mostrarNGP(self):
        string = ""
        print(mostrarPasos)
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
            mostrarPasos.append(termino)

        #Si es un solo elemento el expand me llora por eso el if
        # Simplifica el polinomio obtenido
        if len(xi) > 1:
            polinomio = polinomio.expand() 
        self.polinomio.setText(str(polinomio))
        # para evaluacion numérica
        especializacionEnPunto = sym.lambdify(x,polinomio)
    
        
    def interpolacion_NGReg(self):
        n = len(xi)
        x = sym.Symbol('x')
        a = []
        termino = yi
        #Inicialzo a con los valores de la imagen(yi)
        for i in range(n):
            a.append(yi[i])

        #Recorre los puntos yi generando las diferencias finitas de orden 1
        #Una vez generadas las diferencias finitas las pongo en el vector a 
        #de adelante hacia atras dejando el valor el valor de a que necesito para
        #generar el polinomio 
        #La ultima posicicon del vector a eliminando el valor de yi que no necesito mas
        for j in range(1, n):
            #Hago las diferencia finita entre yi y yi+1
            for i in range(n-1, j-1, -1):
                a[i] = float(a[i]-a[i-1])/float(xi[i]-xi[i-j])
        #Pongo en la primera posicion de el vector a el valor de yi que me importa para
        #generar el polinomio 
        a[0] = yi[n-1]
        mostrarPasos.append(a)

        #Genero el polinomio 
        polinomio = a[0]
        termino = 1

        #Recorre el vector de bn y los multiplica por sus (x - xn) pertenecientes
        for h in range (1, len(a), 1):
            #Genero el termino y despues lo sumo
            for k in range(0, h, 1):
                termino *= (x-xi[n-k-1])
            termino *= a[h]
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
        #Inicializo a con los valores de la imagen(yi)
        for i in range(n):
            a.append(yi[i])

        #Recorro los valores de la imagen para generar las diferencias finitas de orden 1
        #Y los agrego las diferencias finitas en el vector a eliminando los valores de la imagen 
        #Que ya no me sirven, de adelante hacia atras. Y vuelvo a iterar haciendo lo mismo (cantidad de puntos -1 ) veces
        for j in range(1, n):
            #Aca hago las diferencias finitas 
            for i in range(0, n-j, 1):
                a[i] = float(a[i+1]-a[i])/float(xi[i+j]-xi[i])
        #Le agrego el unico valor de la imagen que me interesa en la ultima posicion del vector
        a[n-1] = yi[0]
        print(a)
        mostrarPasos.append(a)

        #Genero el polinomio 
        polinomio = a[n-1]
        termino = 1
        #Recorro el vector a tantas veces como elementos tenga
        for h in range (1, len(a), 1):
            #Dependiendo de cual es la posicion de el elemento
            #Lo multiplico por (x-xn)
            for k in range(0, h, 1):
                termino *= (x-xi[k])
            termino *= a[n-h-1]
            print(termino)
            #Le sumo el termino al polinomio
            polinomio += termino
            #Lo inicializo para la proxima vuelta
            termino = 1
        if len(xi) > 1:
            polinomio = polinomio.expand() 
        #Seteo la info en el el cuadro de texto del polinomio y pongo la funcion para especializar el punto
        self.polinomio.setText(str(polinomio.expand()))
        especializacionEnPunto = sym.lambdify(x,polinomio)

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = FINTER()
    window.show()
    sys.exit(app.exec_())
