# -*- coding: utf-8 -*-

'''
Created on 2017年11月10日

@author: zhang.meng
'''

from PyQt5 import  QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

import utils.auto_test3_image_rc
from main.Ui_modifyXPath import Ui_Dialog

class ModifyXpathDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, prev,modify_index = None,parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/image/images/logo.png"))
        self.prev = prev
        self.modify_index = modify_index
        self.initXpathData()
        
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        xpath_data = (self.lineEdit.text())
        id_data = (self.lineEdit_2.text())
        class_data = (self.lineEdit_3.text())
        input_data = (self.lineEdit_4.text())
        
        self.prev.tableWidget.item(self.modify_index,1).setText(xpath_data)
        self.prev.tableWidget.item(self.modify_index,4).setText(id_data)
        self.prev.tableWidget.item(self.modify_index,5).setText(class_data)
        self.prev.tableWidget.item(self.modify_index,6).setText(input_data)
        self.close()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    def initXpathData(self):
        if isinstance(self.modify_index,int):
            xpath_data = (self.prev.tableWidget.item(self.modify_index,1).text() if self.prev.tableWidget.item(self.modify_index,1) else '')
            id_data = (self.prev.tableWidget.item(self.modify_index,4).text() if self.prev.tableWidget.item(self.modify_index,4) else '')
            class_data = (self.prev.tableWidget.item(self.modify_index,5).text() if self.prev.tableWidget.item(self.modify_index,5) else '')
            input_data = (self.prev.tableWidget.item(self.modify_index,6).text() if self.prev.tableWidget.item(self.modify_index,6) else '')
            self.lineEdit.setText(xpath_data)
            self.lineEdit_2.setText(id_data)
            self.lineEdit_3.setText(class_data)
            self.lineEdit_4.setText(input_data)
