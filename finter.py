import sys
import re
import math
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QMessageBox

qtCreatorFile = "interface.ui" # Nombre del archivo aquí

puntos = []

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


    def agregar_app(self):
        punto = QInputDialog.getInt(self, "Agregar punto","Numero:", 0, 0, 100000, 1)    
        if punto[1]:
            puntos.append(punto[0])
            print(puntos)

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
