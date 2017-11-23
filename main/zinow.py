# -*- coding: utf-8 -*-

'''
Created on 2017年11月10日

@author: zhang.meng
Zinows System
'''

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QMenu,QInputDialog,QAbstractItemView,QWidget,QTreeWidgetItem
from PyQt5.QtCore import Qt,pyqtSlot,QUrl,QByteArray
from PyQt5.Qt import QTableWidgetItem, QVariant
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWebKit import QWebSettings

import utils.auto_test3_image_rc
from lxml import etree
import sys,os,sqlite3,json,codecs,time,re,requests,functools



from main.Ui_zinows import Ui_MainWindow
from main.modifyConfig import ModifyDialog
from login.login import LoginDialog
from utils.table_init import InitTable
from utils.optionWeb import RequestsTable,Manager,MyPage
from utils.my_js import MyJs
from utils.ie_js import IeJs
from f2b2f.handle_chrome_web import Listen_to_web
from main.addCoffee import AddCoffeeDialog
from main.ipConfig import IpConfigDialog
from main.modifyXPath import ModifyXpathDialog
from play.playBack import RecordingPlayBack
from utils.settings import Setting

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from selenium import webdriver

_translate = QtCore.QCoreApplication.translate


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.bananaIndex = 1
        self.tabWidget.removeTab(0)
        
        self.tableSelectValuesList = Setting.tableSelectValuesList
        
        #初始化用户
        self.readyToExport = []
        self.my_custom_process_store = []
        self.dbpath = InitTable.dbpath
        self.initCurrentUser()
        
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[QWidget].connect(self.on_signalMapper_mapped)
        
        
        self.showLoadingGif()
        self.init_socket()
        #为tab绑定关闭信号
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        #为tree绑定右击信号
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.treeWidget.customContextMenuRequested.connect(self.rightClickTree) 
        #初始化数据树
        self.init_tree()
        
        self.initWebView()
        self.initTableView()
        self.initCustomProcess()
        
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        selectedTheme = '&'.join([(self.comboBox.currentText()),(self.comboBox.itemData(self.comboBox.currentIndex()))])
        selectedCoffee = '&'.join([(self.comboBox_2.currentText()),(self.comboBox_2.itemData(self.comboBox_2.currentIndex()))])
        selectedTaskName = (self.lineEdit.text())
        if not selectedTaskName:
            QMessageBox.information(self, u'提示', u'任务不能为空') 
            return
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            #获取当前任务的id
            ids = c.execute(InitTable.get_local_id,(self.configId,self.currentTaskName,self.currentTaskCoffee,self.currentTaskTheme,self.username))
            nowTaskId = [d[0] for d in ids]
            print((u'打桩'))
            #更新数据库中的task任务
            print(u'查询到了id,id: %s,长度为：%s' %(nowTaskId[0],len(nowTaskId)))
            if len(nowTaskId):
                self.currentTaskId = nowTaskId[0]
                print( u'当前任务的id:',self.currentTaskId)
                c.execute(InitTable.update_local_task,(selectedTaskName,selectedCoffee,selectedTheme,self.currentTaskId,))
                conn.commit()
            else:
                raise Exception(u"id不存在，需要新建任务")
        except Exception as a:
            print( u'错误提示：',(a))
            #插入一条任务
            serialName = str(int(time.mktime(time.gmtime())))
            c.execute(InitTable.insert_new_task_data,(serialName,selectedTaskName,selectedCoffee,selectedTheme,self.username,self.configId,))
            self.currentTaskId = c.lastrowid
            self.currentLink = None
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "任务:%s" %selectedTaskName, None))
        finally:
            conn.commit()
            conn.close()            
         
        self.currentTaskName = selectedTaskName
        self.currentTaskCoffee = selectedCoffee
        self.currentTaskTheme = selectedTheme
        
        #每一次都要更新树的结构
        self.re_inint_tree()
        self.checkInternetAndReplaceButton33()
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        被选中的主题
        """
        text = '&'.join([(self.comboBox.itemText(index)),(self.comboBox.itemData(index))])
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_coffee_combo = c.execute(InitTable.get_local_coffee_exclude_parent_id,(self.configId,(text),self.username))
        self.comboBox_2.clear()
        for cof in my_coffee_combo:
#             print( u'变化了几次',cof[1]
            conff_split = cof[1].split('&')
            self.comboBox_2.addItem(conff_split[0],conff_split[1])

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        将环节设置改为回放
        """
        if self.labels.isHidden():
            myBrowser = [u'谷歌浏览器',u'火狐浏览器',u'IE浏览器']
            browserValue, ok = QInputDialog.getItem(self, u'选择浏览器', u'请选择浏览器', myBrowser,current=0,editable = False)
            if ok:
                try:
                    browserValue = (browserValue)
                    browserIndex = myBrowser.index(browserValue, )
                    internetUrl = self.lineEdit_2.text()
                    internet_addr = (internetUrl)
                    rollBackPlay = RecordingPlayBack(self.tableWidget,internet_addr,browserIndex)
                    rollBackPlay.start()
