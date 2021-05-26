# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Database.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Database(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(711, 399)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Img/Telematica.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 81, 61))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../Img/GSM.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(560, 10, 141, 61))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../Img/Telematics.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(160, 30, 361, 31))
        self.label_4.setObjectName("label_4")
        self.searchAbove = QtWidgets.QPushButton(Dialog)
        self.searchAbove.setGeometry(QtCore.QRect(130, 90, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.searchAbove.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Img/Buscar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchAbove.setIcon(icon1)
        self.searchAbove.setIconSize(QtCore.QSize(25, 25))
        self.searchAbove.setObjectName("searchAbove")
        self.buttonLimpiar = QtWidgets.QPushButton(Dialog)
        self.buttonLimpiar.setGeometry(QtCore.QRect(370, 90, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.buttonLimpiar.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Img/limpiar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonLimpiar.setIcon(icon2)
        self.buttonLimpiar.setIconSize(QtCore.QSize(25, 25))
        self.buttonLimpiar.setObjectName("buttonLimpiar")
        self.buttonVistaPrevia = QtWidgets.QPushButton(Dialog)
        self.buttonVistaPrevia.setGeometry(QtCore.QRect(190, 330, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.buttonVistaPrevia.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Img/vistaprevia.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonVistaPrevia.setIcon(icon3)
        self.buttonVistaPrevia.setIconSize(QtCore.QSize(20, 20))
        self.buttonVistaPrevia.setObjectName("buttonVistaPrevia")
        self.buttonExportarPDF = QtWidgets.QPushButton(Dialog)
        self.buttonExportarPDF.setGeometry(QtCore.QRect(360, 330, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.buttonExportarPDF.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Img/exportar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonExportarPDF.setIcon(icon4)
        self.buttonExportarPDF.setIconSize(QtCore.QSize(20, 20))
        self.buttonExportarPDF.setObjectName("buttonExportarPDF")
        self.treeaboveTco = QtWidgets.QTreeWidget(Dialog)
        self.treeaboveTco.setGeometry(QtCore.QRect(40, 130, 621, 191))
        self.treeaboveTco.setObjectName("treeaboveTco")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Database"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Results Critical Parameters </span></p></body></html>"))
        self.searchAbove.setText(_translate("Dialog", "Search Above Tco"))
        self.buttonLimpiar.setText(_translate("Dialog", "Clean Table"))
        self.buttonVistaPrevia.setText(_translate("Dialog", "Preview"))
        self.buttonExportarPDF.setText(_translate("Dialog", "Export to PDF"))
        self.treeaboveTco.headerItem().setText(0, _translate("Dialog", "Sample"))
        self.treeaboveTco.headerItem().setText(1, _translate("Dialog", "Longitud Coherencia"))
        self.treeaboveTco.headerItem().setText(2, _translate("Dialog", "Tc"))
        self.treeaboveTco.headerItem().setText(3, _translate("Dialog", "x"))
        self.treeaboveTco.headerItem().setText(4, _translate("Dialog", "y"))
        self.treeaboveTco.headerItem().setText(5, _translate("Dialog", "New Column"))
        self.treeaboveTco.headerItem().setText(6, _translate("Dialog", "New Column"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Database()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
