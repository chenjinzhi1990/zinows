#!-*- coding:utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,threading

class RecordingPlayBack(threading.Thread):
    def __init__(self,currentTable=None,startLink=None,browserIndex=0):
        threading.Thread.__init__(self)
        self.currentTable = currentTable
        self.startLink = startLink
        self.browserIndex = browserIndex
        self.driver = None
        self.tempWindow = None
        self.storeVlaue = dict()
    def run(self):
        self.playByTable()
    
    def getJs(self,xpath):
        return '''
                var evaluator = new XPathEvaluator(); 
                var result = evaluator.evaluate("{0}", document.documentElement, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
                resultValue = result.singleNodeValue;
                resultValue.style.borderWidth = '2px';
                resultValue.style.borderStyle = 'outset';
                resultValue.style.borderColor = '#0099FF';
                '''.format(xpath.replace("\"","'"))
    
    def playByTable(self):
        try:
            if self.browserIndex==0:
                self.driver = webdriver.Chrome()
            elif self.browserIndex==1:
#                     'C:/Program Files/Mozilla Firefox/firefox.exe'
                self.driver = webdriver.Firefox()
            elif self.browserIndex==2:
#                 "C:/Program Files/Internet Explorer/iexplore.exe"
                self.driver = webdriver.Ie()
        except Exception as e:
            print( e)
            raise Exception(u"此浏览器不可用！")
            return
        self.driver.maximize_window()
        time.sleep(2)
        rows = self.currentTable.rowCount()
        try:
            self.driver.get(self.startLink)
            self.driver.implicitly_wait(30)
            self.tempWindow = self.driver.window_handles
            for row_index in range(rows):
                print( row_index)
                fieldName=(self.currentTable.cellWidget(row_index,0).currentText())
                fieldXpath=(self.currentTable.item(row_index,1).text() if self.currentTable.item(row_index,1) else '')
                fieldValue=(self.currentTable.item(row_index,2).text() if self.currentTable.item(row_index,2) else '')
                fieldExtension=(self.currentTable.item(row_index,3).text() if self.currentTable.item(row_index,3) else '')
                fieldId=(self.currentTable.item(row_index,4).text() if self.currentTable.item(row_index,4) else '')
                fieldClass=(self.currentTable.item(row_index,5).text() if self.currentTable.item(row_index,5) else '')
                fieldInput=(self.currentTable.item(row_index,6).text() if self.currentTable.item(row_index,6) else '')
                fieldIframeType = (self.currentTable.item(row_index,7).text() if self.currentTable.item(row_index,7) else '')
#                 print( fieldName,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput
#                 print( type(fieldName)
                
                if fieldExtension==u"-1":
                    self.driver.switch_to.default_content()
                elif fieldExtension:
                    iframeStepOrder = fieldExtension.split(',')
                    iframeStepType = fieldIframeType.split(',')
                    try:
                        self.driver.switch_to.default_content()
                    except Exception as e:
                        print("链接断开了")
                        self.driver.switch_to_window(self.driver.window_handles[0])
                        self.tempWindow = self.driver.window_handles
                    wait = WebDriverWait(self.driver, 30)
                    for typeIndex in range(len(iframeStepType)):
                        if iframeStepType[typeIndex]=='str':
                            print( 'str类型')
                            wait.until(EC.frame_to_be_available_and_switch_to_it(iframeStepOrder[typeIndex]))
                        elif iframeStepType[typeIndex]=='int':
                            wait.until(EC.frame_to_be_available_and_switch_to_it(int(iframeStepOrder[typeIndex])))
                            print( 'int类型')
#                         self.driver.switch_to_frame(ifm)
                
                if fieldName==u'弹框':
                    try:
                        alert = self.driver.switch_to.alert
                        if fieldXpath==u'yes':
                            alert.accept()
                        else:
                            alert.dismiss()
                        continue
                    except Exception as e:
                        print( e)
                
