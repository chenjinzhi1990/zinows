#!-*- coding:utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''
from main.zinow import configSystem

if __name__=="__main__":
    '''
    系统由此初始化
    '''
    try:
        configSystem()
    except Exception as e:
        print(e)
