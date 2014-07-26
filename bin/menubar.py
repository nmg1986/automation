#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gtk

class MenuBar(gtk.MenuBar):
	def __init__(self):
		super(MenuBar,self).__init__()

		filem=gtk.MenuItem('程序')
		menu=gtk.Menu()
		exit=gtk.ImageMenuItem(gtk.STOCK_QUIT)
		exit.connect('activate',gtk.main_quit)
		menu.append(exit)
		filem.set_submenu(menu)
		self.append(filem)
		
		editm=gtk.MenuItem('设置')
		menu=gtk.Menu()
		config=gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
		config.connect('activate',self.preferences)
		menu.append(config)
		editm.set_submenu(menu)
		self.append(editm)
		
		aboutm=gtk.MenuItem('关于')
		menu=gtk.Menu()
		about_me=gtk.MenuItem('关于作者')
		menu.append(about_me)
		about_she=gtk.MenuItem('关于软件')
		menu.append(about_she)
		aboutm.set_submenu(menu)
		self.append(aboutm)	

		helpm=gtk.MenuItem('帮助')
		menu=gtk.Menu()
		faq=gtk.MenuItem('FAQ')
		menu.append(faq)
		helpm.set_submenu(menu)
		self.append(helpm)
	def preferences(self,menuitem):
		b=gtk.Builder()
		b.add_from_file('xml/preferences.xml')
		w=b.get_object('mainwindow')
		w.set_position(gtk.WIN_POS_CENTER)
		w.show_all()

