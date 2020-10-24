# -*- coding: utf-8 -*-
import sys

#from visualizar import *
from sqlite3 import connect
from PyQt5 import QtPrintSupport
import matplotlib
from matplotlib.widgets import Cursor, PolygonSelector 

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sklearn
#import sklearn.utils._cython_blas
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

from Reportes import *
from ventana_data import *
from ventana_database import *
from ventana_help import*

import pandas as pd
import numpy as np
import math

import os

from datetime import datetime

font = {'family': 'arial',
        'size': 7}
matplotlib.rc('font', **font)


class App(QtWidgets.QMainWindow, Ui_VentanaTco):
    Reportes = None
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent) 
        self.setupUi(self)       
        self.enviar = reportes(self)
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
        self.muestra = ""
        self.Tc = 0
        self.Tirr = 0
        self.Tco = 0
        self.Asl = 0
        self.Bld = 0
        self.longitud_coerencia_ab = 0
        self.longitud_coerencia_c = 0
        self.gamma = 0
        self.dimensionalidad = 0
        self.now = datetime.now().strftime('%Y-%m-%d')
        self.imagen = QtGui.QImage()
        self.data = None
        self.regresionx_p = None
        self.regresionx_p1 = None
        self.regresiony_p = None
        self.regresiony_p1 = None
        self.zfc = None
        self.fc = None
        self.temperaturatco_x   =None
        self.suceptibilidad_y   =None
        self.temperaturatco_x1  =None
        self.suceptibilidad_y1  =None
        self.temperaturatco1_x  =None
        self.pos_delta_tco      =None
        self.log_temperatura    =None
        self.inv_delta          =None 
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(1200, 750)
        self.setMaximumSize(1200, 750)
        self.setWindowIcon(QtGui.QIcon(self.iconName))

        # crear el menu

        exitAct = QtWidgets.QAction(QtGui.QIcon('../Img/exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+q')
        exitAct.triggered.connect(QtWidgets.qApp.quit)

        
        openFile = QtWidgets.QAction(QtGui.QIcon('../Img/openFile.png'), 'Open File', self)
        openFile.setShortcut('Ctrl+o')
        openFile.triggered.connect(self._openData)


        Help = QtWidgets.QAction(QtGui.QIcon('../Img/help.png'), 'Help', self)
        Help.triggered.connect(self._help)

        cleanWindow = QtWidgets.QAction(QtGui.QIcon('../Img/clean.png'),'Clean Window',self)
        cleanWindow.triggered.connect(self._clean)
      

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(cleanWindow)
        self.toolbar.addAction(Help)
        self.toolbar.addAction(exitAct)       
        self.show()

        self.Button_Set.setEnabled(False)
        self.calcular.setEnabled(False)
        self.exportcsv.setEnabled(False)
        self.Masa.setEnabled(False)
        self.Tinicial.setEnabled(False)
        self.buttonloaded.setEnabled(False)
        self.Muestra.setEnabled(False)
        self.savePicture.setEnabled (False)
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
        
        self.fecha.setText(str(self.now))
        self.aboveTco_2.addItem("\u03BE")
        self.aboveTco_2.addItem("\u03C7")

        self.belowTco_2.addItem("\u0394 M*,T*")
        self.belowTco_2.addItem("Theoretical Ms*")
        self.belowTco_2.addItem("\u03BB ab(0)")
        self.belowTco_2.addItem("Hc2(0)")

        self.calcular.clicked.connect(self._getItem)
        self.btnenviar.clicked.connect(self._send)
        self.dataBase.clicked.connect(self._reportdatabase)
        self.Button_Set.clicked.connect(self._arena_size)
        self.Button_Zoom.clicked.connect(self._zoom)
        self.buttonloaded.clicked.connect(self._loaded)
        self.savePicture.clicked.connect (self._savePicture)
        self.exportcsv.clicked.connect(self._savecsv)
        
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
            self.Muestra.setEnabled(True)
            self.savePicture.setEnabled (True)
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
            self.buttonloaded.setEnabled (True)
            self.Button_Set.setEnabled(True)
            self.aboveTco_2.setEnabled(True)
            self.belowTco_2.setEnabled(True)
            self.exportcsv.setEnabled(True)
            self.loaded.setPixmap(QtGui.QPixmap("../Img/puntoverde.png"))

            self.TableDataset.setColumnCount(len(self.dataset.columns))
            self.TableDataset.setRowCount(len(self.dataset.index))
            for i in range(len(self.dataset.index)):
                for j in range(len(self.dataset.columns)):
                    self.TableDataset.setItem(i,j,QtWidgets.QTableWidgetItem(str(self.dataset.iloc[i,j])))
   
    def _clean(self):
        self.Masa.clear()
        self.Muestra.clear()
        self.Tinicial.clear()
        self.Tfinal.clear()
        self.Minicial.clear()
        self.Mfinal.clear()
        self.Datoinicialzfc.clear()
        self.Datofinalzfc.clear()
        self.Datoinicialfc.clear()
        self.Datofinalfc.clear()
        self.Distanciainterplanar.clear()
        self.size_x_min.clear()
        self.size_x_max.clear()
        self.size_y_min.clear()
        self.size_y_max.clear()
        self.field.clear()
        self.column.clear()
        self.figure.clear()
        #self.TableDataset.clear()
        #self.TableDataset.setItem(0, 0, QtWidgets.QTableWidgetItem(str("Temperature (K)")))
        #self.TableDataset.setItem(0, 1, QtWidgets.QTableWidgetItem(str("Magnetic Field (Oe)" )))
        #self.TableDataset.setItem(0, 2, QtWidgets.QTableWidgetItem(str("Moment (emu)")))
        
    def _loaded (self):        
        self.df = self.datos.parse(self.field.currentText())         
        self.TableDataset.setColumnCount(len(self.dataset.columns))
        self.TableDataset.setRowCount(len(self.dataset.index))
        for i in range(len(self.dataset.index)):
            for j in range(len(self.dataset.columns)):
                self.TableDataset.setItem(i,j,QtWidgets.QTableWidgetItem(str(self.df.iloc[i,j])))

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
        elif self.Muestra.text() == "":
            QtWidgets.QMessageBox.question(self, 'Sample Name', "You must enter the Sample Name " + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        else:
            self.muestra = self.Muestra.text()            
            self.dato_inicial = self.Datoinicialzfc.text()
            self.dato_final = self.Datofinalzfc.text()
            masa = self.Masa.text()
            try:
                masa = float(masa)
                if ((self.dato_inicial.isnumeric() == True)  and (self.dato_final.isnumeric() == True)):                            
                    self.dato_inicial = int(self.dato_inicial)
                    self.dato_final = int(self.dato_final)       
                    Momentum = self.df['Moment (emu)']
                    Magnetizacion = Momentum / masa
                    self.df["Magnetizacion"] = Magnetizacion
                    self.data = self.df[self.dato_inicial:self.dato_final][["Temperature (K)", "Magnetizacion"]]
                    self._position_x = self.data['Temperature (K)']
                    self._position_y = self.data["Magnetizacion"]
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
                

        self.df = self.datos.parse(self.field.currentText())

        if (self.Tinicial.text() == "" or self.Tfinal.text() == "" or self.Minicial.text() == "" or self.Mfinal.text() == "" or self.Datoinicialzfc.text() == "" or self.Datofinalzfc.text() == ""):
            QtWidgets.QMessageBox.question(self, 'TC', "You must fill all the fields." + "",
                                           QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        elif self.Masa.text() == "":
            QtWidgets.QMessageBox.question(self, 'Mass', "You must enter the value of the mass." + "",
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
                t_inicial = float(t_inicial)
                t_final = float(t_final)
                m_inicial = float(m_inicial)
                m_final = float(m_final)
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

                self.regresionx_p = np.array(x_p_aux)
                self.regresionx_p1 = np.array(x_p1_aux)
                self.regresiony_p = np.array(y_p_aux)
                self.regresiony_p1 = np.array(y_p1_aux)

                self.grafica = []
                self.grafica.append('')
                self.grafica.append('T (K)')
                self.grafica.append('M (emu/g)')
                self._plot(self._position_x, self._position_y, self.grafica)

                estad_st = "Tc " + str("{0:.3f}".format(self.Tc) + " " + "K")                      
                self.resultados.setText(str(estad_st))
                return True
            except ValueError:
                QtWidgets.QMessageBox.critical(self, 'Warning', "You must enter the value of numeric.",
                                QtWidgets.QMessageBox.Ok)
                 
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
            try:
                masa = float(masa)
                if ((datoInicialFc.isnumeric() == True)  and (datoFinalFc.isnumeric() == True) and  (dato_inicial.isnumeric() == True) and (dato_final.isnumeric() == True)):                    
                    datoInicialFc = int(datoInicialFc)
                    datoFinalFc = int(datoFinalFc)
                    dato_inicial = int(dato_inicial)
                    dato_final = int(dato_final)
                    Momentum = self.df['Moment (emu)']
                    Magnetizacion = Momentum / masa
                    self.df["Magnetizacion"] = Magnetizacion
                    self.zfc = self.df[dato_inicial:dato_final][["Temperature (K)", "Magnetizacion"]]
                    self.fc = self.df[datoInicialFc:datoFinalFc][["Temperature (K)", "Magnetizacion"]]                 
                    self._position_x = []
                    self._position_y = []
                    self._position_x.append(self.fc['Temperature (K)'])
                    self._position_x.append(self.zfc['Temperature (K)'])

                    self._position_y.append(self.fc["Magnetizacion"])
                    self._position_y.append(self.zfc["Magnetizacion"])

                    self.grafica = []
                    self.grafica.append('')
                    self.grafica.append('T (K)')
                    self.grafica.append('M (emu/g)')
                    self._plot(self._position_x, self._position_y, self.grafica, cursor=True)
                
                else:
                    QtWidgets.QMessageBox.critical(self, 'Warning', "You must enter the value of numeric.",
                                QtWidgets.QMessageBox.Ok)
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
                    estad_st = "Tirr " + str("{0:.3f}".format(self.Tirr[0]))+ " " + "K"                      
                    self.resultados.setText(str(estad_st))
                    self.Tirr = float(self.Tirr[0])
                    
            if len(self.point_y)==2:
                if self.aboveTco_2.currentText().strip()=="Tco":
                    pendiente = (self.point_y[0] - self.point_y[1]) / (self.point_x[0] - self.point_x[1])
                    corte_y = self.point_y[1] - pendiente * self.point_x[1]
                    corte_x = -((corte_y) / pendiente)
                    self.Tco = corte_x
                    estad_st = "Tco " + str("{0:.3f}".format(self.Tco))+ " " + "K"
                    
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
                        FI = 2.067833636e-15
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

                        print (a)
                        print (b)

                       
                        self.Asl = 1 / (math.sqrt(4 * abs(a)))
                        self.Bld = b * (self.Asl ** 2) 
                        self.Asl = abs (self.Asl)  
                        self.Bld = abs(self.Bld)
                        
                        
                        self.longitud_coerencia_ab = (math.sqrt((3 * self.Asl * FI ** 2 * self.s) / (PERMEABILIDAD_VACIO * CONSTATE_BOLTZMANN * math.pi)))
                        
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
            QtWidgets.QMessageBox.question(self, 'Mass', "You must enter the value of the mass." + "",
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
                                                    
                        self._position_x.append(temperatura[dato_inicial:vector[0]])
                        self._position_x.append(temperatura[dato_inicial:vector[0]])

                        self._position_y.append(suceptibilidad[dato_inicial:vector[0]])
                        self._position_y.append(inv_x_normal[dato_inicial:vector[0]])

                        self.temperaturatco_x = temperatura[dato_inicial:vector[0]]
                        self.suceptibilidad_y = suceptibilidad[dato_inicial:vector[0]]
                        self.temperaturatco_x1 = temperatura[dato_inicial:vector[0]]
                        self.suceptibilidad_y1 = suceptibilidad[dato_inicial:vector[0]]                 

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

                        self.temperaturatco1_x = temperatura[dato_inicial:dato_final]
                        self.pos_delta_tco = pos_delta_t[dato_inicial:dato_final]

                        self.grafica = []
                        self.grafica.append('')
                        self.grafica.append('T (K)')
                        self.grafica.append('-T/\u0394\u03C7')
                        self._plot(self._position_x,self._position_y, self.grafica, cursor=True)
                        plt.axhline(0, color='g', xmax=70)

                else:
                    QtWidgets.QMessageBox.critical(self, 'Warning', "You must enter the value of numeric.",
                                QtWidgets.QMessageBox.Ok)
                    
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
                    self.grafica.append('(T/\u0394\u03C7)^2')
                    self._plot(self._position_x, self._position_y, self.grafica, cursor=True)
                    

                else:
                    QtWidgets.QMessageBox.critical(self, 'Warning', "You must enter the value of numeric.",
                                QtWidgets.QMessageBox.Ok)
                     
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

                self.log_temperatura = log_temperatura_reducida
                self.inv_delta = inv_log_delta
                self.grafica = []
                self.grafica.append('')
                self.grafica.append('Log(T-Tc0)/Tc0')
                self.grafica.append('Log(-\u0394\u03C7/T)')
                
                self._plot(self._position_x, self._position_y, self.grafica,cursor=True)               
                
            except ValueError:
                QtWidgets.QMessageBox.critical(self, "Be Careful", "You must enter the value of numeric the mass or The vector must be equal",
                                QtWidgets.QMessageBox.Ok)
                return False                     
        else:
            QtWidgets.QMessageBox.critical(self, "Tco", "you must Calculate Tco or coherecia longitud",
                                QtWidgets.QMessageBox.Ok)
   
    def _send(self):

        self.enviar.tableaboveTco.setItem(1, 0, QtWidgets.QTableWidgetItem(self.muestra))
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

        self.enviar.muestra = self.muestra
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
        colors = ['K', 'G' ,'B']

        axes = self.figure.add_subplot(1, 1, 1)
        axes.set_title(grafica[0])
        axes.set_xlabel(grafica[1])
        axes.set_ylabel(grafica[2])
        
        if cursor:
            self.cursor = Cursor(axes, useblit=True, color='green', linewidth=1)
            self.move_cursor = self.canvas.mpl_connect('button_press_event', self._onmove)
            item = self.aboveTco_2.currentText().strip()
            if item == "Tirr":
                self.move_cursor = PolygonSelector(axes, self._onmove,lineprops={'zorder': 5, 'color': 'gray'})
            if item == "Tco":
                if self.tco2.isChecked() == True:
                    axes.axhline(0, color='g', xmax=70)
                    self.move_cursor = PolygonSelector(axes, self._onmove,lineprops={'zorder': 5, 'color': 'gray'})
            elif item == "\u03C7":
                self.move_cursor = PolygonSelector(axes, self._onmove,lineprops={'zorder': 5, 'color': 'gray'})

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
            axes.plot(data_aux_x, data_aux_y, '-o', color ='orange')
        axes.grid(True)
        self.canvas.draw()
    
    def _savePicture(self):
        item = self.aboveTco_2.currentText().strip()
        figura = plt.savefig(item,bbox_inches='tight')
        
        imagen, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export to Picture', item ,
                                                                    "Archivos PNG (*.png);;All Files (*)",
                                                                    options=QtWidgets.QFileDialog.Options())
        if imagen:
            figura = plt.savefig(item,bbox_inches='tight')
            QtWidgets.QMessageBox.information(self, "Export to Picture ", "Picture  export successful",
                                    QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, "Export to Picture ", "there is no data to export.   ",
                                 QtWidgets.QMessageBox.Ok)
     
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

    def _savecsv(self):
        item = self.aboveTco_2.currentText().strip()
        if item == "ZFC":
            filename_output = "../Archivos_csv/ZFC.csv"          
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',os.getenv('Home'),"Archivos CSV (*.csv);;All Files (*)")
            if path[0] != '':                
                    archive_final= pd.DataFrame({"Temperatura (K)": self.data['Temperature (K)'] , "Magnetizacion":self.data["Magnetizacion"] })
                    archive_final.to_csv(filename_output, header = True, index=False)                    
                    QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful   ",
                                        QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.   ",
                                 QtWidgets.QMessageBox.Ok)
        elif item == "Tc":
            filename_output = "../Archivos_csv/TC.csv"          
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',os.getenv('HOME'), "Archivos CSV (*.csv);;All Files (*)")
            if path[0] != '':                                  
                    archive_final= pd.DataFrame({"Temperatura (K)": self.data['Temperature (K)'] , "Magnetizacion":self.data["Magnetizacion"], "Regresión Fase normal x":self.regresionx_p,
                                                "Regresion Fase normal y": self.regresiony_p, "Regresion Fase Superconductora x": self.regresionx_p1, "Regresion Fase Superconductora y":self.regresiony_p1})
                    archive_final.to_csv(filename_output, header = True, index=False)                    
                    QtWidgets.QMessageBox.information(self, "Exportar  cvs", "Data  export successful   ",
                                        QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.   ",
                                 QtWidgets.QMessageBox.Ok)
        elif item == "Tirr":
            filename_output = "../Archivos_csv/Tirr.csv"          
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',  os.getenv('Home'), "Archivos CSV (*.csv);;All Files (*)")
            if path[0] != '':                
                    archive_final= pd.DataFrame({"Temperatura_FC (K)": self.fc['Temperature (K)'] , "Magnetizacion_FC":self.fc["Magnetizacion"],
                                                "Temperatura_ZFC (K)": self.zfc['Temperature (K)'] , "Magnetizacion_ZFC":self.zfc["Magnetizacion"]})
                    archive_final.to_csv(filename_output, header = True, index=False)                    
                    QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful ",
                                        QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.",
                                 QtWidgets.QMessageBox.Ok)
        elif item == "Tco":
            if self.tco1.isChecked() == True:
                filename_output = "../Archivos_csv/Tco_1.csv"          
                path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',  os.getenv('Home'), "Archivos CSV (*.csv);;All Files (*)")
                if path[0] != '':             
                        archive_final= pd.DataFrame({"Temperatura (K)": self.temperaturatco_x, "Suceptibilidad":self.suceptibilidad_y,
                                                    "Temperatura (K)": self.temperaturatco_x1 , "Suceptibilidad":self.suceptibilidad_y1 })
                        archive_final.to_csv(filename_output, header = True, index=False)                    
                        QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful ",
                                            QtWidgets.QMessageBox.Ok)
                else:
                    QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.",
                                    QtWidgets.QMessageBox.Ok)
            
            if self.tco2.isChecked() == True:
                filename_output = "../Archivos_csv/Tco_2.csv"          
                path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',os.getenv('Home'), "Archivos CSV (*.csv);;All Files (*)")
                if path[0] != '':

                        archive_final= pd.DataFrame({"Temperatura (K)": self.temperaturatco1_x, "Delta":self.pos_delta_tco})
                        archive_final.to_csv(filename_output, header = True, index=False)                    
                        QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful ",
                                            QtWidgets.QMessageBox.Ok)
                else:
                    QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.",
                                    QtWidgets.QMessageBox.Ok)
         
        elif item == "\u03BE":
            filename_output = "../Archivos_csv/Longitud_coherencia.csv"          
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',  os.getenv('Home'), "Archivos CSV (*.csv);;All Files (*)")
            if path[0] != '':

                    archive_final= pd.DataFrame({"Temperatura (K)": self.temperatura_reducida[2:260], "Delta T":self.delta_t_cuadrado[2:260]})
                    archive_final.to_csv(filename_output, header = True, index=False)                    
                    QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful ",
                                        QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.",
                                QtWidgets.QMessageBox.Ok)
            
        elif item == "\u03C7":
            filename_output = "../Archivos_csv/Dimensionalidad.csv"          
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV',  os.getenv('Home'), "Archivos CSV (*.csv);;All Files (*)")
            if path[0] != '':    
                    archive_final= pd.DataFrame({"Log Temperatura (K)": self.log_temperatura, "Log Delta T":self.inv_delta})
                    archive_final.to_csv(filename_output, header = True, index=False)                    
                    QtWidgets.QMessageBox.information(self, "Exportar a cvs", "Data  export successful ",
                                        QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.critical(self, "Exportar Data", "there is no data to export.",
                                QtWidgets.QMessageBox.Ok)
            

class Ventana_help(QtWidgets.QDialog, Ui_Help):
    def __init__(self,*args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self) 

class Ventana_Database(QtWidgets.QDialog,Ui_Database):
    def __init__(self,*args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)   
        self.documento = QtGui.QTextDocument()

        # =================== WIDGET QTREEWIDGET ===================
        #self.treeaboveTco.setHeaderHidden(True)
        self.treeaboveTco.setRootIsDecorated(True)
        self.treeaboveTco.setHeaderLabels(["Sample", "Tc (K)", "Tirr (K)", "Tco (K)", "\u03C7", "Ax (x10^-8) (1/K)", "Bld", "\u03C7" + "c" + " (0) (Å)", "\u03BE" + "c" + " (0) (Å)", "\u03BB", "Date"])

        self.model = self.treeaboveTco.model()

        for indice, ancho in enumerate((100, 100, 100, 100), start=0):
            self.model.setHeaderData(indice, QtCore.Qt.Horizontal, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)
            self.treeaboveTco.setColumnWidth(indice, ancho)

        self.treeaboveTco.setAlternatingRowColors(True)

        # =================== EVENTOS QPUSHBUTTON ==================

        self.searchAbove.clicked.connect(self._searchAboveTco)
        self.searchBelow.setEnabled(False)
        #self.searchBelow.clicked.connect(self._searchBelowTco)
        self.buttonLimpiar.clicked.connect(self._tableclean)

        self.buttonVistaPrevia.clicked.connect(self._preview)
        self.buttonExportarPDF.clicked.connect(self._exportPDF)

    def _searchAboveTco(self):
        conexionDB = connect("../Database/cupratos.db")
        cursor = conexionDB.cursor()

        cursor.execute("SELECT Muestra,Tc,Tirr,Tco,Dimensionalidad,Asl,Bld,Longitudab,Longitudc,Gamma,Fecha FROM abovetco")
        datosDB = cursor.fetchall()
        
        if datosDB:
            self.documento.clear()
            self.treeaboveTco.clear()
            datos = ""
            item_widget = []
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % dato
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
    text-align: center;
    padding: 2px;
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
    <th>Sample</th>
    <th>Tc(K)</th>    
    <th>Tirr (K)</th>
    <th>Tco (K)</th>
    <th>"\u03C7"</th> 
    <th>Ax (x10^-8) (1/K)</th>
    <th>"Bld " + "\n" + "x10^-2")</th>
    <th>"\u03C7"</th>
    <th>"\u03BE" + "c" + " (0) (A)"</th>
    <th>"\u03BB"</th>       
    <th>Date</th>
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
        conexionDB = connect("../Database/cupratos.db")
        cursor = conexionDB.cursor()

        cursor.execute("SELECT Muestra,Tc,Tirr,Tco,Dimensionalidad,Asl,Bld,Longitudab,Longitudc,Gamma,Fecha FROM aboveTco")
        datosDB = cursor.fetchall()

        conexionDB.close()
        
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
            vista.resize(800, 800)

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