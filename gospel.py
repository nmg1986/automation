#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from bin.variables import MAIN_WINDOW_WIDTH,MAIN_WINDOW_HEIGHT
from bin.variables import REMOTE_URL,SERVER_FILE
try:
        import gtk
except ImportError as e :
        print e
        sys.exit()
#import bin.SoftCenter as softcenter
#import bin.Deploy as deploy
try:
        import paramiko
except ImportError as e :
        print e

import bin.menubar as menubar
from bin.ToolBar  import ToolBar 
from bin.TitleBar import TitleBar
import time
import urllib
import gobject
import threading

import platform

class Update(threading.Thread):
	def __init__(self,father):
		self.url=REMOTE_URL
		self.filename=SERVER_FILE
		self.father=father

		threading.Thread.__init__(self)

	def run(self):
		try:
			#urllib.urlretrieve(self.url,self.filename)
			pass
		except IOError:
			print '连接网络失败'
		self.father.destroy()
		gospel=Gospel('连接网络失败，你的软件可能不是最新的')
class Start(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.set_default_size(300,100)
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.set_keep_above(True)
		self.set_decorated(False)
		#color=gtk.gdk.color_parse('green')
		#self.modify_bg(gtk.STATE_NORMAL,color)
		vbox=gtk.VBox()
		self.add(vbox)
		img=gtk.Image()
		img.set_from_file('img/gospel.jpg')
		vbox.add(img)
		self.show_all()
	def checkUpdate(self):
		update=Update(self)
		#update=multiprocessing.Process(target=Update,args=(self,))
		update.setDaemon(True)
		update.start()
		#update.join()

	def threads_init(self):
		gtk.gdk.threads_init()			
		
	def main(self):
                gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()

class Gospel(gtk.Window):
	def __init__(self):
		super(Gospel,self).__init__()

		

		self.set_size_request(MAIN_WINDOW_WIDTH,MAIN_WINDOW_HEIGHT)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_resizable(True)
		self.set_decorated(True)
		self.set_app_paintable(True)
		self.set_border_width(0)
		self.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse("green"))
		self.connect("delete-event",gtk.main_quit)
		
		self.vbox=gtk.VBox(False,0)
		self.add(self.vbox)

		self.showbox=gtk.VBox(True,0)
		self.vbox.pack_end(self.showbox,True,True,0)

		self.titlebar=TitleBar(self)
		self.vbox.pack_start(self.titlebar,False,False,0)

		self.toolbar=ToolBar(self)
		self.vbox.pack_start(self.toolbar,False,False,0)

		self.set_sensitive(False)
		
		self.show_all()

		self.loginWin=self.loginWin()
		self.loginWin.show_all()
	def loginWin(self):
                self.loginWin=gtk.Window()
                self.loginWin.set_position(gtk.WIN_POS_CENTER)
                self.loginWin.set_size_request(300,200)
                self.loginWin.set_decorated(False)
                self.fixed=gtk.Fixed()
                self.loginWin.add(self.fixed)
                self.msglabel=gtk.Label()
                self.fixed.put(self.msglabel,50,10)
                self.label=gtk.Label("账号")
                self.fixed.put(self.label,50,55)
                self.userentry=gtk.Entry()
                self.userentry.set_size_request(150,25)
                self.fixed.put(self.userentry,90,50)
                self.label=gtk.Label("密码")
                self.fixed.put(self.label,50,105)
                self.passwdentry=gtk.Entry()
                self.passwdentry.set_size_request(150,25)
                self.fixed.put(self.passwdentry,90,100)
                self.quit_button=gtk.Button("退出")
                self.quit_button.set_size_request(80,30)
                self.login_button=gtk.Button("登录")
                self.login_button.set_size_request(80,30)
                self.fixed.put(self.quit_button,50,150)
                self.fixed.put(self.login_button,170,150)
                self.quit_button.connect("clicked",self.quit_app)
                self.login_button.connect("clicked",self.login_app)

                return self.loginWin
	def login_app(self,widget):
                username=self.userentry.get_text()
                password=self.passwdentry.get_text()
                if username != 'test' or password != '1234':
                        self.msglabel.set_text("用户名或密码错误")
                        self.userentry.set_text("")
                        self.passwdentry.set_text("")
                else:
                        self.loginWin.destroy()
                        self.set_sensitive(True)
        def quit_app(self,widget):
                self.destroy()
                gtk.main_quit()


if __name__ == "__main__" : 
	if platform.system() != 'Linux':
		start=Start()
		start.checkUpdate()
		start.threads_init()
		start.main()
	else:
		gospel=Gospel()
		
		gtk.gdk.threads_init()			
                gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()
