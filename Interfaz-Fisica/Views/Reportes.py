# -*- coding: utf-8 -*-
import sys
from ventana_reportes import *
from sqlite3 import connect
from PyQt5 import QtPrintSupport

class reportes(QtWidgets.QDialog,Ui_Reportes):
    def __init__(self, parent = None , *args, **kwargs, ):
        QtWidgets.QDialog.__init__(self,parent ,*args, **kwargs, )
        self.setupUi(self)
        self.parent = parent
        self.documento = QtGui.QTextDocument()
                
        # create table aboveTco

        self.tableaboveTco.setItem(0, 0, QtWidgets.QTableWidgetItem("Sample"))
        self.tableaboveTco.setItem(0, 1, QtWidgets.QTableWidgetItem("Tc (K)"))
        self.tableaboveTco.setItem(0, 2, QtWidgets.QTableWidgetItem("Tirr"))
        self.tableaboveTco.setItem(0, 3, QtWidgets.QTableWidgetItem("Tco (K)"))
        self.tableaboveTco.setItem(0, 4, QtWidgets.QTableWidgetItem("\u03C7"))
        self.tableaboveTco.setItem(0, 5, QtWidgets.QTableWidgetItem("Ax(1/K)"))
        self.tableaboveTco.setItem(0, 6, QtWidgets.QTableWidgetItem("Bld " + "\n" + "x10^-2"))
        self.tableaboveTco.setItem(0, 7, QtWidgets.QTableWidgetItem("\u03BE" + "ab" + " (0) (Å)"))
        self.tableaboveTco.setItem(0, 8, QtWidgets.QTableWidgetItem("\u03BE" + "c" + " (0) (Å)"))
        self.tableaboveTco.setItem(0, 9, QtWidgets.QTableWidgetItem("\u03BB"))
        self.tableaboveTco.setItem(0, 10, QtWidgets.QTableWidgetItem("Date"))

        # create table belowTco

        self.tablebelowTco.setItem(0, 0, QtWidgets.QTableWidgetItem("Sample"))
        self.tablebelowTco.setItem(0, 1, QtWidgets.QTableWidgetItem("T(K)"))
        self.tablebelowTco.setItem(0, 2, QtWidgets.QTableWidgetItem("Tirr"))
        self.tablebelowTco.setItem(0, 3, QtWidgets.QTableWidgetItem("Theoretical"))
        self.tablebelowTco.setItem(0, 4, QtWidgets.QTableWidgetItem("\u03C7" + " (0) (A)"))
        self.tablebelowTco.setItem(0, 5, QtWidgets.QTableWidgetItem("\u03C7"))
        self.tablebelowTco.setItem(0, 6, QtWidgets.QTableWidgetItem("Hc2 (O) (Oe)"))

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
        self.Fecha = ""       
        

        # Define values of critical parameters belowTco
        # self.tablebelowTco.setItem(0, 0, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 1, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 2, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 4, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 5, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 3, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))
        # self.tablebelowTco.setItem(0, 6, QtWidgets.QTableWidgetItem(str("{0:.2f}".format(12.5))))


        self.exportopdf.clicked.connect(self._exportarPDF)
        self.saveDatabase.clicked.connect(self._saveData)       


    def _exportarPDF(self):
        datosDB = [(self.muestra,self.Tco,self.Tirr,self.Tco,self.dimensionalidad,self.Asl,self.Bld,self.longitud_coerencia_ab,self.longitud_coerencia_c,self.gamma,self.Fecha)]     
        #print (datosDB)        
        if datosDB:
            self.documento.clear()
            datos = ""
            for dato in datosDB:
                datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %dato
        reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: arial, sans-serif;
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
    <th>\u03C7</th> 
    <th>Ax \n (1/K)</th>
    <th>Bld\nx10^-2</th>
    <th>\u03BE ab(0)(Å)</th>
    <th>\u03BE c(0)(Å)</th>
    <th>\u03BB</th>       
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

        if not self.documento.isEmpty():
            nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export to Pdf', "Critical Parameters",
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

    def _saveData(self):
        try:
            conexionDB = connect("../Database/cupratos.db")          

        except ValueError:
            QtWidgets.QMessageBox.information(self, "Failed to DataBase", ValueError,
                                    QtWidgets.QMessageBox.Ok)
            sys.exit(1)
        cursor = conexionDB.cursor()
        try:
            sql = "INSERT INTO abovetco(Muestra, Tc, Tirr, Tco, Dimensionalidad, Asl, Bld, Longitudab, Longitudc," \
                  "Gamma, Fecha) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            
            cursor.execute(sql, ("Sample",self.Tc, self.Tirr, self.Tco, self.dimensionalidad, self.Asl, self.Bld,
                    self.longitud_coerencia_ab, self.longitud_coerencia_c, self.gamma, self.Fecha))

            conexionDB.commit()                   
            QtWidgets.QMessageBox.information(self, "New Row", "a row inserted into the database",
                                    QtWidgets.QMessageBox.Ok)
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Be Careful", ValueError,
                                                QtWidgets.QMessageBox.Ok)
            conexionDB.rollback()
            return False
        cursor.close()
        conexionDB.close()
    