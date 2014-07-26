#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import sqlite3

import gtk

import variables


class NewConfig(gtk.Window):
	def __init__(self,liststore):
		gtk.Window.__init__(self)

		self.index=0
		self.liststore=liststore
		self.set_keep_above(True)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_decorated(False)
		self.set_size_request(450,180)
		self.set_resizable(False)

		self.vbox=gtk.VBox()	
		self.add(self.vbox)
		

		fixed=gtk.Fixed()
		self.vbox.pack_start(fixed,False,False,0)
                
                label,self.hostname=self.create_hostname()
                fixed.put(label,5,5)
                fixed.put(self.hostname,5,25)
                
		label,self.port=self.create_port()
		fixed.put(label,345,5)
		fixed.put(self.port,345,25)
                
		label,self.username=self.create_username()
		fixed.put(label,5,60)
		fixed.put(self.username,5,80)
                
		label,self.password=self.create_password()
		fixed.put(label,345,60)
		fixed.put(self.password,345,80)
                
		quitbtn,okbtn=self.create_button()
		fixed.put(quitbtn,5,140)
		fixed.put(okbtn,345,140)

        	self.show_all()
	def create_hostname(self):
		label=gtk.Label('主机IP')
		hostname=gtk.Entry()
		hostname.set_has_frame(False)
		hostname.set_size_request(180,25)

		return (label,hostname)
	def create_port(self):
		label=gtk.Label('端口')
		port=gtk.Entry()
		port.set_has_frame(False)
		port.set_size_request(100,25)

		return (label,port)
	def create_username(self):
		label=gtk.Label('用户名')
		username=gtk.Entry()
		username.set_has_frame(False)
		username.set_size_request(120,25)

		return (label,username)
	def create_password(self):
		label=gtk.Label('密码')
		password=gtk.Entry()
		password.set_has_frame(False)
		password.set_size_request(100,25)
		password.set_visibility(False)
		password.set_invisible_char('*')

		return label,password
	
	def create_button(self):
        	quitb=gtk.Button('退出')
        	quitb.set_size_request(100,30)
        	quitb.connect('clicked',self.quit)
        	okbt=gtk.Button('确定')
        	okbt.set_size_request(100,30)
        	okbt.connect('clicked',self.add_server)
		okbt.set_properties('relief',gtk.RELIEF_HALF)

		return quitb,okbt
	

	def hide_treeview(self,entry,event,popup):
		popup.destroy()

	def quit(self,widget):
		self.window.destroy()	
		
	def add_server(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()

		self.saveTodb([hostname,port,username,password])
		self.liststore.append([False,hostname,'--','--','--','--','打开终端',1])
		
		self.window.destroy()
	def saveTodb(self,data):
		conn=sqlite3.connect('db/config.db')
		c=conn.cursor()
		c.execute('''
			create table if not exists config
			(hostname text,port text,username text,
			password text，hostname2 text,runlevel text,
			sshport text,rootpasswd,text)
			'''
		)
		c.execute('''
			insert into config(hostname,port,username,password)
			values("%s","%s","%s","%s")
			''' % (data[0],data[1],data[2],data[3])
				)
		conn.commit()
		conn.close()
	def msg(self,text):
		md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,
								gtk.BUTTONS_OK,text)
		md.run()
		md.destroy()
	def IsValid(self,text):
		list=text.split('.')
		if len(list) != 4 :
			return False
		else:
			for i in list:
				if i.isdigit() and 0 <= int(i) <= 255:
					continue
				else:
					return False
		return True
