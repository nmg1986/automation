#!/usr/bin/env python

import gtk
import cairo

class TitleBar(gtk.Toolbar):
    def __init__(self,father):
        gtk.Toolbar.__init__(self)

        #fixed=gtk.Fixed()
        #self.add(fixed)

        #close_button=gtk.Button("X")
        #close_button.set_size_request(40,20)
        #close_button.set_relief(gtk.RELIEF_NONE)
        #close_button.connect('button-press-event',self.close_app)
        #fixed.put(close_button,555,5)

        #min_button=gtk.Button("-")
        #min_button.set_size_request(40,20)
        #min_button.set_relief(gtk.RELIEF_NONE)
        #fixed.put(min_button,515,5)

        #close_button=gtk.EventBox()
        #close_button.set_size_request(10,8)
        #close_button.connect('button-press-event',self.close_app)
        #fixed.put(close_button,580,5)
        #drawing=gtk.DrawingArea()
        #drawing.connect("expose-event", self.draw_close_button)
        #close_button.add(drawing)

        #min_button=gtk.EventBox()
        #min_button.set_size_request(10,10)
        #close_button.connect('button-press-event',self.close_app)
        #fixed.put(min_button,565,5)
        #drawing=gtk.DrawingArea()
        #drawing.connect("expose-event", self.draw_min_button)
        #min_button.add(drawing)

        #button=gtk.Button("xx")
        #button.set_size_request(40,20)
        #button.set_relief(gtk.RELIEF_NONE)
        #fixed.put(button,5,5)

        self.begin_x=''
        self.begin_y=''
        self.end_x=''
        self.end_y=''
        self.motion=False
        self.father=father
        self.set_size_request(-1,80)
        self.connect('button-press-event',self.mouse_press)
        self.connect('button-release-event',self.mouse_release)
        self.connect('motion-notify-event',self.mouse_motion)
        #self.connect('expose-event',self.draw_pixbuf)
        self.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)

    def mouse_press(self,widget,event):
        if event.button == 1:
            if not self.motion:
                self.motion = True
                self.begin_x, self.begin_y = event.x, event.y
		cursor=gtk.gdk.Cursor(gtk.gdk.FLEUR)
		widget.window.set_cursor(cursor)

    def mouse_release(self,widget,event):
        self.motion = False
	#cursor=gtk.gdk.Cursor(gtk.gdk.SB_LEFT_ARROW)
	widget.window.set_cursor(None)

    def mouse_motion(self,widget,event):
        if self.motion :
            self.end_x, self.end_y = event.x_root, event.y_root
            self.father.move(int(self.end_x - self.begin_x),
                    int(self.end_y - self.begin_y))

    def draw_pixbuf(self,widget,event):
        path = 'img/bg.jpg'
        rec=widget.get_allocation()
        width,height=rec.width,rec.height
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(path,width,200)
        #widget.bin_window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL],
         #       pixbuf, 0, 0, 0,0)
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL],
                pixbuf, 0, 0, 0,0)

	#self.draw_buttons()
    def draw_buttons(self):
    	
	EventBox=gtk.EventBox()
        EventBox.set_size_request(28,20)
        EventBox.connect('button-press-event',self.min)
        EventBox.connect('enter-notify-event',self.min_enter)
        EventBox.connect('leave-notify-event',self.min_leave)
        EventBox.set_events( gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.ENTER_NOTIFY_MASK|gtk.gdk.LEAVE_NOTIFY_MASK)
        Image=gtk.image_new_from_file('img/min.jpg')
        EventBox.add(Image)
	EventBox.show_all()
        self.add(EventBox,500,5)

        EventBox=gtk.EventBox()
        EventBox.set_size_request(28,20)
        EventBox.connect('button-press-event',self.max)
        EventBox.connect('enter-notify-event',self.max_enter)
        EventBox.connect('leave-notify-event',self.max_leave)
        EventBox.set_events( gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.ENTER_NOTIFY_MASK|gtk.gdk.LEAVE_NOTIFY_MASK)
        Image=gtk.image_new_from_file('img/max.jpg')
        EventBox.add(Image)
	EventBox.show_all()
        EventBox.connect('button-press-event',self.max)
        self.add(EventBox,815,5)

    def draw_close_button(self,widget,event):
        style = widget.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        widget.window.draw_line(gc,0,0,10,8)
        widget.window.draw_line(gc,10,0,0,8)

    def draw_min_button(self,widget,event):
        style = widget.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        widget.window.draw_line(gc,0,5,10,5)


    def min(self,widget,event):
   	pass 
    def min_enter(self,EventBox,event):
        EventBox.remove(EventBox.get_children()[0])
        Image=gtk.image_new_from_file('img/min-press.jpg')
        Image.show()
        EventBox.add(Image)
        
    def min_leave(self,EventBox,event):
        EventBox.remove(EventBox.get_children()[0])
        Image=gtk.image_new_from_file('img/min.jpg')
        Image.show()
        EventBox.add(Image)
    def max(self,widget,event):
        if event.button == 1:
            self.destroy()
            gtk.main_quit()
    def max_enter(self,EventBox,event):
        EventBox.remove(EventBox.get_children()[0])
        Image=gtk.image_new_from_file('img/max-press.jpg')
        Image.show()
        EventBox.add(Image)

    def max_leave(self,EventBox,event):
        EventBox.remove(EventBox.get_children()[0])
        Image=gtk.image_new_from_file('img/max.jpg')
        Image.show()
        EventBox.add(Image)
    def close_app(self,eb,event):
        self.father.destroy()
        gtk.main_quit()

