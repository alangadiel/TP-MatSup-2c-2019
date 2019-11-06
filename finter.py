import sys
import re
import math
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QTableWidgetItem, QLineEdit, QMessageBox, QAbstractItemView
modo = ["Lagrange","NG Progresivo", "NG Regresivo"]

modoSeleccionado = 0

xi = []
yi = []

qtCreatorFile = "interface.ui" # Nombre del archivo aquí

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class FINTER(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
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
        self.modoInterpolacion.setText(modo[modoSeleccionado])

    def agregar_app(self):
        x = QInputDialog.getInt(self, "Agregar punto","Punto x:", 0, 0, 100000, 1)  
        y = QInputDialog.getInt(self, "Agregar punto","Punto y:", 0, 0, 100000, 1)    
        if x and y:
            xi.append(x[0])
            yi.append(y[0])
            row = len(xi)
            self.tableWidget.setRowCount(row-1)
            punto = QTableWidgetItem(str(x[0]))
            imagen = QTableWidgetItem(str(y[0]))
            self.tableWidget.insertRow(row-1)
            self.tableWidget.setItem(row-1, 0, punto)
            self.tableWidget.setItem(row-1, 1, imagen)
            print(xi)
            print(yi)

    def quitar_app(self):
        if len(yi) != 0:
            xi.pop()
            yi.pop()
            row = len(xi)
            self.tableWidget.removeRow(row)
            self.tableWidget.setRowCount(row)
        else:
            QMessageBox.about(self, "Mensaje","La lista esta vacia")

    def mostrarPasos_app(self):
        QMessageBox.about(self, "Punto de especializacion", "El punto es")

    def especializarPunto_app(self):
        punto, okPressed = QInputDialog.getText(self, "Especializar en un punto","Punto:", QLineEdit.Normal, "")
        QMessageBox.about(self, "Punto de especializacion", "El punto es " + punto)

    def cambiarModo_app(self):
        item, okPressed = QInputDialog.getItem(self, "Cambiar de modo","Modo:", modo, 0, False)
        modoSeleccionado = modo.index(item)
        self.modoInterpolacion.setText(modo[modoSeleccionado])

    def finalizar_app(self):
        sys.exit(app.exec_())

    #def interpolacion_lagrange(self):
        
    #def interpolacion_NGProg(self):
    
    #def interpolacion_NGReg(self):
    

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = FINTER()
    window.show()
    sys.exit(app.exec_())
