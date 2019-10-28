# -*- coding: utf-8 -*-

'''
Created on 2017年11月10日

@author: zhang.meng
'''

from PyQt5.QtWidgets import QDialog,QInputDialog,QMessageBox
from PyQt5.QtCore import pyqtSlot

from main.Ui_addCoffee import Ui_Dialog
import sqlite3
from utils.table_init import InitTable

class AddCoffeeDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self,prev, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.dbpath = InitTable.dbpath
        self.prev = prev
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_theme = c.execute(InitTable.get_local_theme,(self.prev.configId,self.prev.username,))
        themes = []
        for theme in my_theme:
            themes.append(theme[1])
        result, ok = QInputDialog.getItem(self, u'选择主题', u'请选择主题', themes)
        if ok:
            self.lineEdit.setText(result)
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        haveStoreTheme = (self.lineEdit.text())
        newCoffee = ('&'.join([str(self.lineEdit_2.text()),'0']))
        if haveStoreTheme and newCoffee:
            self.close()
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            # iterate through the records
            c.execute(InitTable.add_new_coffee,(newCoffee,haveStoreTheme,self.prev.username,self.prev.configId))
            conn.commit()
            conn.close()
            QMessageBox.information(self, u'提示', u'添加类别成功')
            self.close()
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
