#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gtk
import cairo
from   SoftCenter   import SoftCenter
from   DeployCenter import DeployCenter
from   ConfigCenter import ConfigCenter
from   MonitCenter  import MonitCenter

class ToolBar(gtk.Toolbar):
	def __init__(self,parent):
		gtk.Toolbar.__init__(self)

		self.father=parent

                #self.begin_x=''
                #self.begin_y=''
                #self.end_x=''
                #self.end_y=''
                #self.motion=False
                #self.father=parent
                #self.connect('button-press-event',self.mouse_press)
                #self.connect('button-release-event',self.mouse_release)
                #self.connect('motion-notify-event',self.mouse_motion)
                #self.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)
	        #self.hbox=gtk.HBox()
	        #self.add(self.hbox)
		self.set_style(gtk.TOOLBAR_ICONS)
		softaction=gtk.RadioAction('soft','_软件仓库','软件仓库',None,0)
		softaction.set_group(None)
		softaction.connect('activate',self.soft_center)

		deployaction=gtk.RadioAction('deploy','_安装部署','安装部署',None,1)
		deployaction.set_group(softaction)
		deployaction.connect('activate',self.deploy_center)

		monaction=gtk.RadioAction('monit','_监控中心','监控中心',None,3)
		monaction.set_group(softaction)
		monaction.connect('activate',self.monit_center)

		confaction=gtk.RadioAction('conf','_配置中心','配置中心',None,2)
		confaction.set_group(softaction)
		confaction.connect('activate',self.conf_center)

		quitaction=gtk.RadioAction('deploy','_退出程序','退出程序',None,4)
		quitaction.set_group(softaction)
		quitaction.connect('activate',self.quit)

		softitem=softaction.create_tool_item()
		softitem.set_size_request(80,50)
		#self.hbox.pack_start(softitem,True,True,0)
		self.insert(softitem,-1)

		deployitem=deployaction.create_tool_item()
		deployitem.set_size_request(80,50)
		#self.hbox.pack_start(deployitem,True,True,0)
		self.insert(deployitem,-1)

		confitem=confaction.create_tool_item()
		confitem.set_size_request(80,50)
		self.insert(confitem,-1)

		monitem=monaction.create_tool_item()
		monitem.set_size_request(80,50)
		#self.hbox.pack_start(monitem,True,True,0)
		self.insert(monitem,-1)

		quititem=quitaction.create_tool_item()
		quititem.set_size_request(80,50)
		#self.hbox.pack_end(quititem,True,False,0)
		self.insert(quititem,-1)

		softaction.activate()
	#def mouse_press(self,widget,event):
        #        if event.button == 1:
        #            if not self.motion:
        #                self.motion = True
        #                self.begin_x, self.begin_y = event.x, event.y
        #                cursor=gtk.gdk.Cursor(gtk.gdk.FLEUR)
        #                widget.window.set_cursor(cursor)

        #def mouse_release(self,widget,event):
        #        self.motion = False
        #        widget.window.set_cursor(None)

        #def mouse_motion(self,widget,event):
        #        if self.motion :
        #            self.end_x, self.end_y = event.x_root, event.y_root
        #            self.father.move(int(self.end_x - self.begin_x),
        #                    int(self.end_y - self.begin_y))
	def soft_center(self,action):
		try:
			self.father.showbox.remove(self.father.showbox.get_children()[0])
		except IndexError:
			pass
		self.father.showbox.add(SoftCenter())
		self.father.showbox.show_all()

		return
	def deploy_center(self,action):
		try:
			self.father.showbox.remove(self.father.showbox.get_children()[0])
		except IndexError:
			pass
		self.father.showbox.add(DeployCenter(self.father))
		self.father.showbox.show_all()

		return
	def conf_center(self,action):
                try:
			self.father.showbox.remove(self.father.showbox.get_children()[0])
		except IndexError:
			pass
		self.father.showbox.add(ConfigCenter())
		self.father.showbox.show_all()

		return
	def monit_center(self,action):
                try:
			self.father.showbox.remove(self.father.showbox.get_children()[0])
		except IndexError:
			pass
		self.father.showbox.add(MonitCenter())
		self.father.showbox.show_all()
	def quit(self,action):
                self.father.destroy()
                gtk.main_quit()
                return
	#def draw_pixbuf(self,widget,event):

	#	path = 'img/bg.jpg'
	#	rec=widget.get_allocation()
	#	width,height=rec.width,rec.height
	#	pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(path,width,height)
	#	#img=gtk.Image()
	#	#img.set_from_pixbuf(pixbuf)
	#	#widget.add(img)
	#	#pixmap, mask=pixbuf.render_pixmap_and_mask()
	#	#widget.window.set_back_pixmap(pixmap, False)
	#	widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

	#	#cr = widget.window.cairo_create()
	#	#cr.set_operator(cairo.OPERATOR_CLEAR)
	#	#cr.rectangle(rec.x,rec.y, width,height)
	#	#cr.fill()
	#	#cr.set_operator(cairo.OPERATOR_OVER)