#                 self.checkAlert()
                
                if fieldName==u'变量':
                    variablevalue = self.storeInputValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    self.storeVlaue[str(row_index+1)] = variablevalue
                    time.sleep(2)
                    continue
                
                if fieldName==u'输入':
                    self.inputValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    continue
                
                if fieldName==u'悬停':
                    self.hoverOption(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    continue
                    
                if fieldName==u'单击':
                    self.clickValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    
                    try:
                        for window in self.driver.window_handles:
                            self.tempWindow.index(window)
                    except Exception as e:
                        try:
                            self.driver.switch_to_window(window)
                            self.tempWindow = self.driver.window_handles
                        except Exception as e:
                            try:
                                self.driver.switch_to_window(self.driver.window_handles[0])
                                self.tempWindow = self.driver.window_handles
                            except Exception as e:
                                print (u'还是错')
                    continue
                    
                if fieldName==u'元素':
                    self.elementValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    continue
                
                if fieldName==u'右击':
                    self.rightClickValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    continue
                    
                if fieldName==u'双击':
                    self.doubleClickValue(fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput)
                    time.sleep(2)
                    continue
                
        except Exception as e:
            print( e)
            self.driver.quit()
        finally:
            self.driver.quit()

    def inputValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
        inputs = self.gainElement(fieldXpath,fieldId,fieldClass)
        if fieldValue.startswith('@@@'):
            fieldValue = self.storeVlaue.get(fieldValue[3:],'')
        
        if inputs.tag_name == u'select':
            allOptions = inputs.find_elements_by_tag_name("option")
            for option in allOptions:
                if option.text == fieldValue:
                    option.click()
        else:
            try:
#                 inputs.clear()
#                 inputs.send_keys(fieldValue)
                inputs.send_keys(Keys.CONTROL + "a")
                inputs.send_keys(Keys.DELETE)
                inputs.send_keys(fieldValue)
            except Exception as e:
                print( e)
        
    def submitValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
        submitVal = self.gainElement(fieldXpath,fieldId,fieldClass)
        if submitVal.tag_name==u'input':
            parentForm = submitVal.find_element_by_xpath('..')
            while parentForm.tag_name != u'form':
                parentForm = parentForm.find_element_by_xpath('..')
            try:
                form_target = parentForm.get_attribute('target')
            except:
                form_target = None
            submitVal.submit()
            time.sleep(3)
            return form_target
        elif submitVal.tag_name==u'button' and submitVal.get_attribute('type')==u'button':
            submitVal.click()
            return
        submitVal.submit()
        time.sleep(3)
    
    def clickValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
#         print( self.driver.page_source
        alink = self.gainClickedElement(fieldXpath,fieldId,fieldClass)
        try:
            alink.click()
        except Exception as e:
            self.driver.execute_script("arguments[0].click();", alink)
            print( e)
        

    def elementValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
        try:
            if fieldId:
                element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.ID,fieldId)))
            elif fieldXpath:
                element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,fieldXpath)))
#             self.driver.execute_script(self.getJs(fieldXpath))
        except Exception as e:
            print( e)
        getMyValue = element.text
        print( getMyValue)
        if getMyValue==fieldValue:
            print( u'真是厉害，你找到我了!')
        time.sleep(3)
        
    def hoverOption(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
        hoverEle = self.gainElement(fieldXpath,fieldId,fieldClass)
        
#         self.driver.execute_script(self.getJs(fieldXpath))
        ActionChains(self.driver).move_to_element(hoverEle).perform()
        time.sleep(2)
        
    def checkAlert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception as e:
            print( e)
    
    def rightClickValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
#         print( self.driver.page_source
        right_alink = self.gainClickedElement(fieldXpath,fieldId,fieldClass)
        try:
            ActionChains(self.driver).context_click(right_alink).perform()
            time.sleep(2)
        except Exception as e:
            self.driver.execute_script("arguments[0].contextmenu();", right_alink)
            print( e)
            
    
    def doubleClickValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
#         print( self.driver.page_source
        double_alink = self.gainClickedElement(fieldXpath,fieldId,fieldClass)
        try:
            ActionChains(self.driver).double_click(double_alink).perform()
        except Exception as e:
            self.driver.execute_script("arguments[0].dblclick();", double_alink)
            print( e)
            
    def storeInputValue(self,fieldXpath,fieldValue,fieldExtension,fieldId,fieldClass,fieldInput):
        element_value = self.gainElement(fieldXpath,fieldId,fieldClass)
        try:
            return element_value.text
        except Exception as e:
            return ''
    
    def gainElement(self,fieldXpath,fieldId,fieldClass):
        if fieldId:
            indexCount = 0
            while True and indexCount<2:
                try:
                    element_value = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.ID,fieldId)))
                    break
                except Exception as e:
                    indexCount += 1
        elif fieldXpath:
            indexCount = 0
            while True and indexCount<2:
                try:
                    element_value = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,fieldXpath)))
                    break
                except Exception as e:
                    indexCount += 1
                    self.checkLoopNum(indexCount)
        elif fieldClass:
            indexCount = 0
            while True and indexCount<2:
                try:
                    element_value = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,fieldClass)))
                    break
                except Exception as e:
                    indexCount += 1
                    self.checkLoopNum(indexCount)
#         self.driver.execute_script(self.getJs(fieldXpath))
        return  element_value
    
    def gainClickedElement(self,fieldXpath,fieldId,fieldClass):
        print( u'单击')
        if fieldId:
            indexCount = 0
            while True and indexCount<2:
                try:
                    clicked_element = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.ID,fieldId)))
                    clicked_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.ID,fieldId)))
                    break
                except Exception as e:
                    indexCount += 1
                    self.checkLoopNum(indexCount)
        elif fieldXpath:
            indexCount = 0
            while True and indexCount<2:
                try:
                    clicked_element = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.XPATH,fieldXpath)))
                    clicked_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,fieldXpath)))
                    break
                except Exception as e:
                    indexCount += 1
                    self.checkLoopNum(indexCount)
        elif fieldClass:
            indexCount = 0
            while True and indexCount<2:
                try:
                    clicked_element = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,fieldClass)))
                    clicked_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,fieldClass)))
                    break
                except Exception as e:
                    indexCount += 1
                    self.checkLoopNum(indexCount)
#         self.driver.execute_script(self.getJs(fieldXpath))
        return clicked_element
    
    def checkLoopNum(self,indexCount):
        if indexCount>=2:
            raise Exception(u'找不到元素')
