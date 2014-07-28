#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sqlite3

import gtk

from CellRendererButton import *
from NewConfig import NewConfig
import util
import EditServer
import Model


DEFAULT=0
CUSTOM=1 

class ConfigCenter(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)	

		self.toolbar=self.create_toolbar()
		self.pack_start(self.toolbar,False,False,0)
	
		self.scrolledwindow=self.create_scrolled_window()
		self.pack_start(self.scrolledwindow,True,True,0)
	
		self.treeview=self.create_treeview()
		self.model=self.create_model()
		self.treeview.set_model(self.model)
		self.scrolledwindow.add(self.treeview)

		self.bottom=self.create_bottom()
		self.pack_start(self.bottom,False,False,0)

	def create_toolbar(self):
		toolbar=gtk.Toolbar()
		toolbar.set_style(gtk.TOOLBAR_ICONS)
	
		addtb=gtk.ToolButton(gtk.STOCK_ADD)
		addtb.set_tooltip_text('添加')
		deltb=gtk.ToolButton(gtk.STOCK_REMOVE)
		deltb.set_tooltip_text('删除')
		cleartb=gtk.ToolButton(gtk.STOCK_CLEAR)
		cleartb.set_tooltip_text('清空列表')
		refresh=gtk.ToolButton(gtk.STOCK_REFRESH)
		refresh.set_tooltip_text('刷新')
		info=gtk.ToolButton(gtk.STOCK_INFO)
		info.set_tooltip_text('日志')
		edit=gtk.ToolButton(gtk.STOCK_EDIT)
		edit.set_tooltip_text('编辑')
		prefer=gtk.ToolButton(gtk.STOCK_PREFERENCES)
		prefer.set_tooltip_text('配置')
	       
		toolbar.insert(addtb,0)
		toolbar.insert(deltb,1)
		toolbar.insert(cleartb,2)
		toolbar.insert(refresh,3)
		toolbar.insert(info,4)
		toolbar.insert(edit,5)
		toolbar.insert(prefer,6)
	
		addtb.connect("clicked",self.add_server)
		deltb.connect("clicked",self.delete)
		cleartb.connect("clicked",self.clear)
		refresh.connect("clicked",self.refresh)
		edit.connect('clicked',self.edit)
		prefer.connect('clicked',self.preference)

		return toolbar
	def create_scrolled_window(self):
		scrolledwindow=gtk.ScrolledWindow()
		scrolledwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		scrolledwindow.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)

		return scrolledwindow

	def create_treeview(self):
		treeview=gtk.TreeView()
		treeview.set_headers_visible(True)
		selection=treeview.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
	
		rendererToggle=gtk.CellRendererToggle()
		#rendererToggle.set_activatable(True)
		rendererToggle.connect('toggled',self.toggled,treeview)
		column=gtk.TreeViewColumn(' ',rendererToggle,active=0)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(25)
		treeview.append_column(column)
	
		rendererText=gtk.CellRendererText()
		column=gtk.TreeViewColumn("服务器",rendererText,text=1)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(160)
		treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.set_property("editable",True)
		rendererText.connect("edited",self.cell_edited,2)
		column=gtk.TreeViewColumn("主机名",rendererText,text=2)
		column.set_visible(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(100)
		treeview.append_column(column)
	
		rendererText=gtk.CellRendererText()
		rendererText.set_property("editable",True)
		rendererText.connect("edited",self.cell_edited,3)
		#rendererCombo=gtk.CellRendererCombo()
		column=gtk.TreeViewColumn("运行级别",rendererText,text=3)
		column.set_resizable(True)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(60)
		treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.set_property("editable",True)
		rendererText.connect("edited",self.cell_edited,4)
		column=gtk.TreeViewColumn("SSH端口",rendererText,text=4)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(75)
		treeview.append_column(column)
	
		#rendererText=gtk.CellRendererCombo()
		#column=gtk.TreeViewColumn("",rendererText,text=5)
		#column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		#column.set_resizable(True)
		#column.set_fixed_width(50)
		#treeview.append_column(column)

		#rendererText=gtk.CellRendererText()
		#column=gtk.TreeViewColumn("DNS",rendererText,text=5)
		#column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		#column.set_resizable(True)
		#column.set_fixed_width(50)
		#treeview.append_column(column)

		rendererText=gtk.CellRendererText()
		rendererText.set_property("editable",True)
		rendererText.connect("edited",self.cell_edited,5)
		column=gtk.TreeViewColumn("ROOT密码",rendererText,text=5)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(100)
		treeview.append_column(column)

		rendererButton=CellRendererButton()
		rendererButton.set_fixed_size(30,20)
		rendererButton.connect('clicked',self.open_terminal)
		column=gtk.TreeViewColumn("更多操作",rendererButton,text=6,sensitive=7)
		column.set_alignment(0.5)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(70)
		treeview.append_column(column)
	
		

		

		return treeview
	def create_model(self):
		liststore=Model.CreateConfigModel()
		return liststore

	def create_bottom(self):
		hbox=gtk.HBox(False,3)
		fixed=gtk.Fixed()
		fixed.set_size_request(-1,25)
		choose_button=gtk.CheckButton("全部选中/反选")
		choose_button.connect('toggled',self.choose_all)
		fixed.put(choose_button,0,0)
		hbox.pack_start(fixed,False,False,0)

		fixed=gtk.Fixed()
		check_button=gtk.Button("保存配置")
		check_button.set_size_request(100,25)
		check_button.connect('clicked',self.save_config)
		fixed.put(check_button,0,0)
		hbox.pack_end(fixed,False,False,0)

		return hbox

	def toggled(self,cell,path,treeview):
		model=treeview.get_model()
		model[path][0] = not model[path][0]
		treeview.get_selection().select_path(path)
		return
	def cell_edited(self,renderer,path,text,id):
                treeiter=self.model.get_iter(path)
                self.model.set_value(treeiter,id,text)
                return
	def add_server(self,widget):
		NewConfig(self.model)
		return
	def destroy_add(self,widget,data):
		data.destroy()
		return
	def open_terminal(self,widget):
                pass
	def save_config(self,widget):
		selection=self.treeview.get_selection()
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				treeiter=model.get_iter(path)
				T=util.CONFIG(model,treeiter,self.model)
				T.setDaemon(True)
				T.start()
		return
	def delete(self,widget):
		selection=self.treeview.get_selection()
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				host=model[path][1]
				role=model[path][3]
				conn=sqlite3.connect('db/config.db')	
				c=conn.cursor()
				c.execute("delete from config where hostname='%s' " % (host))
				conn.commit()
				conn.close()
				model.remove(model.get_iter(path))		
		return
	def clear(self,widget):
		self.model.clear()
		#conn=sqlite3.connect('db/server.db')
		#c=conn.cursor()
		#c.execute('delete from server')
		#conn.commit()
		#conn.close()
		return
	def refresh(self,widget):
                model=self.create_model()
                self.treeview.set_model(model)
                return
	def choose_all(self,widget):
		if widget.get_active():
			self.treeview.get_selection().select_all()
			self.treeview.get_model().foreach(self.choose,True)
		else:	
			self.treeview.get_selection().unselect_all()
			self.treeview.get_model().foreach(self.choose,False)
		return
	def choose(self,model,path,iter,data):
		model.set_value(iter,0,data)
		return
	def select_changed(self,selection):
		model,paths = selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				treeiter=model.get_iter(path)
				value=not self.liststore.get_value(treeiter,0)
				self.liststore.set_value(treeiter,0,value)
		return
	def edit(self,widget):
		selection=self.treeview.get_selection()
		model,paths=selection.get_selected_rows()
		if paths is not None:
			for path in paths:
				host=model[path][1]
				index=model[path][3]
			EditServer.EditServer(host,index)

	def preference(self,widget):
		b=gtk.Builder()
		b.add_from_file('xml/softpreference.xml')
		w=b.get_object('mainwindow')
		w.set_size_request(600,460)
		w.set_keep_above(True)
		w.set_position(gtk.WIN_POS_CENTER)
		hpaned=b.get_object('hpaned1')
		hpaned.set_position(150)
		treeview1=b.get_object('treeview1')
		model=gtk.ListStore(str,int)
		model.append(['接入服务器',0])
		model.append(['云中间件',1])
		model.append(['云管理平台',2])
		model.append(['云孵化平台',3])
		model.append(['数据库服务器',4])
		model.append(['双机热备',5])
		model.append(['MFS主控服务器',6])
		model.append(['MFS备份服务器',7])
		model.append(['MFS数据服务器',8])
		model.append(['MFS客户端服务器',9])
		treeview1.set_model(model)
		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn('角色列表',text,text=0)
		treeview1.append_column(column)

		model=gtk.ListStore(bool,str)
		files=os.listdir('package')
		files.sort()
		for file in files:
			if file == 'list.server' or file == 'list.client':
				continue
			else:
				model.append([False,file])
		treeview2=b.get_object('treeview2')
		treeview2.set_model(model)
		toggle=gtk.CellRendererToggle()
		column=gtk.TreeViewColumn('',toggle,active=0)
		treeview2.append_column(column)
		text=gtk.CellRendererText()
		column=gtk.TreeViewColumn('软件包列表',text,text=1)
		treeview2.append_column(column)
		button=b.get_object('button1')	
		button.connect('clicked',self.save_config,w)	
		
		w.show_all()
		return 
	def save_config(self,widget,data):
		data.destroy()	
		

if __name__ == "__main__":
	box=DeployCenter()
	w=gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.set_size_request(500,500)
	w.add(box)
	w.show_all()
	gtk.main()
