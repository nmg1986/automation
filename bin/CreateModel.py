#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
import os
from ConfigParser import SafeConfigParser
import gtk

import variables

import threading
import time

class DownLoad(threading.Thread):
	def __init__(self,window):
		self.url=variables.REMOTE_URL
		self.filename='package/list.server'
		self.connect='正在检查更新...'
		self.connect_error='无法连接服务器,请检查网络设置'
		self.father_window=window

		threading.Thread.__init__(self)		
	def run(self):
		self.msgBox=gtk.Window()
		self.msgBox.set_default_size(200,100)
		self.msgBox.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.msgBox.set_keep_above(True)
		self.msgBox.set_decorated(False)
		vbox=gtk.VBox()
		self.msgBox.add(vbox)
		label=gtk.Label()
		vbox.add(label)
		label.set_text(self.connect)
		self.msgBox.show_all()
		time.sleep(2)
		try:
			urllib.urlretrieve(self.url,self.filename)
		except IOError:
			label.set_text(self.connect_error)
		time.sleep(2)
		self.msgBox.destroy()
		self.father_window.set_sensitive(True)
		self.father_window.set_accept_focus(False)
		self.father_window.statusbar.set_markup("<span foreground='red' >连接服务器失败，你的软件可能不是最新的.</span>")
		self.father_window.statusbar.set_alignment(0.0,0.5)

class ManageSoftList(threading.Thread):
		def __init__(self,liststore):
			self.liststore=liststore
			self.filename='package/list.server'

			threading.Thread.__init__(self)
		def run(self):
			try:
				T=DownLoad()
				T.setDaemon(True)
				T.start()
				
			except IOError:
				#self.msg(self.connect_error)
				print self.connect_error 
			if os.path.isfile(self.filename):
				parser=SafeConfigParser()
				parser.read(self.filename)
				for section in parser.sections():
					name=section
					desc=parser.get(section,'description').strip("'")
					size=parser.get(section,'size').strip("'")
					version=parser.get(section,'version').strip("'")
					self.liststore.append([False,name,desc,version,version,size,'未知',0])
			return
			if not os.path.isfile(self.filename):
				parser=SafeConfigParser()
				parser.read(self.filename)
				for section in parser.sections():
					name=section
					desc=parser.get(section,'description').strip("'")
					size=parser.get(section,'size').strip("'")
					version=parser.get(section,'version').strip("'")
					self.liststore.append([False,name,desc,'---',version,size,'下载',1])
			else:
				serverparser=SafeConfigParser()
				serverparser.read(self.filename)
				clientparser=SafeConfigParser()
				clientparser.read(self.filename)
				for section in serverparser.sections():
					if clientparser.has_section(section):
						clientversion=clientparser.get(section,'version').strip("'")	
						serverversion=serverparser.get(section,'version').strip("'")
						if (clientversion >= serverversion):
							name=section
							desc=clientparser.get(section,'description').strip("'")
							size=clientparser.get(section,'size').strip("'")	
							self.liststore.append([False,name,desc,clientversion,serverversion,size,'最新',0])
						else:
							name=section
							desc=serverparser.get(section,'description').strip("'")
							size=serverparser.get(section,'size').strip("'")
							self.liststore.append([False,name,desc,clientversion,serverversion,size,'立即更新',1])
					else:
						name=section
						desc=serverparser.get(section,'description').strip("'")
						size=serverparser.get(section,'size').strip("'")
						version=serverparser.get(section,'version').strip("'")
						self.liststore.append([False,name,desc,'---',version,size,'下载',1])
		def flush_soft_list(self):
			parser=SafeConfigParser()
			parser.read('package/list.client')
			for section in parser.sections():
				name=section
				desc=parser.get(section,'description').strip("'")
				size=parser.get(section,'size').strip("'")
				version=parser.get(section,'version').strip("'")
				self.liststore.append([False,name,desc,version,version,size,'最新',0])
