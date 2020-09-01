import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore, QtPrintSupport,QtSql


#from visualizar import *
import pymysql

import matplotlib
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

from Reportes import *
 

import pandas as pd
import numpy as np
import math

from datetime import datetime

font = {'family': 'arial',
        'size': 7}
matplotlib.rc('font', **font)

qtCreatorFile = '../QtDesigner/EncimaTco.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    Reportes = None
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent) 
        self.setupUi(self)       
        self.enviar = Ventana_reportes(self)
        self.reportes.clicked.connect(self.enviar.show)
        self.title = 'DETERMINATION OF CRITICAL PARAMETERS FROM STUDY OF MAGNETICS FLUCTUATIONS IN HTCS'
        self.iconName = "../Img/Telematica.png" 
             

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.graphicsView)
        self.canvas.setGeometry(0, 0, self.graphicsView.width(), self.graphicsView.height())

        self._position_x = None
        self._position_y = None
        self.grafica = []
        self.move_cursor = None
        
        self.point_x = []
        self.point_y = []  
        self._size_x = []
        self._size_y = []     
        self.delta_t = []
        self.temperatura_reducida = []       
        self.delta_t_cuadrado = None
        self.s =None
        self.pendiente = 0
        self.Tc = 0
        self.Tirr = 0
        self.Tco = 0
        self.Asl = 0
        self.Bld = 0
        self.longitud_coerencia_ab = 0
        self.longitud_coerencia_c = 0
        self.gamma = 0
        self.dimensionalidad = 0
        self.now = datetime.now()

        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(1116, 672)
        self.setMaximumSize(1116, 672)
        self.setWindowIcon(QtGui.QIcon(self.iconName))

        # crear el menu

        exitAct = QtWidgets.QAction(QtGui.QIcon('../Img/exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+q')
        exitAct.triggered.connect(QtWidgets.qApp.quit)

        openFile = QtWidgets.QAction(QtGui.QIcon('../Img/openFile.png'), 'Open', self)

        openFile = QtWidgets.QAction(QtGui.QIcon('../Img/openFile.png'), 'Open', self)
        openFile.setShortcut('Ctrl+o')
        openFile.triggered.connect(self._openData)

        Help = QtWidgets.QAction(QtGui.QIcon('../Img/help.png'), 'Help', self)
        Help.triggered.connect(self._help)

        Help = QtWidgets.QAction(QtGui.QIcon('../Img/help.png'), 'Help', self)
        Help.triggered.connect(self._help)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(Help)
        self.show()

        self.Button_Set.setEnabled(False)
        self.calcular.setEnabled(False)
        self.Masa.setEnabled(False)
        self.Tinicial.setEnabled(False)
        self.Tfinal.setEnabled(False)
        self.Minicial.setEnabled(False)
        self.Mfinal.setEnabled(False)
        self.Datoinicialzfc.setEnabled(False)
        self.Datofinalzfc.setEnabled(False)
        self.Datoinicialfc.setEnabled(False)
        self.Datofinalfc.setEnabled(False)       
        self.Distanciainterplanar.setEnabled(False)
        self.size_x_min.setEnabled(False)
        self.size_x_max.setEnabled(False)
        self.size_y_min.setEnabled(False)
        self.size_y_max.setEnabled(False)
        self.aboveTco_2.setEnabled(False)
        self.belowTco_2.setEnabled(False)
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        

        self.aboveTco_2.addItem("\u03BE")
        self.aboveTco_2.addItem("\u03C7")

        self.calcular.clicked.connect(self._getItem)
        self.btnenviar.clicked.connect(self._send)
        self.dataBase.clicked.connect(self._reportdatabase)
        self.Button_Set.clicked.connect(self._arena_size)
        self.Button_Zoom.clicked.connect(self._zoom)
     
    def _getItem(self):
        item = self.aboveTco_2.currentText().strip()
        if item == "ZFC":
            self._zfc()
        elif item == "Tc":
            self._tc()
        elif item == "Tirr":
            self._tirreversible()
        elif item == "Tco":
            self._tco()
        elif item == "\u03BE":
            self._longitud_coherencia()
        elif item == "\u03C7":
            self._dimensionalidad()

    def _openData(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'xlsx(*.xlsx)')
        if filePath == "":
            QtWidgets.QMessageBox.question(self, 'Message', "Must Upload a File" + "", QtWidgets.QMessageBox.Ok,
                                           QtWidgets.QMessageBox.Ok)

        elif filePath != "":
            self.datos = pd.ExcelFile(str(filePath))            
            self.field.addItems(list(self.datos.sheet_names))
            self.df = self.datos.parse(self.field.currentText())
            self.dataset = pd.DataFrame(self.datos.parse())
            self.column.addItems(list(self.df.columns.values))
            self.Masa.setEnabled(True)
            self.Tinicial.setEnabled(True)
            self.Tfinal.setEnabled(True)
            self.Minicial.setEnabled(True)
            self.Mfinal.setEnabled(True)
            self.Datoinicialzfc.setEnabled(True)
            self.Datofinalzfc.setEnabled(True)
            self.Datoinicialfc.setEnabled(True)
            self.Datofinalfc.setEnabled(True)
            self.Distanciainterplanar.setEnabled(True)
            self.size_x_min.setEnabled(True)
            self.size_x_max.setEnabled(True)
            self.size_y_min.setEnabled(True)
            self.size_y_max.setEnabled(True)
            self.calcular.setEnabled(True)
            self.Button_Set.setEnabled(True)
            self.aboveTco_2.setEnabled(True)
            self.belowTco_2.setEnabled(True)
            self.loaded.setPixmap(QtGui.QPixmap("../Img/puntoverde.png"))

            self.TableDataset.setColumnCount(len(self.dataset.columns))
            self.TableDataset.setRowCount(len(self.dataset.index))
            for i in range(len(self.dataset.index)):
                for j in range(len(self.dataset.columns)):
                    self.TableDataset.setItem(i,j,QtWidgets.QTableWidgetItem(str(self.dataset.iloc[i,j])))

    def _help(self):
        self.ventana = Ventana_help()
        self.ventana.exec_()

    def _zfc(self):
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self._size_x.clear()
        self._size_y.clear()
          
        self.df = self.datos.parse(self.field.currentText())
        if (self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'Message', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif self.Masa.text() == "":
            QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of the mass." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:            
            self.dato_inicial = self.Datoinicialzfc.text()
            self.dato_final = self.Datofinalzfc.text()
            masa = self.Masa.text()
            try:
                masa = float(masa)
                if ((self.dato_inicial.isnumeric() == True)  and (self.dato_final.isnumeric() == True)):                            
                    self.dato_inicial = int (self.dato_inicial)
                    self.dato_final = int(self.dato_final)       
                    Momentum = self.df['Moment (emu)']
                    Magnetizacion = Momentum / masa
                    self.df["Magnetizacion"] = Magnetizacion
                    data = self.df[self.dato_inicial:self.dato_final][["Temperature (K)", "Magnetizacion"]]
                    self._position_x = data['Temperature (K)']
                    self._position_y = data["Magnetizacion"]
                    self.grafica = []
                    self.grafica.append('')
                    self.grafica.append('T (K)')
                    self.grafica.append('M (emu/g)')
                    self._plot(self._position_x, self._position_y, self.grafica)
                    
            
                else:
                    QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)                
                return True
            except ValueError:
                QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of mass  numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return False
            
    def _arena_size(self):        

        if (len(self.size_x_min.text()) > 0 and len(self.size_x_max.text()) > 0 and len(self.size_y_min.text()) > 0 and
                len(self.size_y_max.text()) > 0):
            self._size_x = [float(self.size_x_min.text()), float(self.size_x_max.text())]
            self._size_y = [float(self.size_y_min.text()), float(self.size_y_max.text())]
            cursor = True if (self.aboveTco_2.currentText().strip() == "Tirr" or
                              self.aboveTco_2.currentText().strip() == "Tco" or
                              self.aboveTco_2.currentText().strip() == "\u03BE") else False
            self._plot(self._position_x, self._position_y, self.grafica, x_lim=self._size_x, y_lim=self._size_y,
                       cursor=cursor, data_aux_x=self.point_x, data_aux_y=self.point_y)
        else:
            print('Enter the axis limit')

    def _tc(self):
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        self._size_x.clear()
        self._size_y.clear()
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        print (self._size_x)
        print (self._size_y)
         

        self.df = self.datos.parse(self.field.currentText())

        if (self.Tinicial.text() == "" or self.Tfinal.text() == "" or self.Minicial.text() == "" or self.Mfinal.text() == "" or self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'Mensaje', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif self.Masa.text() == "":
            QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of the mass." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            masa = self.Masa.text()
            t_inicial = self.Tinicial.text()
            t_final = self.Tfinal.text()
            m_inicial = self.Minicial.text()
            m_final = self.Mfinal.text()
            self.dato_inicial = self.Datoinicialzfc.text()
            self.dato_final = self.Datofinalzfc.text()            
            try:
                masa = float(masa)
                t_inicial = int(t_inicial)
                t_final = int(t_final)
                m_inicial = int(m_inicial)
                m_final = int(m_final)
                self.dato_inicial = int(self.dato_inicial)
                self.dato_final = int (self.dato_final)

                Momentum = self.df['Moment (emu)']
                Magnetizacion = Momentum / masa
                self.df["Magnetizacion"] = Magnetizacion
                suceptibilidad = (self.df["Magnetizacion"]) / (self.df["Magnetic Field (Oe)"])
                inv_suceptibilidad = 1 / (suceptibilidad)
                self.df["suceptibilidad"] = inv_suceptibilidad

                datax = self.df[74:264][["Temperature (K)"]]
                datay = self.df[74:264][["Magnetizacion"]]
                datax1 = self.df[0:24][["Temperature (K)"]]
                datay1 = self.df[0:24][["Magnetizacion"]]

                model = LinearRegression()
                model1 = LinearRegression()

                model.fit(datax, datay)
                model1.fit(datax1, datay1)

                x_p = [[t_inicial], [t_final]]
                y_p = model.predict(x_p)

                x_p1 = [[m_inicial], [m_final]]
                y_p1 = model1.predict(x_p1)

                Intercepto = model.intercept_[0]
                Pendiente = model.coef_[0][0]
                

                Intercepto_1 = model1.intercept_[0]
                Pendiente_1 = model1.coef_[0][0]

                self.Tc = (Intercepto_1 - Intercepto) / (Pendiente - Pendiente_1)
                #y = (Pendiente_1 * self.Tc) + Intercepto_1

            
                self._position_x = []
                self._position_y = []

                tam = self.df[self.dato_inicial:self.dato_final]['Temperature (K)'].to_numpy().shape[0]
                x_p_aux = np.array([])
                steps = (t_final - t_inicial) / tam
                for index in range(tam):
                    x_p_aux = np.append(x_p_aux, t_inicial + steps * index)
                steps = (y_p[1][0] - y_p[0][0]) / tam
                y_p_aux = []
                for index in range(tam):
                    y_p_aux = np.append(y_p_aux, y_p[0][0] + steps * index)
                steps = (m_final - m_inicial) / tam
                x_p1_aux = []
                for index in range(tam):
                    x_p1_aux = np.append(x_p1_aux, m_inicial + steps * index)
                steps = (y_p1[1][0] - y_p1[0][0]) / tam
                y_p1_aux = []
                for index in range(tam):
                    y_p1_aux = np.append(y_p1_aux, y_p1[0][0] + steps * index)

                self._position_x.append(self.df[self.dato_inicial:self.dato_final]['Temperature (K)'].to_numpy())
                self._position_x.append(np.array(x_p_aux))
                self._position_x.append(np.array(x_p1_aux))

                self._position_y.append(self.df[self.dato_inicial:self.dato_final]['Magnetizacion'].to_numpy())
                self._position_y.append(np.array(y_p_aux))
                self._position_y.append(np.array(y_p1_aux))

                self.grafica = []
                self.grafica.append('')
                self.grafica.append('T (K)')
                self.grafica.append('M (emu/g)')
                self._plot(self._position_x, self._position_y, self.grafica)

                estad_st = "Tc " + str("{0:.3f}".format(self.Tc) + " " + "°K")                      
                self.resultados.setText(str(estad_st))
                return True
            except ValueError:
                QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok) 
                return False
            
    def _tirreversible(self):
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self._size_x.clear()
        self._size_y.clear()
          
        self.clearFocus()
        self.df = self.datos.parse(self.field.currentText())
        if (self.Datoinicialfc.text() == "" or  self.Datofinalfc.text() == "" or self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'ZfC - FC', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif (self.Masa.text() == ""):
            QtWidgets.QMessageBox.question(self, 'Mass', "You must enter the value of the mass or The vector must be equal" + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            masa = self.Masa.text()
            datoInicialFc = (self.Datoinicialfc.text())
            datoFinalFc = (self.Datofinalfc.text())
            dato_inicial = (self.Datoinicialzfc.text())
            dato_final = (self.Datofinalzfc.text())
            print ("Entro") 
            try:
                masa = float(masa)
                if ((datoInicialFc.isnumeric() == True)  and (datoFinalFc.isnumeric() == True) and  (dato_inicial.isnumeric() == True) and (dato_final.isnumeric() == True)):                    
                    print ("Entro_2") 
                    datoInicialFc = int(datoInicialFc)
                    datoFinalFc = int(datoFinalFc)
                    dato_inicial = int(dato_inicial)
                    dato_final = int(dato_final)
                    Momentum = self.df['Moment (emu)']
                    Magnetizacion = Momentum / masa
                    self.df["Magnetizacion"] = Magnetizacion
                    zfc = self.df[dato_inicial:dato_final][["Temperature (K)", "Magnetizacion"]]
                    fc = self.df[datoInicialFc:datoFinalFc][["Temperature (K)", "Magnetizacion"]]
                    print (dato_inicial)
                    print (dato_final)
                    print (datoInicialFc)
                    print (datoFinalFc)
                    self._position_x = []
                    self._position_y = []
                    self._position_x.append(fc['Temperature (K)'])
                    self._position_x.append(zfc['Temperature (K)'])

                    self._position_y.append(fc["Magnetizacion"])
                    self._position_y.append(zfc["Magnetizacion"])

                    self.grafica = []
                    self.grafica.append('')
                    self.grafica.append('T (K)')
                    self.grafica.append('M (emu/g)')
                    self._plot(self._position_x, self._position_y, self.grafica, cursor=True)
                
                else:
                    QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return True    
            except ValueError:
                QtWidgets.QMessageBox.question(self, 'Mass', "You must enter the value of numeric the mass or The vector must be equal" + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return False         

    def _onmove(self, event):
        self.cursor.onmove(event)
        if event.xdata and event.ydata:
            if len(self.point_y)<2:
                self.point_x = np.append(self.point_x, event.xdata)
                self.point_y = np.append(self.point_y, event.ydata)
                if self.aboveTco_2.currentText().strip()=="Tirr":                
                    self.Tirr = self.point_x
                    estad_st = "Tirr " + str("{0:.3f}".format(self.Tirr[0]))+ " " + "°K"                      
                    self.resultados.setText(str(estad_st))
                    self.Tirr = float(self.Tirr[0])
                    
            if len(self.point_y)==2:
                if self.aboveTco_2.currentText().strip()=="Tco":
                    pendiente = (self.point_y[0] - self.point_y[1]) / (self.point_x[0] - self.point_x[1])
                    corte_y = self.point_y[1] - pendiente * self.point_x[1]
                    corte_x = -((corte_y) / pendiente)
                    self.Tco = corte_x
                    estad_st = "Tco " + str("{0:.3f}".format(self.Tco))+ " " + "°K" 
                    self.resultados.setText(str(estad_st))
                    
                    

                elif self.aboveTco_2.currentText().strip()=="\u03C7":                     
                    pendiente = (self.point_y[0] - self.point_y[1]) / (self.point_x[0] - self.point_x[1])
                    corte_y = self.point_y[1] - pendiente * self.point_x[1]
                    corte_x = -((corte_y) / pendiente)
                    self.dimensionalidad = pendiente
                    estad_st = "\u03C7" + str("{0:.3f}".format(self.dimensionalidad))+'\n'
                    self.resultados.setText(str(estad_st))                     

                elif self.aboveTco_2.currentText().strip() == "\u03BE":
                                       
                    aux_x = sorted(self.point_x)
                    pos_x_mayor = np.where(self._position_x > aux_x[0])[1]
                    pos_x_menor = np.where(self._position_x < aux_x[1])[1]
                    self.point_x, self.point_y = [], []
                    aux = np.array(self._position_x)
                    aux_ = np.array(self._position_y)
                    self.point_x = aux[0][pos_x_mayor[0]: pos_x_menor[-1]]
                    self.point_y = aux_[0][pos_x_mayor[0]: pos_x_menor[-1]]

                    try:
                        PI = 2.067833636e-15
                        PERMEABILIDAD_VACIO = 1.256637061e-6
                        CONSTATE_BOLTZMANN = 1.380648e-23 

                        
                        delta_t_sum =self.point_x
                        t_reducida = self.point_y
                        

                        y = pd.DataFrame(delta_t_sum)
                        x = pd.DataFrame(t_reducida)
                        

                        X_train, X_test, y_train,y_test= train_test_split(x, y, test_size=0.25)
                        X_train = X_train.values.reshape([X_train.values.shape[0], 1])
                        X_test = X_test.values.reshape([X_test.values.shape[0], 1])


                        poly_features = PolynomialFeatures(degree=2)
                        X_poly = poly_features.fit_transform(X_train)
                        poly_model = LinearRegression()
                        poly_model.fit(X_poly, y_train)

                        a = poly_model.coef_[0][2]                        
                        b = poly_model.intercept_[0]

                       
                        self.Asl = 1 / (math.sqrt(4 * abs(a)))
                        self.Bld = b * (self.Asl ** 2) 
                        self.Asl = abs (self.Asl)  
                        self.Bld = abs(self.Bld)
                        
                        

                        self.longitud_coerencia_ab = (math.sqrt((3 * self.Asl * PI ** 2 * self.s) / (PERMEABILIDAD_VACIO * CONSTATE_BOLTZMANN * math.pi)))
                        
                        self.longitud_coerencia_c = (math.sqrt(self.s * self.Bld) / 2)
                        
                        self.gamma = self.longitud_coerencia_ab / self.longitud_coerencia_c
                        
                        
                        estad_st =  "Asl" + " " + str("{0:.3E}".format(self.Asl))+'\n' +\
                                    "Bld" + " "  + str("{0:.3E}".format(self.Bld))+'\n' +\
                                    "\u03BE"+"ab " + str("{0:.3E}".format(self.longitud_coerencia_ab))+'\n' +\
                                    "\u03BE"+"c " + str("{0:.3E}".format(self.longitud_coerencia_c)) + '\n' +\
                                    "\u03B3" + " "+ str("{0:.3E}".format(self.gamma))
                        self.resultados.setText(str(estad_st))
                        
                        #return True
                    except ValueError:
                        QtWidgets.QMessageBox.question(self, 'Error', "You must enter the value of numeric  or The vector must be equal" + "",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                        return False
                
                self._plot(self._position_x, self._position_y, self.grafica, cursor=True, data_aux_x=self.point_x,
                           data_aux_y=self.point_y, x_lim=self._size_x, y_lim=self._size_y)
                self.point_x = []
                self.point_y = []

    def _tco(self):
        self.tco1.setEnabled(True)
        self.tco2.setEnabled(True)
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self._size_x.clear()
        self._size_y.clear()
        
        self.df = self.datos.parse(self.field.currentText())
        
        if (self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'ZFC', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif self.Masa.text() == "":
            QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of the mass." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            masa = self.Masa.text()
            dato_inicial = self.Datoinicialzfc.text()
            dato_final = self.Datofinalzfc.text()
            try:
                masa = float(masa)
                if ((dato_inicial.isnumeric() == True) and (dato_final.isnumeric() == True)):
                    dato_inicial = int (dato_inicial)
                    dato_final = int (dato_final)
                    temperatura = self.df['Temperature (K)']
                    Momentum = self.df['Moment (emu)']
                    Magnetizacion = Momentum / masa
                    self.df["Magnetizacion"] = Magnetizacion
                    suceptibilidad = (self.df["Magnetizacion"]) / (self.df["Magnetic Field (Oe)"])
                    inv_suceptibilidad = 1 / (suceptibilidad)
                    self.df["suceptibilidad"] = inv_suceptibilidad

                    data_x = self.df[75:170]['Temperature (K)']
                    data_y = self.df[75:170]['suceptibilidad']

                    data_x = pd.DataFrame(data_x)
                    data_y = pd.DataFrame(data_y)

                    model = LinearRegression()

                    model.fit(data_x, data_y)

                    intercepto = model.intercept_[0]
                    pendiente = model.coef_[0][0]

                    x_normal = pendiente * (temperatura[dato_inicial:dato_final]) + intercepto
                    inv_x_normal = 1 / (x_normal)                    
                    delta_x = suceptibilidad - inv_x_normal
                    self.delta_t = temperatura[dato_inicial:dato_final] / delta_x
                    pos_delta_t = (-1 * (self.delta_t))
                   

                    if self.tco1.isChecked() == True:
                        self._position_x = []
                        self._position_y = []

                       
                        vector = inv_x_normal.shape
                        print (vector) 
                            
                        self._position_x.append(temperatura[dato_inicial:vector[0]])
                        self._position_x.append(temperatura[dato_inicial:vector[0]])

                        self._position_y.append(suceptibilidad[dato_inicial:vector[0]])
                        self._position_y.append(inv_x_normal[dato_inicial:vector[0]])                

                        self.grafica = []
                        self.grafica.append('')
                        self.grafica.append('T (K)')
                        self.grafica.append('M (emu/g)')
                        self._plot(self._position_x, self._position_y, self.grafica)

                    if self.tco2.isChecked() == True:
                        self._position_x = []
                        self._position_y = []

                        self.point_x = []
                        self.point_y = []                   

                        self._position_x.append(temperatura[dato_inicial:dato_final])                

                        self._position_y.append(pos_delta_t[dato_inicial:dato_final])

                        self.grafica = []
                        self.grafica.append('Tirr')
                        self.grafica.append('T (K)')
                        self.grafica.append('M (emu/g)')
                        self._plot(self._position_x,self._position_y, self.grafica, cursor=True)

                else:
                    QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return True        
            except ValueError:
                QtWidgets.QMessageBox.question(self, 'Mass', "You must enter the value of numeric the mass or The vector must be equal" + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return False

    def _longitud_coherencia(self):
        self.point_x, self.point_y = [], []
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self._size_x.clear()
        self._size_y.clear()
                
               
        self.df = self.datos.parse(self.field.currentText())
        if (self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'ZFC', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif (self.Distanciainterplanar.text() == ""):
            QtWidgets.QMessageBox.question(self, 'Interplanar Distance', "You must enter the value of the interplanar distance." +
                                           "", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif (self.Tco):
            dato_inicial = self.Datoinicialzfc.text()
            dato_final = self.Datofinalzfc.text()
            self.s = self.Distanciainterplanar.text()
            try:
                if ((dato_inicial.isnumeric() == True) and (dato_final.isnumeric() == True)):
                    dato_inicial = int (dato_inicial)
                    dato_final = int (dato_final)
                    self.s = float(self.s)
                    temperatura = self.df[dato_inicial:dato_final]['Temperature (K)']
                    self.temperatura_reducida = (temperatura - self.Tco) / self.Tco
                    self.delta_t_cuadrado = (self.delta_t[dato_inicial:dato_final] ** 2)

                    
                    self._position_x = []
                    self._position_y = []

                    
                    self._position_x.append(self.temperatura_reducida[2:260])            
                    self._position_y.append(self.delta_t_cuadrado[2:260])

                    self.grafica = []
                    self.grafica.append('')
                    
                    self.grafica.append('(T-Tco)/Tco')
                    self.grafica.append('\u0394\u03C7/(T K)')
                    self._plot(self._position_x, self._position_y, self.grafica, cursor=True)
                    #self.temperatura_reducida = self.temperatura_reducida.tolist()

                else:
                    QtWidgets.QMessageBox.question(self, 'Message', "You must enter the value of numeric." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)  
                return True

            except ValueError:
                QtWidgets.QMessageBox.question(self, 'Error', "You must enter the value of numeric  or The vector must be equal" + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return False

        else:
            QtWidgets.QMessageBox.question(self, 'Message', "It would help if you Calculated the Tco Value" + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def _dimensionalidad(self):
        self.tco1.setEnabled(False)
        self.tco2.setEnabled(False)
        self.size_x_max.clear()
        self.size_x_min.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self._size_x.clear()
        self._size_y.clear()
        self.temperatura_reducida = self.temperatura_reducida.tolist()        
        if (self.Tco and self.temperatura_reducida):
            self.temperatura_reducida = pd.Series(self.temperatura_reducida)
            try:            
                delta_inv = -1 * (self.delta_t)        
                delta_inv = delta_inv.dropna()
                aux_delta = delta_inv.to_numpy()

                posicionBorrar =  np.where(aux_delta < 0)[0]
                posicionBorrar_1 = np.where(aux_delta == 0)[0]

                temperatura_reducida_new = self.temperatura_reducida      
            
                aux_temp = temperatura_reducida_new.to_numpy()      
                
                
                TemReducidaBorrar =  np.where(aux_temp < 0)[0]
                TempReducidaBorrar_1 = np.where(aux_temp == 0)[0]
                concatenar = np.concatenate((posicionBorrar,posicionBorrar_1), axis=0)        
                
                mj2 = set(concatenar)
                mj2 = sorted (list(mj2))
            

                concatenar_temp = np.concatenate((TemReducidaBorrar,TempReducidaBorrar_1), axis=0)       
                mj3 = set(concatenar_temp)
                mj3 = sorted (list(mj3))

                concatenar_temp = np.concatenate((mj2,mj3), axis=0)       
                mj4 = set(concatenar_temp)
                mj4 = sorted (list(mj4))
                arreglo = np.array(mj4)
                    
                temp_delta = np.delete (aux_delta, (arreglo))
                temp_reducida = np.delete(aux_temp, (arreglo))     
                            

                log_delta = np.log10(temp_delta)       
                inv_log_delta = -1*(log_delta) 
                log_temperatura_reducida = np.log10(temp_reducida)
                        
                self._position_x = []
                self._position_y = []

                
                self._position_x.append(log_temperatura_reducida)
                self._position_y.append(inv_log_delta)

                self.grafica = []
                self.grafica.append('')
                self.grafica.append('Log (-\u0394\u03C7/T) (K^-1)')
                self.grafica.append('(T-Tco)/Tco')
                self._plot(self._position_x, self._position_y, self.grafica,cursor=True)

                
                
            except ValueError:
                QtWidgets.QMessageBox.critical(self, "Be Careful", "You must enter the value of numeric the mass or The vector must be equal",
                                                QtWidgets.QMessageBox.Ok)
                return False                     
        else:
            QtWidgets.QMessageBox.critical(self, "Tco", "you must Calculate Tco or coherecia longitud",
                                QtWidgets.QMessageBox.Ok)
   
    def _send(self):

        self.enviar.tableaboveTco.setItem(1, 0, QtWidgets.QTableWidgetItem(str("Sm358")))
        self.enviar.tableaboveTco.setItem(1, 1, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(self.Tc))))
        self.enviar.tableaboveTco.setItem(1, 2, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(self.Tirr))))
        self.enviar.tableaboveTco.setItem(1, 3, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(self.Tco))))
        self.enviar.tableaboveTco.setItem(1, 4, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(self.dimensionalidad))))
        self.enviar.tableaboveTco.setItem(1, 5, QtWidgets.QTableWidgetItem(str("{0:.2E}".format(self.Asl))))
        self.enviar.tableaboveTco.setItem(1, 6, QtWidgets.QTableWidgetItem(str("{0:.2E}".format(self.Bld))))
        self.enviar.tableaboveTco.setItem(1, 7, QtWidgets.QTableWidgetItem(str("{0:.2E}".format(self.longitud_coerencia_ab))))
        self.enviar.tableaboveTco.setItem(1, 8, QtWidgets.QTableWidgetItem(str("{0:.2E}".format(self.longitud_coerencia_c))))
        self.enviar.tableaboveTco.setItem(1, 9, QtWidgets.QTableWidgetItem(str("{0:.2E}".format(self.gamma))))        
        self.enviar.tableaboveTco.setItem(1, 10, QtWidgets.QTableWidgetItem(str(self.now)))

        self.enviar.Tc = str("{0:.2f}".format(self.Tc))
        self.enviar.Tirr = str("{0:.2f}".format(self.Tirr))
        self.enviar.Tco = str("{0:.2f}".format(self.Tco))
        self.enviar.Asl = str("{0:.2E}".format(self.Asl))
        self.enviar.Bld = str("{0:.2E}".format(self.Bld))
        self.enviar.longitud_coerencia_ab = str("{0:.2E}".format(self.longitud_coerencia_ab))
        self.enviar.longitud_coerencia_c = str("{0:.2E}".format(self.longitud_coerencia_c))
        self.enviar.gamma = str("{0:.2E}".format(self.gamma))
        self.enviar.dimensionalidad = str("{0:.2F}".format(self.dimensionalidad))
        self.enviar.Fecha = str(self.now)

    def _plot(self, x, y, grafica, x_lim=[], y_lim=[], cursor=False, data_aux_x=[], data_aux_y=[]):
        self.figure.clear()
        x = np.array(x)
        y = np.array(y)
        colors = ['K', 'B' ,'G']

        axes = self.figure.add_subplot(1, 1, 1)
        axes.set_title(grafica[0])
        axes.set_xlabel(grafica[1])
        axes.set_ylabel(grafica[2])
        
        if cursor:
            self.cursor = Cursor(axes, useblit=True, color='green', linewidth=1)
            self.move_cursor = self.canvas.mpl_connect('button_press_event', self._onmove)
        else:
            if self.move_cursor:
                self.canvas.mpl_disconnect(self.move_cursor)
        tam = len(x.shape)
        if len(x_lim) > 0:
            axes.set_xlim(x_lim[0], x_lim[1])
            axes.set_ylim(y_lim[0], y_lim[1])
        if tam > 1:
            for data in range(x.shape[0]):
                axes.scatter(x[data], y[data],color=colors[data],s = 5)
        else:
            axes.plot(x, y)
        if len(data_aux_x)>0:
            axes.plot(data_aux_x, data_aux_y, '-*', color ='orange')
        axes.grid(True)
        self.canvas.draw()
  
    def _zoom (self):
        matplotlib.use('Qt5Agg')
        x = np.array(self._position_x)
        y = np.array(self._position_y)
        colors = ['K', 'B' ,'G']

        figure = plt.figure(figsize=(8,5))
        axes = figure.add_subplot(1, 1, 1)
        
        tam = len(x.shape)
        if tam > 1:
            for data in range(x.shape[0]):
                axes.scatter(x[data], y[data],color=colors[data],s = 5)
        else:
            axes.plot(x, y)        
        plt.show()
        
    def _reportdatabase(self):
        self.reportesdatos = Ventana_Database()
        self.reportesdatos.exec_()

class Ventana_help(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('../QtDesigner/help.ui', self)    

class Ventana_Database(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('../QtDesigner/Database.ui', self)   
        self.documento = QtGui.QTextDocument()

        # =================== WIDGET QTREEWIDGET ===================
        #self.treeaboveTco.setHeaderHidden(True)
        self.treeaboveTco.setRootIsDecorated(True)
        self.treeaboveTco.setHeaderLabels(["muestra", "tc", "tirr", "tco", "dimensionalidad", "asl", "bld", "longitudab", "longitudc", "gamma", "fecha"])

        self.model = self.treeaboveTco.model()

        for indice, ancho in enumerate((100, 100, 100, 100), start=0):
            self.model.setHeaderData(indice, QtCore.Qt.Horizontal, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)
            self.treeaboveTco.setColumnWidth(indice, ancho)

        self.treeaboveTco.setAlternatingRowColors(True)

        # =================== EVENTOS QPUSHBUTTON ==================

        self.searchAbove.clicked.connect(self._searchAboveTco)
        self.searchBelow.clicked.connect(self._searchBelowTco)
        self.buttonLimpiar.clicked.connect(self._tableclean)

        self.buttonVistaPrevia.clicked.connect(self._preview)
        self.buttonExportarPDF.clicked.connect(self._exportPDF)

    def _searchAboveTco(self):
        self.connection = pymysql.connect(
            host='localhost',  # ip
            user='root',
            password='12345',
            db='cupratos')

        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT muestra, tc, tirr, tco, dimensionalidad, asl, bld, longitudab, longitudc, gamma, fecha FROM cupratos.abovetco;")
        datosDB = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        
        if datosDB:
            self.documento.clear()
            self.treeaboveTco.clear()
            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % dato
                item_widget.append(QtWidgets.QTreeWidgetItem(
                    (str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]), str(dato[4]), str(dato[5]), str(dato[6]),str(dato[7])+
                    str(dato[8]),str(dato[9]),str(dato[10]))))

            reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: center;
   }
table {
       font-family: arial, sans-serif;
       border-collapse: collapse;
       width: 100%;
      }
td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
   }
th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
   }
