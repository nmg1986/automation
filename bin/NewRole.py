#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import sqlite3

import gtk

import variables


class NewRole(gtk.Window):
	def __init__(self,liststore,father):
		gtk.Window.__init__(self)

                self.father=father
		self.index=0
		self.liststore=liststore
		self.set_keep_above(True)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_decorated(False)
		self.set_size_request(355,220)
		self.set_resizable(False)

		self.vbox=gtk.VBox()	
		self.add(self.vbox)
		

		fixed=gtk.Fixed()
		self.vbox.pack_start(fixed,False,False,0)
                
                label,self.hostname=self.create_hostname()
                fixed.put(label,5,5)
                fixed.put(self.hostname,5,25)
                
		label,self.port=self.create_port()
		fixed.put(label,248,5)
		fixed.put(self.port,248,25)
                
		label,self.username=self.create_username()
		fixed.put(label,5,60)
		fixed.put(self.username,5,80)
                
		label,self.password=self.create_password()
		fixed.put(label,248,60)
		fixed.put(self.password,248,80)
                
		label,self.role=self.create_role()
		fixed.put(label,5,120)
		fixed.put(self.role,5,140)
                
		label,self.soft=self.create_soft()
		fixed.put(label,200,120)
        	fixed.put(self.soft,200,140)

		quitbtn,okbtn=self.create_button()
		fixed.put(quitbtn,5,180)
		fixed.put(okbtn,248,180)
                self.father.set_sensitive(False)
        	self.show_all()
	def create_hostname(self):
		label=gtk.Label('主机IP')
		hostname=gtk.Entry()
		hostname.set_has_frame(False)
		hostname.set_size_request(100,25)

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
		username.set_size_request(100,25)

		return (label,username)
	def create_password(self):
		label=gtk.Label('密码')
		password=gtk.Entry()
		password.set_has_frame(False)
		password.set_size_request(100,25)
		password.set_visibility(False)
		password.set_invisible_char('*')

		return label,password
	def create_role(self):

		label=gtk.Label('角色')
		self.role_entry=gtk.Entry()
		self.role_entry.set_size_request(150,25)
		self.role_entry.set_has_frame(False)
		self.role_entry.connect('grab-focus',self.show_role)
		return label,self.role_entry

	def create_soft(self):

		label=gtk.Label('软件包')
		self.soft=gtk.Entry()
		self.soft.set_size_request(150,25)
		self.soft.set_has_frame(False)
		self.soft.connect('grab-focus',self.show_soft)

		return label,self.soft

	def create_button(self):
        	quitb=gtk.Button('退出')
        	quitb.set_size_request(100,30)
        	quitb.set_relief(gtk.RELIEF_NONE)
        	quitb.connect('clicked',self.quit)
        	okbt=gtk.Button('确定')
        	okbt.set_size_request(100,30)
        	okbt.set_relief(gtk.RELIEF_NONE)
        	okbt.connect('clicked',self.add_server)
		#okbt.set_properties('relief',gtk.RELIEF_HALF)

		return quitb,okbt
	def show_role(self,entry):
		x,y=entry.get_parent_window().get_position()
		popup=gtk.Window(gtk.WINDOW_POPUP)
		popup.move(x+5,y+165)
		treeview=gtk.TreeView()
		treeview.set_size_request(200,-1)
		treeview.set_headers_visible(False)
		treeview.set_rules_hint(True)
		treeview.set_hover_selection(True)
		treeview.connect('button-press-event',self.selectRole,popup)
		popup.add(treeview)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("角色",rendererText,text=0)
		treeview.append_column(column)

		model=gtk.ListStore(str)
            	for item in variables.SERVER_TYPE:
			model.append([item,])

		treeview.set_model(model)
		popup.show_all()
		entry.connect('focus-out-event',self.hide_treeview,popup)
	def show_soft(self,entry):
		x,y=entry.get_parent_window().get_position()
		popup=gtk.Window(gtk.WINDOW_POPUP)
		popup.set_keep_above(True)
		popup.move(x+245,y+165)
		popup.set_decorated(False)
		treeview=gtk.TreeView()
		treeview.set_size_request(200,-1)
		treeview.set_headers_visible(False)
		treeview.set_rules_hint(True)
		treeview.connect('button-press-event',self.selectSoft,popup)
		popup.add(treeview)

		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("软件包",rendererText,text=0)
		treeview.append_column(column)

		model=gtk.ListStore(str)
		files=os.listdir(variables.PKG_DIR)
		files.sort()
		for file in files:
			if file == 'list.server' or file == 'list.client' or file== 'server.list':
				continue
			else:
				model.append([file,])
		treeview.set_model(model)
		popup.show_all()
		entry.connect('focus-out-event',self.hide_treeview,popup)

	def selectRole(self,widget,event,popup):
                if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
                    treeselection = widget.get_selection()
                    (model, iter) = treeselection.get_selected()
                    role = model.get_value(iter, 0)
                    self.role.set_text(role)
                    popup.destroy()
                    return 
        def selectSoft(self,widget,event,popup):
                if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
                    treeselection = widget.get_selection()
                    (model, iter) = treeselection.get_selected()
                    role = model.get_value(iter, 0)
                    self.soft.set_text(role)
                    popup.destroy()
                    return
	def hide_treeview(self,entry,event,popup):
		popup.destroy()

	def quit(self,widget):
		self.window.destroy()
		self.father.set_sensitive(True)
		
	def add_server(self,widget):
		hostname=self.hostname.get_text()
		port=self.port.get_text()
		username=self.username.get_text()
		password=self.password.get_text()
		role=self.role.get_text()
		soft=self.soft.get_text()
		self.liststore.append([False,hostname,role,0,soft,0,'准备部署','--'])
		self.saveTodb([hostname,port,username,password,role,soft])
		self.window.destroy()
		self.father.set_sensitive(True)
	def saveTodb(self,data):
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
			create table if not exists server
			(hostname text,port text,username text,password text,role text,package text,type text,progress text,status text)
			'''
		)
		c.execute('''
			insert into server(hostname,port,username,password,role,package,type,progress,status)
			values("%s","%s","%s","%s","%s","%s","%s","%s","%s")
			''' % (data[0],data[1],data[2],data[3],data[4],data[5],'0','准备部署','0')
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
