# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Help(object):
    def setupUi(self, ventana):
        ventana.setObjectName("ventana")
        ventana.setEnabled(True)
        ventana.resize(770, 551)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/Telematica.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ventana.setWindowIcon(icon)
        ventana.setAutoFillBackground(False)
        ventana.setSizeGripEnabled(False)
        self.textEdit = QtWidgets.QTextEdit(ventana)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 741, 311))
        self.textEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(ventana)
        self.label.setGeometry(QtCore.QRect(10, 340, 331, 141))
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setPixmap(QtGui.QPixmap("img/Telematics.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ventana)
        self.label_2.setGeometry(QtCore.QRect(440, 340, 211, 181))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("img/GSM.jpg"))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(ventana)
        QtCore.QMetaObject.connectSlotsByName(ventana)

    def retranslateUi(self, ventana):
        _translate = QtCore.QCoreApplication.translate
        ventana.setWindowTitle(_translate("ventana", "help"))
        self.textEdit.setHtml(_translate("ventana", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:8pt; font-weight:600;\"> </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:11pt;\">Los superconductores tienen resistencia eléctrica cero y se comportan como diamagnéticos perfectos, por tal razón presentan diferentes propiedades en la magnetización, el calor específico, el efecto termoeléctrico y la conductividad     térmica. Los superconductores de alta temperatura crítica en las últimas décadas son el centro de innumerables investigaciones debido a su alta anisotropía planar, lo que los hacen fuertes candidatos para el estudio del modelo de fluctuaciones magnéticas que permite el cálculo de parámetros críticos superconductores como: Longitud de coherencia, longitud de penetración, temperatura crítica, entre otros. El diseño de implementación de análisis experimental a un modelo de simulación mejora los tiempos de respuesta del cálculo de parámetros críticos superconductores del procesamiento de análisis de datos, dándole una trazabilidad en la generación de una interfaz de usuario para obtener resultados más confiables y precisos. Así, en este trabajo se propone el diseño y elaboración de una simulación con el fin de optimizar el cálculo de parámetros críticos superconductores a partir de un modelo de fluctuaciones magnéticas, y así mejorar los métodos de caracterización de materiales.</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt;\">Cristian Leonardo Cárdenas García</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt;\">    </span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = QtWidgets.QDialog()
    ui = Ui_Help()
    ui.setupUi(ventana)
    ventana.show()
    sys.exit(app.exec_())
