# -*- coding: utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-four\config.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets,QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(742, 523)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(210, 390, 281, 51))
        self.horizontalLayoutWidget.setObjectName(("horizontalLayoutWidget"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(("horizontalLayout"))
        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(("radioButton_2"))
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName(("radioButton"))
        self.horizontalLayout.addWidget(self.radioButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(250, 450, 195, 61))
        self.horizontalLayoutWidget_2.setObjectName(("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName(("horizontalLayout_3"))
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 731, 351))
        self.gridLayoutWidget.setObjectName(("gridLayoutWidget"))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(("gridLayout"))
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName(("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName(("lineEdit_6"))
        self.gridLayout.addWidget(self.lineEdit_6, 3, 1, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName(("lineEdit_5"))
        self.gridLayout.addWidget(self.lineEdit_5, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName(("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName(("lineEdit_7"))
        self.gridLayout.addWidget(self.lineEdit_7, 4, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Bell MT"))
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName(("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(("Agency FB"))
        font.setPointSize(12)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName(("lineEdit_8"))
        self.gridLayout.addWidget(self.lineEdit_8, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", u"配置远程参数", None))
        self.radioButton_2.setText(_translate("Dialog", u"启用", None))
        self.radioButton.setText(_translate("Dialog", u"拒用", None))
        self.pushButton_2.setText(_translate("Dialog", u"保存", None))
        self.pushButton.setText(_translate("Dialog", u"取消", None))
        self.label_4.setText(_translate("Dialog", u"  通过用户同步路径:", None))
        self.label_6.setText(_translate("Dialog", u" 通过流水号同步路径:", None))
        self.label_5.setText(_translate("Dialog", u"        登录路径:", None))
        self.label_7.setText(_translate("Dialog", u"数据上传远程系统路径:", None))
        self.label_8.setText(_translate("Dialog", u"      远程系统名称:", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

