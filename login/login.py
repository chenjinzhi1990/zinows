# -*- coding: utf-8 -*-

'''
Created on 2017年11月10日

@author: zhang.meng
'''
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QDialog,QMessageBox,QLineEdit,QApplication
from PyQt5.QtCore import pyqtSlot

from login.Ui_login import Ui_Dialog
from utils.table_init import InitTable

import utils.auto_test3_image_rc
import base64
import sys,sqlite3,json,ast,requests,types

class LoginDialog(QDialog, Ui_Dialog):
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
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.dbpath = InitTable.dbpath
        self.createUsertable()
        self.isLocal = 1
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.isLocal:
            print( u'本地密码登录')
            self.localPasswordLogin()
#             self.accept()
        else:
            print( u'远程密码登录')
            self.remotePasswordLogin()
#             self.close()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.isLocal = 1
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.isLocal = 0
    
    def createUsertable(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        # create zm_user tables
        try:
            c.execute(InitTable.zm_user)
            # save the changes
            conn.commit()
            c.execute(InitTable.zm_user_insert)
        except sqlite3.OperationalError as o:
            print( o)
        finally:
            conn.commit()
            # close the connection with the database
            conn.close()
    
    def localPasswordLogin(self):
        '''
        本地登录的账号和密码进行验证，验证成功的话就初始化数据库，否则，让用户重新登录。
        '''
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print(username)
        print(type(username))
        if username and password:
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            users = c.execute(InitTable.select_local_user)
            for row in users:
                self.user=row
#             print( self.user
            conn.commit()
            conn.close()
            if username==self.user[0]:
                if password==self.user[1]:
                    conn = sqlite3.connect(self.dbpath)
                    c = conn.cursor()
                    try:
                        c.execute(InitTable.set_local_user_active)
                        c.execute(InitTable.set_other_user_forbidden)
                    except Exception as e:
                        print( e)
                    finally:
                        conn.commit()
                        # close the connection with the database
                        conn.close()
                    
                    #初始化数据库
                    self.initDatabase()
                    self.accept()
                    print( u'本地密码登录')
                else:
                    QMessageBox.critical(self, 'Error', 'Password error')
            else:
                QMessageBox.critical(self, 'Error', 'Username error')
        else:
            QMessageBox.critical(self, 'Error', 'Username or password not null')


    def initDatabase(self):
        '''
        创建默认的配置表、主题表、类别表、任务表、数据表，并初始化本地用户的默认的主题、类别
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        # create zm_user tables
        try:
            c.execute(InitTable.zm_config)
            c.execute(InitTable.zm_theme)
            c.execute(InitTable.zm_coffee)
            c.execute(InitTable.zm_task)
            c.execute(InitTable.zm_xpath)
            c.execute(InitTable.zm_custom_process)
            conn.commit()
            c.execute(InitTable.zm_theme_insert )
            c.execute(InitTable.zm_coffee_insert)
#             c.execute(InitTable.zm_task_insert,(InitTable.serialName,))
            conn.commit()
        except sqlite3.OperationalError as o:
            print( o)
        finally:
            conn.commit()
            # close the connection with the database
            conn.close()
    
    
    def remotePasswordLogin(self):
        '''
        远程密码登录
        '''
        username = (self.lineEdit.text())
        password = (self.lineEdit_2.text()).encode('utf-8')
        if username and password:
            password = base64.encodestring(password)
#             print( username,password
            #获取当前config表中状态为1的远程系统
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            try:
                remoteSystemInfo = c.execute(InitTable.select_remote_status_active)
                remoteSystemId = [info[0] for info in remoteSystemInfo]
            except Exception as e:
                QMessageBox.critical(self, 'Error', u'远程用户不可用')
                return
            finally:
                conn.commit()
                conn.close()
            if len(remoteSystemId):
            #此处要向远程发送请求，返回结果值
#                 print( type(username)
#                 print( type(password)
                self.getRemoteConfigInfo(remoteSystemId[0])
                headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                payload = {'username':username,'password':str(password,'utf-8')}
                try:
                    self.loginPathStroe = str(self.loginPathStroe,'utf-8')
                    print( self.loginPathStroe)
                    login = requests.post(self.loginPathStroe,headers=headers,data = json.dumps(payload),timeout=5)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', u'连接超时')
                    return
                print(type(login))
                print(type(login.content))
                result = json.loads(str(login.content,'utf-8'))
                print( '--------------------------------------------------')
#                 print( result
                print( '--------------------------------------------------')
                if result:
                    #远程验证成功,将用户表中的其他数据全部数据状态全部更新为0，不可用状态
                    conn = sqlite3.connect(self.dbpath)
                    c = conn.cursor()
                    try:
                        c.execute(InitTable.update_user_forbidden_status)
                        #插入一条用户记录
                        c.execute(InitTable.insert_new_user_recorde,((username),(password),remoteSystemId[0]))
                        c.execute(InitTable.update_custom_process_status,((username),remoteSystemId[0]))
                    except Exception as e:
                        print( e)
                    finally:
                        conn.commit()
                        conn.close()
                    self.initThemeAndCoffee(result,username,remoteSystemId[0])
                    self.accept()
                else:
                    QMessageBox.critical(self, 'Error', u'远程账号或密码不可用')
            else:
                QMessageBox.critical(self, 'Error', u'远程用户不可用')
                return
            
        else:
            QMessageBox.critical(self, 'Error', 'Username or password not null')
            
    def getRemoteConfigInfo(self,remoteSystemId):
        print( u'获取远程的配置')
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            RemoteConfigInfo = c.execute(InitTable.select_config_by_id,(remoteSystemId,))
            currentRemoteConfig = [[info[1],info[2],info[3],info[4],info[5]] for info in RemoteConfigInfo]
            if len(currentRemoteConfig):
#                 print( currentRemoteConfig[0]
                self.systemNameStroe,self.loginPathStroe = currentRemoteConfig[0][0],currentRemoteConfig[0][1].encode('utf-8')
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
            
    def getThemeAndCoffeeAndTaskAndXpath(self,username,configId):
#         print( type(username)
#         print( type(configId)
#         print( username
#         print( configId
        #先获取所有的主题
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allThemeNames = c.execute(InitTable.get_all_theme_name,(configId,username,))
        tempAllThemeNames = [themeName[0] for themeName in allThemeNames]
        
        #获取所有的类别和主题
        allThemeAndCoffeeNames = c.execute(InitTable.get_all_theme_and_coffee_name,(configId,username,))
        tempAllThemeAndCoffeeNames = [[themeAndCoffeeName[0],themeAndCoffeeName[1],themeAndCoffeeName[2]] for themeAndCoffeeName in allThemeAndCoffeeNames]
        
        #获取所有的流水号和版本号
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(configId,username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        
        conn.commit()
        conn.close()
        return   tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial
    
    def initThemeAndCoffee(self,themeAndCoffeeListAndProcess,username,configId):
        print( themeAndCoffeeListAndProcess)
        themeAndCoffeeList = themeAndCoffeeListAndProcess.get('syncThemeAndCoffee')
        processList = themeAndCoffeeListAndProcess.get('syncProcessName')
        tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial = self.getThemeAndCoffeeAndTaskAndXpath(username,configId)
        insertThemeList = []
        insertCoffeeList = []
        for themeAndCoffeeItem in themeAndCoffeeList:
#             print( type(themeAndCoffeeItem)
#             print( themeAndCoffeeItem
            remoteThemeName = '&'.join([themeAndCoffeeItem['themeName'],str(themeAndCoffeeItem['themeId'])])
            remoteCoffeeName = '&'.join([themeAndCoffeeItem['coffeeName'],str(themeAndCoffeeItem['coffeeId'])])
            parentCoffeeId = themeAndCoffeeItem['parentCoffeeId']
            #判断是否需要插入主题
            try:
                themeIndex = tempAllThemeNames.index(remoteThemeName)
                if isinstance(themeIndex,int):
                    pass
#                     print( u'本主题已经存在',remoteThemeName
            except Exception as e:
#                 print( u'本主题不存在',remoteThemeName
                insertThemeList.append((remoteThemeName,username,configId))
                tempAllThemeNames.append(remoteThemeName)
             
            #判读是否需要插入类别
            checkCoffeeAndTheme = [1 for themeAndCoffee in tempAllThemeAndCoffeeNames if themeAndCoffee[0]==remoteThemeName and themeAndCoffee[1]== remoteCoffeeName and themeAndCoffee[2]==parentCoffeeId]
            if not len(checkCoffeeAndTheme):
#                 print( u'需要插入类别',remoteThemeName,remoteCoffeeName
                insertCoffeeList.append((remoteCoffeeName,remoteThemeName,username,configId,parentCoffeeId,))
                tempAllThemeAndCoffeeNames.append([remoteThemeName,remoteCoffeeName,parentCoffeeId])
        
        insertProcessList = []
        for processItem in processList:
            insertProcessList.append((processItem.get('processId'),processItem.get('processName'),username,configId,))
        
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        #批量插入主题
        try:
            if len(insertThemeList):
                c.executemany(InitTable.import_insert_theme,insertThemeList)
        except Exception as e:
            print( e)
        #批量插入类别
        try:
            if len(insertCoffeeList):
                c.executemany(InitTable.import_insert_coffee,insertCoffeeList)
        except Exception as e:
            print( e)
        #批量插入自定义程序信息
#         print( insertProcessList
        try:
            if len(insertProcessList):
                c.executemany(InitTable.insert_custom_process,insertProcessList)
        except Exception as e:
            print( e)
        finally:
            conn.commit()
            conn.close()
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoginDialog()
    ui.show()
    sys.exit(app.exec_())