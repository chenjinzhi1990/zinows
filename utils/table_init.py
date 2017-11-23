#!-*- coding:utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

import time

class InitTable(object):
    dbpath = 'xpath.db'
    
    zm_user = '''CREATE TABLE zm_user (
          id integer PRIMARY KEY AUTOINCREMENT,
          username varchar(30) DEFAULT NULL,
          password varchar(30) DEFAULT NULL,
          isLocal boolean DEFAULT 0,
          configId integer DEFAULT NULL,
          status boolean DEFAULT 0
        )'''
    
    zm_config = '''CREATE TABLE zm_config (
          id integer PRIMARY KEY AUTOINCREMENT,
          systemName varchar(50) DEFAULT NULL,
          loginPath varchar(80) DEFAULT NULL,
          syncByUserPath varchar(80) DEFAULT NULL,
          syncBySerialPath varchar(80) DEFAULT NULL,
          syncDataPath varchar(80) DEFAULT NULL,
          status boolean DEFAULT 0
        )'''
    
    zm_theme = '''CREATE TABLE zm_theme (
              id integer PRIMARY KEY AUTOINCREMENT,
              themeName varchar(30) DEFAULT NULL,
              username varchar(30) DEFAULT NULL,
              status boolean DEFAULT 0,
              configId integer DEFAULT NULL
            )'''
    zm_coffee = '''CREATE TABLE zm_coffee (
                  id integer PRIMARY KEY AUTOINCREMENT,
                  coffeeName varchar(30) DEFAULT NULL,
                  themeName varchar(30) DEFAULT NULL,
                  username varchar(30) DEFAULT NULL,
                  status boolean DEFAULT 0,
                  configId integer DEFAULT NULL,
                  parentCoffeeId integer DEFAULT NULL
                )'''
    
    zm_custom_process = '''CREATE TABLE zm_custom_process (
      id integer PRIMARY KEY AUTOINCREMENT,
      customProcessId integer DEFAULT NULL,
      customProcessName varchar(50) DEFAULT NULL,
      username varchar(30) DEFAULT NULL,
      configId integer DEFAULT NULL,
      status boolean DEFAULT 0
    )'''
    
    zm_task = '''CREATE TABLE zm_task (
                      id integer PRIMARY KEY AUTOINCREMENT,
                      serialNo varchar(50) DEFAULT NULL,
                      version integer DEFAULT NULL,
                      taskName varchar(30) DEFAULT NULL,
                      coffeeName varchar(30) DEFAULT NULL,
                      themeName varchar(30) DEFAULT NULL,
                      username varchar(30) DEFAULT NULL,
                      status boolean DEFAULT 0,
                      configId integer DEFAULT NULL
                    )'''
    zm_xpath = '''CREATE TABLE zm_xpath (
                          id integer PRIMARY KEY AUTOINCREMENT,
                          taskId integer DEFAULT NULL,
                          taskLink varchar(50) DEFAULT NULL,
                          xpathJson text DEFAULT NULL,
                          status boolean DEFAULT 0
                        )'''
    zm_user_insert = ''' 
                    insert into zm_user values(null,'admin','admin123',1,-1,0)
                    '''
    
    zm_theme_insert = '''
                    insert into zm_theme values(null,'我的主题&0','admin',1,-1)
                    '''
    zm_coffee_insert = '''
                    insert into zm_coffee values(null,'链接&0','我的主题&0','admin',1,-1,-1)
                    '''
    #测试数据
    serialName = str(int(time.mktime(time.gmtime())))
    zm_task_insert = r'insert into zm_task values(null,?,1,"普元","链接","我的主题","admin",1,null,1)'
                    
    select_local_user = ''' select username,password from zm_user where isLocal=1 '''
    #获取本地用户的主题
    get_local_theme = r'select id,themeName,username from zm_theme where configId=? and status=1 and username=?'
    
    #获取本地用户的类别
    get_local_coffee = r'select id,coffeeName,themeName,username from zm_coffee where configId=? and status=1 and themeName=? and username=? and parentCoffeeId=?'
    #获取本地用户的类别，不需要父类id
    get_local_coffee_exclude_parent_id = r'select id,coffeeName,themeName,username from zm_coffee where configId=? and status=1 and themeName=? and username=?'
    
    #获取本地用户的任务
    get_local_task = r'select id,taskName,coffeeName,themeName,username from zm_task  where configId=? and status=1 and coffeeName=? and  themeName=?  and username=?'
    
    #获取当前任务的id
    get_local_id = r'select id from zm_task where configId=? and status=1 and taskName=? and coffeeName=? and  themeName=?  and username=?'
    
    #更新数据库中的本条任务
    update_local_task = r'update zm_task set taskName=?,coffeeName=?,themeName=? where id=?'
    
    #获取任务的版本
    get_local_version = r'select version from zm_task where id=?'
    
    #更新数据库中的本条任务
    update_local_version = r'update zm_task set version=? where id=?'
    
    #获取任务的所有字段
    get_local_task = r'select id,taskName,coffeeName,themeName,username from zm_task  where configId=? and status=1 and coffeeName=? and  themeName=?  and username=?'
    
    #原有xpath数据失效
    update_local_xpath = r'update zm_xpath set status=0 where taskId=?'
    
    #插入新的xpath数据
    insert_new_xpath_data = r'insert into zm_xpath values(null,?,?,?,1)'
    
    #插入新的task数据
    insert_new_task_data = r'insert into zm_task values(null,?,null,?,?,?,?,1,?)'
    
    #查询与任务对应的链接
    select_task_link = r'select taskLink from zm_xpath where status=1 and taskId=?'
    
    #查询与任务对应的linkJson
    select_task_link_json = r'select xpathJson from zm_xpath where status=1 and taskId=?'
    
    #查询与任务对应的fieldJson
    select_task_field_json = r'select fieldJson from zm_xpath where status=1 and taskId=?'
    
    #查询与任务对应的任务类型
    select_task_type = r'select taskType from zm_task where status=1 and id=?'
    
    #查询与任务对应的pageJson
    select_task_page_json = r'select pageJson from zm_xpath where status=1 and taskId=?'
    
    #通过id获取对应任务的数据
    get_need_task_and_data = r'select t.id,t.serialNo,t.version,t.taskName,t.coffeeName,t.themeName,t.username,t.status,t.configId,x.id,x.taskId,x.taskLink,x.xpathJson,x.status  from zm_task t,zm_xpath x where t.status=1 and x.status=1 and t.id=? and t.id=x.taskId'
    
    #添加新的主题
    add_new_theme = r'insert into zm_theme values(null,?,?,1,?)'
    
    #添加新的类别
    add_new_coffee = r'insert into zm_coffee values(null,?,?,?,1,?,-1)'
    
    #获取所有主题的名称
    get_all_theme_name = r'select themeName from zm_theme where configId=? and status=1 and username=?'
    
    #获取所有类别和主题的名称
    get_all_theme_and_coffee_name = r'select themeName,coffeeName,parentCoffeeId from zm_coffee where configId=? and status=1 and username=?'
    
    #获取所有的流水号和版本号
    get_all_serialNum_and_version = r'select id,serialNo,version from zm_task where configId=? and status=1 and username=?'
    
    #根据id删除任务
    deleteTaskById = r'update zm_task set status=0 where id=?'
    
    #根据id删除数据
    deleteXpathByTaskId = r'update zm_xpath set status=0 where taskId=?'
    
    #导入数据时插入新的task数据
    import_insert_new_task_data = r'insert into zm_task values(null,?,?,?,?,?,?,1,?)'
    
    #插入主题
    import_insert_theme = r'insert into zm_theme values(null,?,?,1,?)'
    
    #插入类别
    import_insert_coffee = r'insert into zm_coffee values(null,?,?,?,1,?,?)'
    
    #插入远程配置
    insert_remote_config = r'insert into zm_config values(null,?,?,?,?,?,?)'
    
    #获取远程的配置
    select_all_config = r'select id,systemName,loginPath,syncByUserPath,syncBySerialPath,syncDataPath,status from zm_config'
    
    #获取远程中状态为1的系统
    select_remote_status_active = r'select id from zm_config where status=1'
    
