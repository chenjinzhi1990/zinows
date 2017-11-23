# -*- coding: utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-seven\modifyXPath.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(628, 306)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 601, 211))
        self.gridLayoutWidget.setObjectName(("gridLayoutWidget"))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(("gridLayout"))
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit.setObjectName(("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit_2.setObjectName(("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_3.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit_3.setObjectName(("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_4.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit_4.setObjectName(("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 250, 93, 40))
        self.pushButton.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButton.setStyleSheet(("font: 12pt \"Arial\";"))
        self.pushButton.setObjectName(("pushButton"))
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 250, 93, 40))
        self.pushButton_2.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButton_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.pushButton_2.setObjectName(("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", u"查看|修改数据", None))
        self.label_2.setText(_translate("Dialog", "id", None))
        self.label.setText(_translate("Dialog", "xpath", None))
        self.label_3.setText(_translate("Dialog", "class", None))
        self.label_4.setText(_translate("Dialog", "input", None))
        self.pushButton.setText(_translate("Dialog", "modify", None))
        self.pushButton_2.setText(_translate("Dialog", "cancel", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

