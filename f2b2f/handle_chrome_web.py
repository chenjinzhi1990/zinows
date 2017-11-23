# -*- coding: utf-8 -*- 
'''
Created on 2017年11月10日

@author: zhang.meng
'''

from wsgiref.simple_server import make_server
from cgi import parse_qs

from utils.settings import Setting

import sys   
from PyQt5.QtCore import QThread,Qt
# from PyQt5.QtGui import QTableWidgetItem,QAbstractItemView
from PyQt5 import QtCore
import urllib.parse

class Listen_to_web(QThread):
    listWidgetAddItem = QtCore.pyqtSignal(dict)
    rowPositionChangeTo = QtCore.pyqtSignal('QString')
    rowPositionChangeToSecond = QtCore.pyqtSignal(list)
    rowPositionChangeToThird = QtCore.pyqtSignal(int,dict,bool)
    
    def __init__(self,pa, parent=None):
        QThread.__init__(self,parent)
        self.pa = pa
#         self.t1.setDaemon(True)
#         self.t1.start()
        print( u'启动线程')
    
    def application(self,environ, start_response):
        print( u'发送请求')
        if environ.get('PATH_INFO', 'no')==Setting.internetPath:
            self.handleFieldAndDataReq(environ)
            
        response_body = 'good afternoon'
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain;charset=utf-8'),]
    
        start_response(status, response_headers)
        return [response_body.encode("utf-8")]
    
    def handleFieldAndDataReq(self,environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        request_body = str(request_body,'utf-8')
        d = parse_qs(str(request_body))
        col_index = 0
        scrollYes = True
        currentMouseseRow = self.pa.tableWidget.currentRow()
        currentRowFirstCellValue = (self.pa.tableWidget.item(currentMouseseRow,1).text() if self.pa.tableWidget.item(currentMouseseRow,1) else '')
        if not currentRowFirstCellValue and currentMouseseRow> -1:
            rowPosition = currentMouseseRow
            scrollYes = False
        else:
            rowPosition = self.pa.tableWidget.rowCount()
            self.pa.tableWidget.insertRow(rowPosition)
#         self.pa.tableWidget.setItem(rowPosition,col_index,QTableWidgetItem(u'字段'))
#         my_column_index = col_index
        col_index += 1
        temWebData = {}
        for k in d:
            try:
                temWebData[k]  = urllib.parse.unquote(d[k][0])
            except Exception as u:
                pass
        self.rowPositionChangeToSecond.emit([rowPosition,0,temWebData.get('elementTag','')])
        
        self.rowPositionChangeToThird.emit(rowPosition,temWebData,scrollYes)
        
#         newItem = QTableWidgetItem(temWebData.get('elementXPath',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,1,newItem)
#         
#         newItem = QTableWidgetItem(temWebData.get('elementValue',u''))
# #         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,2,newItem)
#         
#         self.rowPositionChangeTo.emit(str(rowPosition))
#         
#         newItem = QTableWidgetItem(temWebData.get('elementIframe',u'主窗体'))
# #         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,3,newItem)
#         
#         newItem = QTableWidgetItem(temWebData.get('elementId',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,4,newItem)
#         
#         newItem = QTableWidgetItem(temWebData.get('elementClass',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,5,newItem)
#         
#         newItem = QTableWidgetItem(temWebData.get('elementInput',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.pa.tableWidget.setItem(rowPosition,6,newItem)
        
#         if scrollYes:
#             print( u'指定到的行：',rowPosition
#             self.pa.tableWidget.setFocus()
#             self.pa.tableWidget.selectRow(rowPosition)
#             self.pa.tableWidget.scrollToItem(self.pa.tableWidget.item(rowPosition, 1), QAbstractItemView.PositionAtCenter)
        
        
        
            
#             print( u'字段设置数据：',(d[k][0])
#             print( col_index
#             if col_index==3:
#                 self.rowPositionChangeToSecond.emit([rowPosition,my_column_index,(d[k][0])])
#                 break
#             try:
#                 newItem = QTableWidgetItem((d[k][0]))
#                 newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#                 self.pa.tableWidget.setItem(rowPosition,col_index,newItem)
#             except DecodeError,u:
#                 newItem = QTableWidgetItem((d[k][0].decode('gbk','replace')))
#                 self.pa.tableWidget.setItem(rowPosition,col_index,newItem)
#             col_index += 1
#         self.rowPositionChangeTo.emit(str(rowPosition))
    
    
    
    def start_listen_req(self):
        httpd = make_server('0.0.0.0', 9998, self.application)
        httpd.serve_forever()
        
        print( 'end')
        
    def run(self):
        self.start_listen_req()
        
if __name__=='__main__':
    Listen_to_web()