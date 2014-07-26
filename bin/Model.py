#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gtk
import os
from ConfigParser import SafeConfigParser
import sqlite3

def CreateSoftModel():
	liststore=gtk.ListStore(bool,str,str,str,str,str,str,int)
	if not os.path.isfile('package/list.server'):
		parser=SafeConfigParser()
		parser.read('package/list.client')
		for section in parser.sections():
			name=section
			desc=parser.get(section,'description').strip("'")
			size=parser.get(section,'size').strip("'")
			version=parser.get(section,'version').strip("'")
			liststore.append([False,name,desc,version,version,size,'未知',0])
	
	return liststore

def CreateConfigModel():
	liststore=gtk.ListStore(bool,str,str,str,str,str,str,int)
	if  os.path.isfile('db/config.db'):
		conn=sqlite3.connect('db/config.db')
		cursor=conn.cursor()
		cursor.execute('select hostname,port,username,password,hostname2,runlevel,sshport,rootpasswd from config') 
		while True:
			data=cursor.fetchone()
			if data is None:
				break
			hostname=str(data[0])
			port=str(data[1])
			username=str(data[2])
			password=str(data[3])
			hostname2=str(data[4])
			runlevel=str(data[5])
			sshport=str(data[6])
			rootpasswd=str(data[7])
			liststore.append([False,hostname,hostname2,runlevel,sshport,rootpasswd,'terminal',1])
		cursor.close()
		conn.close()
			
	return liststore
def CreateServerModel():
	liststore=gtk.ListStore(bool,str,str,str,str,str,str,str)
	if os.path.isfile('db/server.db'):
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute('select hostname,role,type,progress,status from server') 
		while True:
			data=cursor.fetchone()
			if data is None:
				break
			hostname=str(data[0])
			index=str(data[1])
			role=str(data[1])
			flag=str(data[2])
			if flag == '0':
				soft='默认软件包'
			else:
				soft='自定义软件包'
			progress=str(data[3])
			status=str(data[4])	
			if status == '0':
				status='--'
			else:
				status='√' 
			liststore.append([False,hostname,role,index,soft,flag,progress,status])
	
		cursor.close()
		conn.close()
	return liststore

def CreateMonitModel():
	liststore=gtk.ListStore(bool,str,str,str,str,str,str,str,str)
	if os.path.isfile('db/monit.db'):
		conn=sqlite3.connect('db/monit.db')
		cursor=conn.cursor()
		cursor.execute('select hostname from monit') 
		while True:
			data=cursor.fetchone()
			if data is None:
				break
			hostname=str(data[0])
			
			liststore.append([False,hostname,'--','--','--','--','--','--','--'])
		cursor.close()
		conn.close()
	return liststore