#                     rollBackPlay.playByTable()
                except Exception as e:
                    QMessageBox.information(self, u'提示', e)
        else:
            QMessageBox.information(self, u'提示', u'请等待页面加载完成！')
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        关闭当前页
        """
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        self.bananaIndex = 1
         
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        关闭当前页
        """
        ok = QMessageBox.question(self, u'关闭', u'要关闭当前页面吗？',QMessageBox.Yes,QMessageBox.No)
        if ok== QMessageBox.Yes:
            self.movie.stop()
            self.labels.setHidden(True)
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.removeRow(0)
            self.bananaIndex = 1
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
            
            now_index =  self.stackedWidget.currentIndex() - 1
            self.stackedWidget.setCurrentIndex(now_index)
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.currentTaskName = None
            
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        录制完成，保存
        """
        if self.tableWidget.rowCount():
            self.saveAllDataToSqlite()
    
    
#     @pyqtSlot(QtWidgets.QWidget)
    def on_signalMapper_mapped(self, comboBox):
        """
        表格首列的下拉菜单数值变化信号，用于弹框与自定义程序的选择
        """
        print( u"row: {0} column: {1} text: {2},index:{3}".format(
            comboBox.row,
            comboBox.column,
            comboBox.currentText(),
            comboBox.currentIndex()
        ))
        if comboBox.currentIndex()==4:
            print( u'恭喜你选到了弹框')
            my_alert_box = [u'接受弹框',u'取消弹框']
            my_alert_equal_box = [u'yes',u'no']
            if len(my_alert_box):
                processValue, ok = QInputDialog.getItem(self, u'选择弹框操作', u'请选择操作', my_alert_box,current=0,editable = False)
                if ok:
                    alertValue = my_alert_equal_box[my_alert_box.index((processValue))]
                    newItem = QTableWidgetItem(alertValue)
                    self.tableWidget.setItem(comboBox.row,1,newItem)
            else:
                QMessageBox.information(self, u'选择自定义程序', u'没有自定义程序可供选择')
        elif comboBox.currentIndex()==5:
            print( u'恭喜你选到了自定义程序')
            if len(self.my_custom_process_store):
                processValue, ok = QInputDialog.getItem(self, u'选择自定义程序', u'请选择', self.my_custom_process_store,current=0,editable = False)
                if ok:
                    processValueList = processValue.split(':')
                    newItem = QTableWidgetItem(processValueList[0])
                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                    self.tableWidget.setItem(comboBox.row,1,newItem)
                    
                    newItem = QTableWidgetItem(processValueList[1])
                    self.tableWidget.setItem(comboBox.row,2,newItem)
            else:
                QMessageBox.information(self, u'选择自定义程序', u'没有自定义程序可供选择')
                
    @pyqtSlot()
    def on_actionSynchronizastion_triggered(self):
        """
        数据同步到远程系统中
        """
        print( u'数据同步')
        if self.configId>0:
            storeExportDatasList = self.exportOrSyncDatas()
            if len(storeExportDatasList):
                syncDataToRemoteSystem = json.dumps(storeExportDatasList)
                headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                syncResult = requests.post(self.syncDataPathStroe,headers=headers,data = syncDataToRemoteSystem)
                if isinstance(syncResult.content,str):
                    syncResultFromRemoteDict = None
                    try:
                        syncResultFromRemote = str(syncResult.content,'utf-8')
                        print("远程版本",syncResultFromRemote)
                        syncResultFromRemoteDict = json.loads(syncResultFromRemote)
                    except Exception as e:
                        syncResultFromRemote=':'.join(syncResultFromRemote.split('='))
                        syncResultFromRemoteDict = json.loads(syncResultFromRemote)
                    if syncResultFromRemoteDict:
                        syncKeys = syncResultFromRemoteDict.keys()
                        if len(syncKeys):
                            QMessageBox.information(self, u'未同步数据：', ';'.join(syncKeys))
                            
                QMessageBox.information(self, u'数据同步', u'数据同步成功')
            else:
                QMessageBox.information(self, u'提示', u'您未选择需要同步的数据')
        else:
            QMessageBox.information(self, u'提示', u'本地用户禁用同步数据')
        
    @pyqtSlot()
    def on_actionExport_triggered(self):
        """
        选定需要导出的task，然后选择此按钮进行导出
        """
        print( u'导出')
        path = QtWidgets.QFileDialog.getSaveFileName(
        self, u'保存文件', '', 'USTC(*.ustc)')
        storeExportDatasList = []
        print(path)
        if len(path)>1 and path[0]:
            with codecs.open(path[0], 'wb',encoding='utf-8') as stream:
                storeExportDatasList = self.exportOrSyncDatas()
                if len(storeExportDatasList):
                    json.dump(storeExportDatasList,stream,ensure_ascii=False)
                    QMessageBox.information(self, u'USTC', u'保存成功')
                else:
                    QMessageBox.information(self, u'提示', u'您未选择需要导出的数据')
    @pyqtSlot()
    def on_actionImport_triggered(self):
        """
        将数据库中的全部数据进行导出
        """
        print( u'导入数据')
        path = QtWidgets.QFileDialog.getOpenFileName(
        self, u'打开文件', '', 'USTC(*.ustc)')
        
        #记录更新的数据
        recodeUpdateData = []
        #记录更新失败的数据
        recodeUpdateFaild = []
        #记录插入的数据
        recodeInsertData = []
        #记录插入失败的数据
        recodeInsertFaild = []
        #未能更新的数据
        recodeCannotUpdate = []
        
        if len(path)>1 and path[0]:
            with codecs.open(path[0], 'rb',encoding='utf-8-sig') as stream:
                readDatas =  stream.readlines()
                print( type(readDatas))
                for taskDatas in readDatas:
                    print(taskDatas)
                    print(type(taskDatas))
                    taskJson = json.loads(taskDatas)
                    print( type(taskJson))
                    
                    recodeUpdateData,recodeInsertData,recodeCannotUpdate = self.importDatasToMySqlite3(taskJson)
            try:
                self.re_inint_tree()
            except Exception as e:
                print(e)
            QMessageBox.information(self, u'提示', u'更新{0}:{1};\n插入{2}:{3};\n未更新{4}:{5}'.format(len(recodeUpdateData),' '.join(recodeUpdateData),len(recodeInsertData),' '.join(recodeInsertData),len(recodeCannotUpdate),' '.join(recodeCannotUpdate))) 
                                
    
    @pyqtSlot()
    def on_actionExit_triggered(self):
        """
        退出此系统
        """
        print( u'退出系统')
        ok = QMessageBox.question(self, u'退出', u'要退出系统是吧？',QMessageBox.Yes,QMessageBox.No)
        if ok== QMessageBox.Yes:
            global fullDriver
            if fullDriver:
                global sched
                sched.shutdown()
                
                fullDriver.quit()
            print(u'全部退出')
            os._exit(0)
    @pyqtSlot()
    def on_actionHandleJs_triggered(self):
        """
        手动执行js
        """
        global fullDriver
        try:
            if fullDriver:
                fullDriver.execute_script(IeJs.js)
            print("手动执行完毕！")
        except Exception as e:
            print(e)
            
    
    @pyqtSlot()
    def on_actionConfig_param_triggered(self):
        """
        用于进行参数配置
        """
        print( u'配置参数')
        self.ipConfigDialog = IpConfigDialog()
        self.ipConfigDialog.show()
        self.ipConfigDialog.closeSystemRequest.connect(self.closeSystemRequest)
    
    def closeSystemRequest(self,yes):
        if yes=="yes":
            global fullDriver
            if fullDriver:
                global sched
                sched.shutdown()
                
                fullDriver.quit()
            print(u'全部退出')
            os._exit(0)
    
    @pyqtSlot()
    def on_actionModify_config_triggered(self):
        """
        用于配置参数的修改
        """
        print( u'修改配置')
        self.modifyDialog = ModifyDialog()
        self.modifyDialog.show()
        self.modifyDialog.closeSystemRequest.connect(self.closeSystemRequest)
        
    
    @pyqtSlot()
    def on_actionModify_local_password_triggered(self):
        """
        用于本地密码的修改
        """
        print( u'修改本地密码')
    
    @pyqtSlot()
    def on_actionShow_all_data_triggered(self):
        """
        用于查看所有的task以及数据
        """
        print( u'查看所有的task数据')
    
    @pyqtSlot()
    def on_actionInfo_triggered(self):
        """
        用于展示系统信息
        """
        print( u'系统信息')
        QMessageBox.aboutQt( self, "PyQt" )
    
    
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemDoubleClicked(self, item, column):
        """
        用于左侧树中的任务被双击后获取xpath的操作
        """
        print( u'数据树中的参数被双击')
        if not item.text(2):
            return
        
        task_coffee = item.parent()
        if task_coffee:
            task_theme = task_coffee.parent()
            task_theme = self.getTopTheme(task_theme)
            if task_theme:
                self.currentTaskCoffee = ('&'.join([(task_coffee.text(0)),(task_coffee.text(1))]))
                self.currentTaskTheme = ('&'.join([(task_theme.text(0)),(task_theme.text(1))]))
                self.currentTaskName = (item.text(0))
                print( self.tabWidget.currentIndex())
                print( u'别找了，我就是任务,主题：%s,类别：%s,任务名：%s' %(self.currentTaskTheme,self.currentTaskCoffee,self.currentTaskName,))
                ok = QMessageBox.Yes
                if self.stackedWidget.currentIndex():
                    ok = QMessageBox.question(self, u'退出', u'要舍弃当前的配置吗？',QMessageBox.Yes,QMessageBox.No)
                if ok== QMessageBox.Yes:
                    self.bananaIndex = 1
                    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:%s" %item.text(0), None))
                    self.tabWidget.setCurrentWidget(self.tab_2)
                    self.tabWidget.setTabEnabled(self.tabWidget.currentIndex(),True)
                    self.stackedWidget.setCurrentIndex(0)
                    self.lineEdit.setText(item.text(0))
                    allThemeItems = ['&'.join([(self.comboBox.itemText(i)),(self.comboBox.itemData(i))]) for i in range(self.comboBox.count())]
                    try:
                        idx_theme = allThemeItems.index('&'.join([(task_theme.text(0)),(task_theme.text(1))]))
                        self.comboBox.setCurrentIndex(idx_theme)
                        
                        conn = sqlite3.connect(self.dbpath)
                        c = conn.cursor()
                        my_coffee_combo = c.execute(InitTable.get_local_coffee_exclude_parent_id,(self.configId,'&'.join([(task_theme.text(0)),(task_theme.text(1))]),self.username))
                        self.comboBox_2.clear()
                        for cof in my_coffee_combo:
                            conf_split = cof[1].split('&')
                            self.comboBox_2.addItem(conf_split[0],conf_split[1])
                        allCoffeeItems = ['&'.join([(self.comboBox_2.itemText(i)),(self.comboBox_2.itemData(i))]) for i in range(self.comboBox_2.count())]
                        idx_coffee = allCoffeeItems.index('&'.join([(task_coffee.text(0)),(task_coffee.text(1))]))
                        self.comboBox_2.setCurrentIndex(idx_coffee)
                    except:
                        print( u'出错了')
                        
                    try:
                        #获取当前任务的id
                        ids = c.execute(InitTable.get_local_id,(self.configId,self.currentTaskName,self.currentTaskCoffee,self.currentTaskTheme,self.username))
                        nowTaskId = [d[0] for d in ids]
                        print( u'打桩')
                        #更新数据库中的task任务
                        print( u'查询到了id,id: %s,长度为：%s' %(nowTaskId[0],len(nowTaskId)))
                        if len(nowTaskId):
                            self.currentTaskId = nowTaskId[0]
                        #查询与任务对应的链接，并填充
                        print( u'当前任务的id:',self.currentTaskId)
                        links = c.execute(InitTable.select_task_link,(self.currentTaskId,))
                        lk = [l[0] for l in links]
                        if len(lk):
                            self.currentLink = lk[0]
                            self.lineEdit_2.setText(lk[0])
                        else:
                            self.currentLink = None
                            self.lineEdit_2.setText('')
                    except Exception as a:
                        print( u'错误提示：',(a))
                        
    def getTopTheme(self,task_theme):
        '''
        获取树的顶层主题
        '''
        tem_task_theme = None
        while task_theme:
            tem_task_theme = task_theme
            task_theme = tem_task_theme.parent()
        return tem_task_theme
    
    @pyqtSlot(float)
    def on_doubleSpinBox_valueChanged(self, p0):
        """
        修改浏览器的显示比例
        """
        self.webView.setZoomFactor(p0)
        
    def initWebView(self):
        '''
        初始化浏览器参数，绑定加载完成信号
        '''
        requests_table = RequestsTable()
        manager = Manager(requests_table)
        page = MyPage()
#         page.setNetworkAccessManager(manager)
        page.mainFrame().loadFinished.connect(self.onDone)
        self.tempMyFrame = []
        page.frameCreated.connect(self.onDone_1)
        self.webView.setPage(page)
#         加载swf文件需要此项设置，很重要
        settings = self.webView.settings()
        
#         所有的settings设置
    
        settings.setAttribute(QWebSettings.LocalStorageDatabaseEnabled,True)
    

    def onDone(self,p0):
        '''
        主窗体加载完成后，执行js
        '''
        print( 'page load finished ',p0)
        if p0:
            print( u'加载完毕')
            self.movie.stop()
            self.labels.setHidden(True)
            frame = self.webView.page().mainFrame()
            frame.evaluateJavaScript((MyJs.js_2))
            frame.evaluateJavaScript((MyJs.js))
#             frame.evaluateJavaScript(('location.href = "https://www.baidu.com/";'))
        if not p0:
            print( u'加载失败')
            QMessageBox.information(self, u'提示', u'对不起，加载失败！') 
            
    def onDone_1(self,createdFrame):
        '''
        iframe窗体创建时，为iframe窗体绑定加载完成信号
        '''
        if (createdFrame.frameName())==u'abcdefg':
            return
        
        if createdFrame not in self.tempMyFrame:
            self.tempMyFrame.append(createdFrame)
            createdFrame.loadFinished.connect(functools.partial(self.onDone_2, createdFrame))
    
    def onDone_2(self,createdFrame,p0):
        '''
        iframe窗体加载完成后，执行js
        '''
        if p0:
            self.movie.stop()
            self.labels.setHidden(True)
            createdFrame.evaluateJavaScript((MyJs.js))
    
    def initTableView(self):
        '''
        初始化表格设置
        '''
        listsHorizontalHeaderItem = [u'操作',u'xpath',u'提取到的数据',u'iframe序号',u'标签的id',u'标签的class',u'标签的name',u'iframe的类型',u'iframe`s Indexs']
        self.tableWidget.setColumnCount(len(listsHorizontalHeaderItem))
        for index in range(self.tableWidget.columnCount()):
            self.tableWidget.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(listsHorizontalHeaderItem[index]))
        print( self.tableWidget.width())
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,350)
        self.tableWidget.setColumnWidth(2,200)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(7,100)
        self.tableWidget.setColumnWidth(8,100)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
        
        self.tableWidget.setColumnHidden(4,True)
        self.tableWidget.setColumnHidden(5,True)
        self.tableWidget.setColumnHidden(6,True)

    def init_socket(self):
        '''
        初始化前段js监听
        '''
        self.listenToWeb = Listen_to_web(self)
        self.listenToWeb.rowPositionChangeTo.connect(self.addColboxToTableView)
        self.listenToWeb.rowPositionChangeToSecond.connect(self.addColboxToTableView_2)
        self.listenToWeb.rowPositionChangeToThird.connect(self.addColboxToTableView_3)
        self.listenToWeb.start()
        
    def addColboxToTableView(self,rowPosition):
        pass
        
    def addColboxToTableView_2(self,listRow):
        '''
        表格首列插入数据
        '''
        print( listRow)
        combobox = QtWidgets.QComboBox()
        combobox.currentIndexChanged.connect(self.signalMapper.map)
        
        for item in self.tableSelectValuesList:
            combobox.addItem(item)
        
        rowXpath =  listRow[2]
        if rowXpath:
            if rowXpath==u'input':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'输入'))
            elif rowXpath==u'a':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'span':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'button':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'img':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'submit':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'select':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'输入'))
            elif rowXpath==u'textarea':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'输入'))
            elif rowXpath==u'click':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            elif rowXpath==u'li':
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'单击'))
            else:
                combobox.setCurrentIndex(self.tableSelectValuesList.index(u'变量'))
        
        combobox.row = listRow[0]
        combobox.column = listRow[1]
        
        self.tableWidget.setCellWidget(listRow[0],listRow[1],combobox)
        self.signalMapper.setMapping(combobox, combobox)
    
    def addColboxToTableView_3(self,rowPosition,temWebData,scrollYes):
        '''
        表格其他列插入数据
        '''
        newItem = QTableWidgetItem(temWebData.get('elementXPath',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,1,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementValue',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,2,newItem)
        
        changeIframeValue = temWebData.get('elementIframe',u'-1')
        newItem = QTableWidgetItem(changeIframeValue)
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,3,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementId',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,4,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementClass',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,5,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementInput',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,6,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementIframeType',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,7,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementIframeIndex',u''))
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,8,newItem)
        
        if scrollYes:
            print( u'指定到的行：',rowPosition)
            self.tableWidget.setFocus()
            self.tableWidget.selectRow(rowPosition)
            self.tableWidget.scrollToItem(self.tableWidget.item(rowPosition, 1), QAbstractItemView.PositionAtCenter)
        
#         if changeIframeValue.endswith(u'2'):
#             
#             print( (self.webView.page().mainFrame().toHtml())
    
    def showLoadingGif(self):
        '''
        页面加载时的gif图初始化
        '''
        self.labels = QtWidgets.QLabel('', self)
        self.labels.setGeometry(self.width()/2,self.height()/2,130,130)
        self.labels.setStyleSheet(("background-color: rgb(255,255,255,0.2);"))
        self.movie = QtGui.QMovie(r":/image/images/1.gif",QByteArray(),self.labels)
        self.labels.setMovie(self.movie)
        
    def showContextMenu(self,pos):
        '''
        表格元素的右击信号
        '''
        print( u'右键单击')
        row_num_list = list(index.row() for index in self.tableWidget.selectedIndexes())
        if len(row_num_list):
            row_num = row_num_list[0]
            row_num_list = set(row_num_list)
            row_num_list = list(row_num_list)
            row_num_list.sort()
            row_num_list.reverse()
            print( row_num_list)
            menu = QMenu()
            item1 = menu.addAction(u"删除")
            item2 = menu.addAction(u"查看｜修改")
            item3 = menu.addAction(u"本行前插入")
            item4 = menu.addAction(u"本行后插入")
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item1:
                ok = QMessageBox.question(self, u'删除', u'要删除我？',QMessageBox.Yes,QMessageBox.No)
                if ok== QMessageBox.Yes:
                    for remove_index in row_num_list:
                        print( remove_index)
                        self.tableWidget.removeRow(remove_index)
                    for row in range(self.tableWidget.rowCount()):
                        if row >= row_num_list[len(row_num_list)-1]:
                            self.tableWidget.cellWidget(row,0).row = row
                        
            if action == item2:
                try:
                    if (self.tableWidget.cellWidget(row_num_list[0],0).currentText()):
                        self.modifyXpathDialog =  ModifyXpathDialog(self,modify_index=row_num_list[0])
                        self.modifyXpathDialog.show()
                except Exception as e:
                    pass
            if action == item3:
                self.beaforeOrAfterInsert(row_num_list[0])
            if action == item4:
                self.beaforeOrAfterInsert(row_num_list[0]+1)
            
    
    def beaforeOrAfterInsert(self,row_num):
        '''
        表格中插入一行
        '''
        self.tableWidget.insertRow(row_num)
                
        self.insertNewTableRow(row_num)
        
        newItem = QTableWidgetItem()
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,1,newItem)
        
        newItem = QTableWidgetItem()
        self.tableWidget.setItem(row_num,2,newItem)
        
        newItem = QTableWidgetItem()
        self.tableWidget.setItem(row_num,3,newItem)
        
        newItem = QTableWidgetItem()
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,4,newItem)
        
        newItem = QTableWidgetItem()
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,5,newItem)
        
        newItem = QTableWidgetItem()
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,6,newItem)
        
        newItem = QTableWidgetItem()
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,7,newItem)
        newItem = QTableWidgetItem()
#         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(row_num,7,newItem)
        
        self.tableWidget.setCurrentCell(row_num,1)
#                 更新插入行下面的每第一个的row的值
        for row in range(self.tableWidget.rowCount()):
            if row > (row_num):
                self.tableWidget.cellWidget(row,0).row = row
                        
    def closeTab (self, currentIndex):
        ''' 
        为tab绑定关闭信号，下标为0，不能关闭，备用
        '''
        currentQWidget = self.tabWidget.widget(currentIndex)
        if currentIndex==0:
            ok = QMessageBox.question(self, u'关闭', u'要关闭当前页面吗？',QMessageBox.Yes,QMessageBox.No)
            if ok== QMessageBox.Yes:
                for row in range(self.tableWidget.rowCount()):
                    self.tableWidget.removeRow(0)
                self.bananaIndex = 1
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
                
                now_index =  self.stackedWidget.currentIndex() - 1
                self.stackedWidget.setCurrentIndex(now_index)
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                self.currentTaskName = None
            return
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
        self.tabWidget.setTabEnabled(currentIndex,False)

    def rightClickTree(self,pos):
        '''
        主题与类别树区域的右击信号
        '''
        menu = QMenu()
        if self.configId > -1:
            return;
        item1 = menu.addAction(u"添加主题") 
        item2 = menu.addAction(u"添加类别")
        action = menu.exec_(self.treeWidget.mapToGlobal(pos))
        if action == item1:
            text, ok = QtWidgets.QInputDialog.getText(self, u'添加',
            u'请输入添加的主题:')
            if ok and text:
                addThemeText = '&'.join([str(text),'0'])
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                c.execute(InitTable.add_new_theme,((addThemeText),self.username,self.configId))
                conn.commit()
                conn.close()
                QMessageBox.information(self, u'提示', u'添加主题成功')
                self.re_inint_tree(needFlush=True)
            else:
                QMessageBox.information(self, u'提示', u'添加主题失败')
        if action == item2:
            addCoffeeDialog = AddCoffeeDialog(self)
            addCoffeeDialog.show()
            addCoffeeDialog.exec_()
            self.re_inint_tree(needFlush=True)
            print( u'添加成功')
            
    def init_tree(self):
        '''
        初始化数据树,同时初始化comboBox下拉菜单
        '''
        initParentId = 0
        if self.configId==-1:
            initParentId = -1
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_theme = c.execute(InitTable.get_local_theme,(self.configId,self.username,))
        theme_index = 0
        my_theme_store = [theme for theme in my_theme]
        #清空树、下拉菜单
        self.treeWidget.clear()
#         topLevelCounts = self.treeWidget.topLevelItemCount()
#         for topIndex in range(topLevelCounts):
#             topItem = self.treeWidget.topLevelItem(0)
#             self.treeWidget.removeItemWidget(topItem,0)
#             childCounts = topItem.childCount()
#             for childIndex in range(childCounts):
#                 topItem.removeChild(topItem.child[0])
#             self.treeWidget.remove()
        
        self.treeWidget.setColumnCount(3)
        self.treeWidget.hideColumn(1)
        self.treeWidget.hideColumn(2)
        self.comboBox.clear()
        self.comboBox_2.clear()
        print(my_theme_store)
        for itheme in my_theme_store:
            itheme_split = itheme[1].split('&')
#             print(dir(self.comboBox))
            self.comboBox.addItem(itheme_split[0],QVariant(itheme_split[1]))
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setText(0,(itheme_split[0]))
            item_0.setText(1,(itheme_split[1]))
            item_0.setFlags(item_0.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
 
             
            my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],initParentId))
            my_coffee_store = [coffee for coffee in my_coffee]
             
            for icoffee in my_coffee_store:
                icoffee_split = icoffee[1].split('&')
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0, (icoffee_split[0]))
                item_1.setText(1, (icoffee_split[1]))
                item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                 
                my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
                my_task_store = [task for task in my_task]
                     
                for itask in my_task_store:
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
                 
                #循环处理多级树
                self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1)
            theme_index += 1
        conn.commit()
        conn.close()
        self.treeWidget.itemChanged.connect (self.handleChanged)
         
        self.treeWidget.expandToDepth(1)
        
    def initHandleCoffeeTree(self,itheme,parentCoffeeId,items,addMoreCoffee=False):
        '''
        循环处理多级树
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],parentCoffeeId))
        my_coffee_store = [coffee for coffee in my_coffee]
        
        for icoffee in my_coffee_store:
            icoffee_split = icoffee[1].split('&')
            if addMoreCoffee:
                self.comboBox_2.addItem(icoffee_split[0],icoffee_split[1])
            item_1 = QtWidgets.QTreeWidgetItem(items)
            item_1.setText(0, (icoffee_split[0]))
            item_1.setText(1, (icoffee_split[1]))
            item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
            my_task_store = [task for task in my_task]
            for itask in my_task_store:
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
            #循环处理多级树
            self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1,addMoreCoffee=addMoreCoffee)
    
    @pyqtSlot(QTreeWidgetItem,int)
    def handleChanged(self, item, column):
        '''
        树中元素选中信号
        '''
        if item.checkState(column) == QtCore.Qt.Checked:
            try:
                self.readyToExport.index(item)
            except Exception as e:
                self.readyToExport.append(item)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            try:
                self.readyToExport.remove(item)
            except Exception as e:
                pass

    def initCurrentUser(self):
        '''
        初始化当前用户信息
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            userInfos = c.execute(InitTable.get_start_user_info)
            for user in userInfos:
#                 print( u'用户：{0}，参数ID:{1}'.format(user[0],user[1])
#                 print(type(user[0]))
#                 print(user[0])
                self.username = user[0]
                self.configId = -1
                if user[1]:
                    self.configId = user[1]
#                 print( type(user[0]),user[0]
#                 print( type(self.configId),self.configId
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
        
        #根据configId判断是否需要到远程去更新数据
        if self.configId > 0:
            self.getRemoteConfigInfo()
            #查询对应的configId获取相应的远程配置
#             print( self.configId
            headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
            user_json = {'username':self.username, 'zicada':'2.0'}
            syncByUser = requests.post(self.syncByUserPathStroe,headers=headers,data = json.dumps(user_json))
            syncUserResult = str(syncByUser.content,'utf-8')
            print( u'版本同步：',syncUserResult)
            syncByUserData = json.loads(syncUserResult)
            if isinstance(syncByUserData,list):
            #对获取到的流水号和版本进行校验
                sendToRemoteBySerial = self.checkSerialNoAndVersion(syncByUserData)
                if sendToRemoteBySerial:
                    login = requests.post(self.syncBySerialPathStroe,headers=headers,data = json.dumps(sendToRemoteBySerial))
                    needSyncResult = str(login.content,'utf-8')
                    print( u'流水号同步：',needSyncResult)
                    needSyncDatas = json.loads(needSyncResult)
                    if isinstance(needSyncDatas,list) and len(needSyncDatas):
#                         print( type(needSyncDatas)
                        self.importDatasToMySqlite3(needSyncDatas)
                        
    def checkSerialNoAndVersion(self,syncByUserData):
        '''
        检查任务流水号和版本信息
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(self.configId,self.username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        conn.commit()
        conn.close()
        needSyncSerial = []
        for userData in syncByUserData:
            print( userData['serialNo'])
            print( userData['version'])
            try:
                serialIndex = tempSerial.index(userData['serialNo'])
                print( serialIndex)
                if isinstance(serialIndex,int):
                    serialAndVersion = temAllSerialAndVerisons[serialIndex]
                    #判断版本号是否高于本系统
                    if not serialAndVersion[2] or (isinstance(userData['version'],int) and (userData['version'] > serialAndVersion[2])):
                        print( u'删除原有的任务和数据，分别插入任务和数据')
                        needSyncSerial.append({"version":userData['version'],"serialNo":userData['serialNo']})
                        
            except Exception as e:
                print( e)
                print( u'任务不存在，直接插入任务和数据')
                needSyncSerial.append({"version":userData['version'],"serialNo":userData['serialNo']})
        
        if len(needSyncSerial):
            return {'username':self.username,'taskInfo':needSyncSerial}
        
    def importDatasToMySqlite3(self,taskJson):
        '''
        系统中导入数据方法
        '''
        tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial = self.getThemeAndCoffeeAndTaskAndXpath()
        
        #记录更新的数据
        recodeUpdateData = []
        #记录更新失败的数据
        recodeUpdateFaild = []
        #记录插入的数据
        recodeInsertData = []
        #记录插入失败的数据
        recodeInsertFaild = []
        #未能更新的数据
        recodeCannotUpdate = []
        
        for everyTask in taskJson:
            remoteThemeName = '&'.join([everyTask['themeName'],str(everyTask['themeId'])])
            remoteCoffeeName = '&'.join([everyTask['coffeeName'],str(everyTask['coffeeId'])])
            #判断是否需要插入或更新任务以及数据
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            try:
                print('版本号',everyTask['serialNo'])
                if not everyTask['serialNo']:
                    everyTask['serialNo'] = str(int(time.mktime(time.gmtime())))
                    time.sleep(1)
                serialIndex = tempSerial.index(everyTask['serialNo'])
#                 print( serialIndex
                if isinstance(serialIndex,int):
                    serialAndVersion = temAllSerialAndVerisons[serialIndex]
                    print( len(serialAndVersion))
                    #判断版本号是否高于本系统
#                     print( everyTask['version'] ,serialAndVersion[2]
                    if not serialAndVersion[2] or (isinstance(everyTask['version'],int) and (everyTask['version'] > serialAndVersion[2])):
                        print( u'删除原有的任务和数据，分别插入任务和数据')
                        c.execute(InitTable.deleteTaskById,(serialAndVersion[0],))
                        c.execute(InitTable.deleteXpathByTaskId,(serialAndVersion[0],))
#                                     (null,serialName,version,taskName,coffeeName,themeName,username,1,null,taskType
                        c.execute(InitTable.import_insert_new_task_data,(everyTask['serialNo'],everyTask['version'],everyTask['taskName'],remoteCoffeeName,remoteThemeName,self.username,self.configId,))
                        taskId = c.lastrowid
                        c.execute(InitTable.insert_new_xpath_data,(taskId,everyTask['xpath']['taskLink'],(json.dumps(everyTask['xpath']['xpathJson'])),))
                        recodeUpdateData.append(everyTask['taskName'])
                    else:
                        recodeCannotUpdate.append(everyTask['taskName'])
                
            except Exception as e:
                print( e)
                print( u'任务不存在，直接插入任务和数据')
                print( type(self.configId))
                c.execute(InitTable.import_insert_new_task_data,(everyTask['serialNo'],everyTask['version'],everyTask['taskName'],remoteCoffeeName,remoteThemeName,self.username,self.configId,))
                taskId = c.lastrowid
                c.execute(InitTable.insert_new_xpath_data,(taskId,everyTask['xpath']['taskLink'],(json.dumps(everyTask['xpath']['xpathJson'])),))
                tempSerial.append(everyTask['serialNo'])
                recodeInsertData.append(everyTask['taskName'])
            finally:
                conn.commit()
                conn.close()
             
        return recodeUpdateData,recodeInsertData,recodeCannotUpdate
        
    def getThemeAndCoffeeAndTaskAndXpath(self):
        '''
        获取任务信息
        '''
        #先获取所有的主题
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allThemeNames = c.execute(InitTable.get_all_theme_name,(self.configId,self.username,))
        tempAllThemeNames = [themeName[0] for themeName in allThemeNames]
        
        #获取所有的类别和主题
        allThemeAndCoffeeNames = c.execute(InitTable.get_all_theme_and_coffee_name,(self.configId,self.username,))
        tempAllThemeAndCoffeeNames = [[themeAndCoffeeName[0],themeAndCoffeeName[1]] for themeAndCoffeeName in allThemeAndCoffeeNames]
        
        #获取所有的流水号和版本号
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(self.configId,self.username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        
        conn.commit()
        conn.close()
        return   tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial
        
    def getRemoteConfigInfo(self):
        '''
        获取远程配置信息
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            RemoteConfigInfo = c.execute(InitTable.select_config_by_id,(self.configId,))
            currentRemoteConfig = [[info[1],info[2],info[3],info[4],info[5]] for info in RemoteConfigInfo]
            if len(currentRemoteConfig):
#                 print( currentRemoteConfig[0]
                self.systemNameStroe,\
                self.loginPathStroe,\
                self.syncByUserPathStroe,\
                self.syncBySerialPathStroe,\
                self.syncDataPathStroe = currentRemoteConfig[0][0],\
                                        currentRemoteConfig[0][1].encode('utf-8'),\
                                        currentRemoteConfig[0][2].encode('utf-8'),\
                                        currentRemoteConfig[0][3].encode('utf-8'),\
                                        currentRemoteConfig[0][4].encode('utf-8')
#             print( type(self.loginPathStroe)
#             print( self.loginPathStroe
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()

    def exportOrSyncDatas(self):
        '''
        导出数据方法
        '''
        exportTaskId = []
        storeExportDatasList = []
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            for item in self.readyToExport:
                if item.text(2):
                    task_coffee = item.parent()
                    if task_coffee:
                        task_theme = task_coffee.parent()
                        task_theme = self.getTopTheme(task_theme)
                        if task_theme:
                            print( item.text(2))
                            exportTaskId.append(int(item.text(2)))
            for nid in exportTaskId:
                needExportData = c.execute(InitTable.get_need_task_and_data,(nid,))
                for da in needExportData:
                    lsDa = list(da)
                    '''
                    t.id,t.serialName,t.version,t.taskName,t.coffeeName,t.themeName,t.username,t.status,t.configId,t.taskType,x.id,x.taskLink,x.linkJson,x.fieldJson,x.pageJson,x.status,x.needSetLogin
                    '''
                    tempExportDatasDict = {'id':lsDa[0],'serialNo':lsDa[1],'version':lsDa[2],'taskName':lsDa[3],'coffeeId':int(lsDa[4].split('&')[1]),'coffeeName':lsDa[4].split('&')[0],'themeId':int(lsDa[5].split('&')[1]),'themeName':lsDa[5].split('&')[0],'username':lsDa[6],'status':lsDa[7],'configId':lsDa[8],'xpath':{'id':lsDa[9],'taskId':lsDa[10],'taskLink':lsDa[11],'xpathJson':json.loads(lsDa[12]),'status':lsDa[13]},'taskType':3}
                    storeExportDatasList.append(tempExportDatasDict)
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
        return storeExportDatasList
    
    def addMoreItemToTableWidget(self):
        '''
        当列表中有大于等于两条数据时就讲后续的列表自动补齐
        '''
        countItem = self.tableWidget.rowCount()
        if countItem >= 2:
            tableXpath_1 = (self.tableWidget.item(countItem-1,1).text())
            tableXpath_2 = (self.tableWidget.item(countItem-2,1).text())
            if not tableXpath_1 or not tableXpath_2:
                return
            
            selectedFieldIndex = self.tableWidget.cellWidget(countItem-1,0).currentIndex()
            tableXpath_list_1 = tableXpath_1.split('/')
            tableXpath_list_2 = tableXpath_2.split('/')
            
            if len(tableXpath_list_1)==len(tableXpath_list_2):
                for i in range(len(tableXpath_list_1)):
                    if not (tableXpath_list_1[i]==tableXpath_list_2[i]):
                        print( i)
                        path_num_str1 =  re.findall(r'\d+',tableXpath_list_1[i])
                        path_num_str2 =  re.findall(r'\d+',tableXpath_list_2[i])
                        if len(path_num_str1) and len(path_num_str2):
                            path_num1 = int(path_num_str1[0])
                            path_num2 = int(path_num_str2[0])
                            increase_num = path_num1
                            if path_num2>path_num1:
                                increase_num = path_num2
                            new_linkXpath_list = tableXpath_list_1
                            increase_num = increase_num+1
                            frame = self.webView.page().currentFrame()
                            selectors = etree.HTML((frame.toHtml()))
                            while increase_num:
                                new_position_str = re.sub('[\d]+',str(increase_num),new_linkXpath_list[i])
                                new_linkXpath_list[i] = new_position_str
                                createdXpath =  '/'.join(new_linkXpath_list)
                                print( createdXpath)
                                content = selectors.xpath(createdXpath)
                                if len(content):
                                    resultContent =  ''.join(content[0].xpath('string(.)').replace('\n','').split())
                                    
                                    rowPosition = self.tableWidget.rowCount()
                                    print( type(rowPosition))
                                    self.tableWidget.insertRow(rowPosition)
                                    
                                    self.insertNewTableRow(rowPosition,currentColumnNum=selectedFieldIndex)
                                    
                                    newItem = QTableWidgetItem((createdXpath))
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,1,newItem)
                                    
                                    newItem = QTableWidgetItem(resultContent)
                                    self.tableWidget.setItem(rowPosition,2,newItem)
                                    
                                    newItem = QTableWidgetItem()
                                    self.tableWidget.setItem(int(rowPosition),3,newItem)
                                else:
                                    break
                                increase_num = increase_num + 1
                        break
                    
    def checkInternetAndReplaceButton33(self):
        '''
        创建任务后检查填入的地址信息
        '''
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
            
        internetUrl = self.lineEdit_2.text()
        internet_addr = (internetUrl)
        if internet_addr.startswith(u'http://') or internet_addr.startswith(u'https://'):
            self.internet_addr = internet_addr
            now_index =  self.stackedWidget.currentIndex() + 1
            self.stackedWidget.setCurrentIndex(now_index)
            self.movie.start()
            if self.labels.isHidden():
                self.labels.setHidden(False)
            #如果任务已经存在，并且链接没有变化，那么就将数据库的数据填充到list中
            
            if self.currentLink and self.currentLink==internet_addr:
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                try:
                    print( u'查询本id所有的数据插入到table中')
                    jsonLinks = c.execute(InitTable.select_task_link_json,(self.currentTaskId,))
                    for links in jsonLinks:
                        linksLoad = json.loads(links[0])
                        for strawberryData in linksLoad:
                            rowPosition = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(rowPosition)
                            
                            #操作xpath的方式
                            combobox = QtWidgets.QComboBox()
                            combobox.currentIndexChanged.connect(self.signalMapper.map)
                            for item in self.tableSelectValuesList:
                                combobox.addItem(item)
                            
                            combobox.row = int(rowPosition)
                            combobox.column = 0
                            
                            allCoffeeItems = [(combobox.itemText(i)) for i in range(combobox.count())]
                            idx_coffee = allCoffeeItems.index(strawberryData['fieldName'])
                            self.insertNewTableRow(int(rowPosition),currentColumnNum=idx_coffee)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldXpath',''))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,1,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldValue',''))
                            self.tableWidget.setItem(rowPosition,2,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldExtension',''))
                            self.tableWidget.setItem(rowPosition,3,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldId',''))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,4,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldClass',''))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,5,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldInput',''))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,6,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldIframeType',''))
                            self.tableWidget.setItem(rowPosition,7,newItem)
                            
                            newItem = QTableWidgetItem(strawberryData.get('fieldIframeIndex',''))
                            self.tableWidget.setItem(rowPosition,8,newItem)
                            
                except Exception as e:
                    print( e)
                finally:
                    conn.commit()
                    conn.close()    
            self.webView.load(QUrl(internetUrl))
            
        else:
            QMessageBox.information(self, u'我需要网址', u'请输入正确格式的网址：http://或者https://')
            
    def re_inint_tree(self,needFlush = False):
        '''
        再次初始化主题与类别树
        '''
        initParentId = 0
        if self.configId==-1:
            initParentId = -1
        self.readyToExport.clear()
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_theme = c.execute(InitTable.get_local_theme,(self.configId,self.username,))
        theme_index = 0
        my_theme_store = [theme for theme in my_theme]
        self.username = my_theme_store[0][2]
        #清空树、下拉菜单
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(3)
        self.treeWidget.hideColumn(1)
        self.treeWidget.hideColumn(2)
        if needFlush:
            self.comboBox.clear()
            self.comboBox_2.clear()
        for itheme in my_theme_store:
            print( theme_index)
            print( itheme[1])
            itheme_split = itheme[1].split('&')
            if needFlush:
                self.comboBox.addItem(itheme_split[0],QVariant(itheme_split[1]))
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setText(0,itheme_split[0])
            item_0.setText(1,itheme_split[1])
            item_0.setFlags(item_0.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            
            my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],initParentId))
            my_coffee_store = [coffee for coffee in my_coffee]
                
            for icoffee in my_coffee_store:
                print( icoffee[1])
                icoffee_split = icoffee[1].split('&')
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0, (icoffee_split[0]))
                item_1.setText(1, (icoffee_split[1]))
                item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                
                my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
                my_task_store = [task for task in my_task]
                    
                for itask in my_task_store:
                    print( itask[1])
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
                #循环处理多级树
                self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1)
                
        
        conn.commit()
        conn.close()
        
        try:
            for parentTheme in self.treeWidget.findItems(self.currentTaskTheme.split('&')[0], QtCore.Qt.MatchFixedString):
                parentTheme.setExpanded(True)
                for indexCoffee in range( parentTheme.childCount()):
                    parentTheme.child(indexCoffee).setExpanded(True)
        except Exception as e:
            print( e)
            self.treeWidget.expandToDepth(1)
        
        self.treeWidget.itemChanged.connect(self.handleChanged)
        
    def saveAllDataToSqlite(self):
        '''
        保存所有数据到数据库
        '''
        
        internetAddr = (self.lineEdit_2.text())
        
        rows = self.tableWidget.rowCount()
        have_get = False
        have_input = False
        for user_index in  range(rows):
            try:
                if (self.tableWidget.cellWidget(user_index,0).currentText())==u'输入验证码':
                    have_input = True
                
                if (self.tableWidget.cellWidget(user_index,0).currentText())==u'获取验证码':
                    have_get = True
            except Exception as e:
                print( e)
        
        if have_get:
            if have_input:
                pass
            else:
                QMessageBox.information(self, u'提示', u'获取验证码与输入验证码未配对！')
                return
        
        tableWidgetData = []
        for row_index in range(rows):
            print( row_index)
            try:
                tableWidgetDic = {'stepNum':"step-%03d" %(row_index+1),\
                                  'fieldName':(self.tableWidget.cellWidget(row_index,0).currentText()),\
                                  'fieldXpath':(self.tableWidget.item(row_index,1).text() if self.tableWidget.item(row_index,1) else ''),\
                                  'fieldValue':(self.tableWidget.item(row_index,2).text() if self.tableWidget.item(row_index,2) else ''),\
                                  'fieldExtension':(self.tableWidget.item(row_index,3).text() if self.tableWidget.item(row_index,3) else ''),\
                                  'fieldId':(self.tableWidget.item(row_index,4).text() if self.tableWidget.item(row_index,4) else ''),\
                                  'fieldClass':(self.tableWidget.item(row_index,5).text() if self.tableWidget.item(row_index,5) else ''),\
                                  'fieldInput':(self.tableWidget.item(row_index,6).text() if self.tableWidget.item(row_index,6) else ''),\
                                  'fieldIframeType':(self.tableWidget.item(row_index,7).text() if self.tableWidget.item(row_index,7) else ''),\
                                  'fieldIframeIndex':(self.tableWidget.item(row_index,8).text() if self.tableWidget.item(row_index,8) else '')}
                tableWidgetData.append(tableWidgetDic)
            except Exception as e:
                print( e)
                print( row_index)
                print( type(self.tableWidget.cellWidget(row_index,0)))
            
        xpathJson = json.dumps(tableWidgetData)
        
        
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        #获取本任务的版本
        my_versions = c.execute(InitTable.get_local_version,(self.currentTaskId,))
        vers = [ver[0] for ver in my_versions]
        version = 1
        if len(vers) and vers[0]:
            version = vers[0] + 1
        conn.commit()
        conn.close()
        #更新任务版本
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.update_local_version,(version,self.currentTaskId,))
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
            
        #原数据失效设置
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.update_local_xpath,(self.currentTaskId,))
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
            
        #插入新的xpath数据
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.insert_new_xpath_data,(self.currentTaskId,internetAddr,xpathJson,))
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
        
        QMessageBox.information(self, u'提示', u'保存成功')
#         成功保存表格中的数据后关闭当前页，回到任务创建页面
        now_index =  self.stackedWidget.currentIndex() - 1
        self.stackedWidget.setCurrentIndex(now_index)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.currentTaskName = None
    
    def insertNewTableRow(self,rowNum,currentColumnNum=0):
        '''
        表格中插入新的一行
        '''
        combobox_1 = QtWidgets.QComboBox()
        combobox_1.currentIndexChanged.connect(self.signalMapper.map)
        for item in self.tableSelectValuesList:
            combobox_1.addItem(item)
        
        combobox_1.row = rowNum
        combobox_1.column = 0
        
        combobox_1.setCurrentIndex(currentColumnNum)
        self.tableWidget.setCellWidget(rowNum,0,combobox_1)
        self.signalMapper.setMapping(combobox_1, combobox_1)
    
    def initCustomProcess(self):
        '''
                    初始化自定义程序
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            my_custom_process = c.execute(InitTable.select_custom_process,(self.username,self.configId,))
            self.my_custom_process_store = [':'.join([str(process[0]),process[1]]) for process in my_custom_process]
            print( self.my_custom_process_store)
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()

class MovieSplashScreen(QtWidgets.QSplashScreen):
    '''
    系统启动后gif图设置
    '''
    def __init__(self, movie, parent = None):
        movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(movie.frameRect().size())
        
        QtWidgets.QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)
    
    def showEvent(self, event):
        self.movie.start()
    
    def hideEvent(self, event):
        self.movie.stop()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
    
    def sizeHint(self):
        return self.movie.scaledSize()

def job(fullDriver):
    try:
        global fullHandles
        print (u'定时任务')
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        checkForm = fullDriver.execute_script(IeJs.js_0)
        print(checkForm)
        if checkForm:
            fullDriver.execute_script(IeJs.js_1)
        tempHandles = fullDriver.window_handles
        for wid in tempHandles:
            try:
                fullHandles.index(wid)
            except Exception as e:
                fullDriver.switch_to_window(wid)
                fullHandles = tempHandles
                reCheckForm = fullDriver.execute_script(IeJs.js_0)
                print(checkForm)
                if reCheckForm:
                    fullDriver.execute_script(IeJs.js_1)
                break
    except Exception as e:
        print (u'报错')
        try:
            fullDriver.switch_to_window(fullDriver.window_handles[0])
        except Exception as e:
            print (u'还是错')

def setScheduler(fullDriver):
    sched = BackgroundScheduler()
    sched.add_job(job, trigger = IntervalTrigger(seconds=10),args=[fullDriver])
    sched.start()
    return sched

   
def configSystem():
    '''
    系统启动入口
    '''
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseDesktopOpenGL,15)
    app.setAttribute(Qt.AA_UseOpenGLES,16)
    app.setAttribute(Qt.AA_UseSoftwareOpenGL,17)
    app.setAttribute(Qt.AA_ShareOpenGLContexts,18)
    login = LoginDialog()
    if login.exec_():
        movie = QtGui.QMovie(":/image/images/hadppy_newyear.gif")
        splash = MovieSplashScreen(movie)
        splash.show()
        
        start = time.time()
        while movie.state() == QtGui.QMovie.Running and time.time() < start + 10:
            app.processEvents()
        
        splash.close()
        ui = MainWindow()
        ui.show()
        try:
            global fullDriver
            fullDriver = None
#             fullDriver = webdriver.Ie()
#             fullDriver = webdriver.Chrome()
#             fullDriver.get("https://www.baidu.com")
#             fullDriver.get("http://192.168.80.144:8080/bwp/login")
#             fullHandles = fullDriver.window_handles
#             global sched
#             sched = setScheduler(fullDriver)
        except Exception as e:
            fullDriver = None
            QMessageBox.warning(ui,"警示","无法打开本操作系统IE浏览器，请检查IE浏览器的相关配置！")
        if not app.exec_():
            if fullDriver:
                sched.shutdown()
                
                fullDriver.quit()
            print(u'全部退出')
            os._exit(0)
#         os._exit(app.exec_())