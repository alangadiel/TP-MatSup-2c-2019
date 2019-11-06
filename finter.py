import sys
import re
import math
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QTableWidgetItem, QLineEdit, QMessageBox, QAbstractItemView

modo = ["Lagrange","NG Progresivo", "NG Regresivo"]

modoSeleccionado = 0
puntos = []

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
        punto = QInputDialog.getInt(self, "Agregar punto","Numero:", 0, 0, 100000, 1)    
        if punto[1]:
            puntos.append(punto[0])
            row = len(puntos)
            self.tableWidget.setRowCount(row-1)
            x = QTableWidgetItem(str(row))
            y = QTableWidgetItem(str(punto[0]))
            self.tableWidget.insertRow(row-1)
            self.tableWidget.setItem(row-1, 0, x)
            self.tableWidget.setItem(row-1, 1, y)
            print(puntos)

    def quitar_app(self):
        if len(puntos) != 0:
            puntos.pop()
            row = len(puntos)
            self.tableWidget.removeRow(row)
            self.tableWidget.setRowCount(row)
        else:
            QMessageBox.about(self, "Mensaje","La lista esta vacia")

    def mostrarPasos_app(self):
        QMessageBox.about(self, "Punto de especializacion", "El punto es")

    def especializarPunto_app(self):
        punto = QInputDialog.getInt(self, "Agregar punto","Numero:", 0, 0, 100000, 1)    
        QMessageBox.about(self, "Punto de especializacion", "El punto es")

    def cambiarModo_app(self):
        QMessageBox.about(self, "Punto de especializacion", "El punto es")

    def finalizar_app(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = FINTER()
    window.show()
    sys.exit(app.exec_())
