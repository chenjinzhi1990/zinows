# -*- coding: utf-8 -*-

'''
Created on 2017年11月10日

@author: zhang.meng
'''
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QDialog,QMessageBox,QApplication
from PyQt5.QtCore import pyqtSlot

from main.Ui_config import Ui_Dialog
import utils.auto_test3_image_rc
from utils.table_init import InitTable
import sys,sqlite3,os


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/image/images/logo.png"))
        self.dbpath = InitTable.dbpath
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        print( u'确定')
        systemName = (self.lineEdit_8.text())
        logPath = (self.lineEdit_5.text())
        syncByUserPath = (self.lineEdit_4.text())
        syncBySerialPath = (self.lineEdit_6.text())
        syncDataPath = (self.lineEdit_7.text())
        
        print( type(logPath))
        print( u'logPath:{0},syncByUserPath:{1},syncBySerialPath:{2},syncDataPath:{3}'.format(systemName,logPath,syncByUserPath,syncBySerialPath,syncDataPath))
        status = 0
        if self.radioButton_2.isChecked():
            status = 1
        
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        flag = False
        try:
            if logPath and syncByUserPath and syncBySerialPath and syncDataPath:
                if status==1:
                    c.execute(InitTable.update_remote_status_forbidden)
                    conn.commit()
                c.execute(InitTable.insert_remote_config,(systemName,logPath,syncByUserPath,syncBySerialPath,syncDataPath,status))
                flag = True
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
        if flag:
            ok = QMessageBox.question(self, u'退出', u'重新登录后配置生效，是否重新登录？',QMessageBox.Yes,QMessageBox.No)
            if ok== QMessageBox.Yes:
                os._exit(0)
        
        self.close()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print( u'取消')
        self.close()


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    ui = Dialog()
    ui.show()
    sys.exit(app.exec_())
