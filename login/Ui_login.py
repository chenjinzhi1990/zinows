# -*- coding: utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-style\login.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,QtWidgets,QtGui


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(628, 362)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 80, 521, 161))
        self.gridLayoutWidget.setObjectName(("gridLayoutWidget"))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(("gridLayout"))
        
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 2, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(("font: 16pt \"Arial\";"))
        self.lineEdit.setObjectName(("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 2, 1)
        
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 2, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName(("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 4, 1, 2, 1)
        
        
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(150, 290, 291, 51))
        self.horizontalLayoutWidget_4.setObjectName(("horizontalLayoutWidget_4"))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setObjectName(("horizontalLayout_4"))
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(160, 250, 271, 29))
        self.groupBox.setTitle((""))
        self.groupBox.setObjectName(("groupBox"))
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(140, 10, 106, 16))
        self.radioButton.setObjectName(("radioButton"))
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(("radioButton_2"))
        
        
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 10, 611, 61))
        self.pushButton_3.setStyleSheet(("font: 75 16pt \"Arial\";\n"
"background-color: rgb(214, 214, 214);"))
        self.pushButton_3.setObjectName(("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", u"系统登录", None))
        self.pushButton_2.setText(_translate("Dialog", u"登录", None))
        self.pushButton.setText(_translate("Dialog", u"取消", None))
        self.radioButton.setText(_translate("Dialog", u"远程模式", None))
        self.radioButton_2.setText(_translate("Dialog", u"本地模式", None))
        self.label.setText(_translate("Dialog", u"用户  :", None))
        self.label_2.setText(_translate("Dialog", u"密码  :", None))
        self.pushButton_3.setText(_translate("Dialog", u"Zinows网页元素录制客户端", None))
#         self.pushButton_3.setText(_translate("Dialog", "USTC Xpath Gather System", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

