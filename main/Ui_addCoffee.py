# -*- coding: utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-four-bak\addCoffee.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(406, 178)
        Dialog.setMaximumSize(QtCore.QSize(450, 200))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 61))
        self.horizontalLayoutWidget.setObjectName(("horizontalLayoutWidget"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label.setStyleSheet(("font: 12pt \"Arial\";"))
        self.label.setObjectName(("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit.setObjectName(("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setObjectName(("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 80, 291, 51))
        self.horizontalLayoutWidget_2.setObjectName(("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(("horizontalLayout_2"))
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.label_2.setObjectName(("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.lineEdit_2.setObjectName(("lineEdit_2"))
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(80, 140, 80, 30))
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 140, 80, 30))
        self.pushButton_3.setObjectName(("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", u"添加类别", None))
        self.label.setText(_translate("Dialog", u"主题", None))
        self.pushButton.setText(_translate("Dialog", u"选择主题", None))
        self.label_2.setText(_translate("Dialog", u"类别", None))
        self.pushButton_2.setText(_translate("Dialog", u"添加", None))
        self.pushButton_3.setText(_translate("Dialog", u"取消", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