#     用户表中的其他数据全部数据状态全部更新为0，不可用状态
    update_user_forbidden_status = r'update zm_user set status=0 where status=1'
    
    #插入一条用户记录
    insert_new_user_recorde = r'insert into zm_user values(null,?,?,0,?,1)'
    
    #得到初始化的用户
    get_start_user_info = r'select username,configId from zm_user where status=1'
    
    #将本地用户状态置为1
    set_local_user_active = r'update zm_user set status=1 where isLocal=1'
    
    #将非本地用户置为0
    set_other_user_forbidden = r'update zm_user set status=0 where isLocal=0'
    
    #设置远程配置状态全部为0
    update_remote_status_forbidden = r'update zm_config set status=0 where status=1'
    
    #设置置顶id的远程配置状态为1
    update_remote_selected_id_active = r'update zm_config set status=1 where id=?'
    
    #根据ID获取远程的配置
    select_config_by_id = r'select id,systemName,loginPath,syncByUserPath,syncBySerialPath,syncDataPath,status from zm_config where id=?'
    
    #查询与任务对应的loginJson
    select_task_login_json = r'select loginJson from zm_xpath where status=1 and taskId=?'
    
    #修改远程配置
    update_remote_config = r'update zm_config set systemName=?,loginPath=?,syncByUserPath=?,syncBySerialPath=?,syncDataPath=? where id=?'
    
    #插入新的自定义程序
    insert_custom_process = r'insert into zm_custom_process values(null,?,?,?,?,1)'

    #更新自定义程序
    update_custom_process_status = r'update zm_custom_process set status=0 where username=? and configId=?'

    #查找自定义程序
    select_custom_process = r'select customProcessId,customProcessName from zm_custom_process where username=? and configId=? and status=1'