tr:nth-child(even) {
                    background-color: #dddddd;
                   }
</style>
</head>
<body>

<h3>Critical parameters<br/></h3>
<img src="../img/GSM.jpg" >
<table align="center" width="100%" cellspacing="0">
  <tr>
    <th>Sample</th>
    <th>Tc</th>
    <th>Tirr</th>
    <th>Tco</th>
    <th>LongitudCoherencia</th>
    <th>Suceptibilidad</th>
    <th>Fecha</th>
  </tr>
  [DATOS]
</table>
</body>
</html>
""".replace("[DATOS]", datos)

            datos = QtCore.QByteArray()
            datos.append(str(reporteHtml))
            codec = QtCore.QTextCodec.codecForHtml(datos)
            unistr = codec.toUnicode(datos)

            if QtCore.Qt.mightBeRichText(unistr):
                self.documento.setHtml(unistr)
            else:
                self.documento.setPlainText(unistr)

            self.treeaboveTco.addTopLevelItems(item_widget)
        else:
            QtWidgets.QMessageBox.information(self, "AboveTco", "No results found.",
                                    QtWidgets.QMessageBox.Ok)

    def _searchBelowTco(self):
        self.connection = pymysql.connect(
            host='localhost',  # ip
            user='root',
            password='12345',
            db='cupratos')

        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT muestra,t,emu,m,fecha FROM cupratos.belowtco;")
        datosDB = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        
        if datosDB:
            self.documento.clear()
            self.treeaboveTco.clear()
            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</tr>" % dato
                item_widget.append(QtWidgets.QTreeWidgetItem(
                    (str(dato[0]), str(dato[1]), str(dato[2]), str(dato[3]), str(dato[4]))))

            reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: center;
   }
table {
       font-family: arial, sans-serif;
       border-collapse: collapse;
       width: 100%;
      }
td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
   }
th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
   }
tr:nth-child(even) {
                    background-color: #dddddd;
                   }
</style>
</head>
<body>
<h3>Critical parameters<br/></h3>
<table align="center" width="100%" cellspacing="0">
  <tr>
    <th>Muestra</th>
    <th>T</th>
    <th>Emu</th>
    <th>m</th>
    <th>Fecha</th>
  </tr>
  [DATOS]
</table>
</body>
</html>
""".replace("[DATOS]", datos)

            datos = QtCore.QByteArray()
            datos.append(str(reporteHtml))
            codec = QtCore.QTextCodec.codecForHtml(datos)
            unistr = codec.toUnicode(datos)
            if QtCore.Qt.mightBeRichText(unistr):
                self.documento.setHtml(unistr)
            else:
                self.documento.setPlainText(unistr)

            self.treeaboveTco.addTopLevelItems(item_widget)
        else:
            QtWidgets.QMessageBox.information(self, "AboveTco", "No results found.",
                                    QtWidgets.QMessageBox.Ok)
    def _tableclean(self):
        self.documento.clear()
        self.treeaboveTco.clear()

    def _preview(self):
        if not self.documento.isEmpty():
            impresion = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)

            vista = QtPrintSupport.QPrintPreviewDialog(impresion, self)
            vista.setWindowTitle("Preview")
            vista.setWindowFlags(QtCore.Qt.Window)
            vista.resize(800, 600)

            exportarPDF = vista.findChildren(QtWidgets.QToolBar)
            exportarPDF[0].addAction(QtGui.QIcon("exportarPDF.png"), "Export to a PDF", self._exportPDF)

            vista.paintRequested.connect(self._previewImpresion)
            vista.exec_()
        else:
            QtWidgets.QMessageBox.critical(self, "preview", "There is no data to display",
                                 QtWidgets.QMessageBox.Ok)

    def _previewImpresion(self,impresion):
        self.documento.print_(impresion)

    def _print(self):
        if not self.documento.isEmpty():
            impresion = QtWidgets.QPrinter(QtPrintSupport.QPrinter.HighResolution)

            dlg = QtPrintSupport.QPrintDialog(impresion, self)
            dlg.setWindowTitle("Print document")

            if dlg.exec_() == QtPrintSupport.QPrintDialog.Accepted:
                self.documento.print_(impresion)

            del dlg
        else:
            QtWidgets.QMessageBox.critical(self, "Print", "There is no data to display.  ",
                                 QtWidgets.QMessageBox.Ok)

    def _exportPDF(self):
        if not self.documento.isEmpty():
            nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Exportar a PDF", "AboveTco",
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QtWidgets.QFileDialog.Options())

            if nombreArchivo:            
                impresion = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
                impresion.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
                impresion.setOutputFileName(nombreArchivo)
                self.documento.print_(impresion)

                QtWidgets.QMessageBox.information(self, "Exportar a PDF", "Data  export successful   ",
                                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, "Exportar a PDF", "there is no data to export.   ",
                                 QtWidgets.QMessageBox.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())