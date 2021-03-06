"""Documentación del módulo.
Esta aplicacion es un desarrollo de escritorio para simular a partir de la data entregada
paramentros criticos en los superconductores """

__author__ = "Cristian Leonardo Cárdenas Garcia"
__copyright__ = "Copyright 2020"
__credits__ = ["Grupo de Investigación Telematics", "Cristian Leonardo Cárdenas", "Indry","Miguel Angel Mendoza"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Telematics"
__email__ = "leonardcad02@gmail.com"
__status__ = "Producion"

import sys 
#from PyQt5 import uic,QtWidgets,QtGui
from ventana_principal import *

from Aplicacion import *



class MainWindow(QtWidgets.QMainWindow,Ui_mainWindow):
    def __init__(self,*args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.title = 'DETERMINATION OF CRITICAL PARAMETERS FROM STUDY OF MAGNETICS FLUCTUATIONS IN HTCS'
        self.iconName = "../img/Telematica.png"
        self.title = 'DETERMINATION OF CRITICAL PARAMETERS FROM STUDY OF MAGNETICS FLUCTUATIONS IN HTCS'
        self.iconName = "../Img/Telematica.png"
        self.setWindowTitle(self.title)
        self.setMinimumSize(713,469)
        self.setMaximumSize(713,469)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.DataEntry.clicked.connect(self.abrir)
        self.Description.clicked.connect(self.description)

    def abrir(self):
        self.ui = App()

    def description(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
