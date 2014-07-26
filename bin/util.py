#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import time
import os
import sqlite3

from ssh import *

PKG_DIR='package/'
REMOTE_DIR='/opt/'
class INSTALL(threading.Thread):
	def __init__(self,treemodel,treeiter,liststore):
		self.model=treemodel
		self.treeiter=treeiter
		self.liststore=liststore
		self.host=self.model.get_value(self.treeiter,1)
		index=self.model.get_value(self.treeiter,3)
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
					select port,username,password,package 
					from server where hostname='%s' and role='%s'
				  ''' %(self.host,index)
				) 
		data=c.fetchone()
		self.port=int(data[0])
		self.username=str(data[1])
		self.password=str(data[2])
		self.package=data[3].replace(' ','').replace('[','').replace(']','').replace("'","").split(',')
		conn.close()
		threading.Thread.__init__(self)
	def run(self):
		if self.treeiter is not None:
			self.install()	
	def install(self):
                path=self.liststore.get_path(self.treeiter)
                print path
		self.liststore.set_value(self.treeiter,7,'--')
		ssh=SSHClient()
		self.liststore.set_value(self.treeiter,6,'正在连接服务器')
		rc=ssh.connect(self.username,self.password,self.host,self.port)	
		if rc == 0:
			self.liststore.set_value(self.treeiter,6,'成功建立连接')
		else:
			self.liststore.set_value(self.treeiter,6,'连接失败(%d)' % rc)
			return
		time.sleep(2)
		for package in self.package:
                        package=package.split('-')[0]
			self.liststore.set_value(self.treeiter,6,'正在上传%s安装包' % package)
			localfile=os.path.join(PKG_DIR,package)
			remotefile=os.path.join(REMOTE_DIR,package)
			ssh.upload(localfile,remotefile)
			time.sleep(2)
			self.liststore.set_value(self.treeiter,6,'上传成功')
			time.sleep(2)
			self.liststore.set_value(self.treeiter,6,'正在解压%s安装包' % package)
			rc=ssh.execute('tar -xzmf %s -C %s' % (remotefile,REMOTE_DIR))
			time.sleep(3)
			if rc == 0:
				self.liststore.set_value(self.treeiter,6,'解压%s成功'%package)
			else:
				self.liststore.set_value(self.treeiter,6,'解压%s失败'%package)
				return
			time.sleep(1)
			self.liststore.set_value(self.treeiter,6,'正在部署%s' % package)
			rc=ssh.execute('cd %s/%s;./install' % (REMOTE_DIR,package))
			if rc == 0:
				self.liststore.set_value(self.treeiter,6,'部署%s成功'%package)
			else :
				self.liststore.set_value(self.treeiter,6,'部署%s失败'%package)
				self.liststore.set_value(self.treeiter,7,'×')
				return
		self.liststore.set_value(self.treeiter,6,'部署成功')
		self.liststore.set_value(self.treeiter,7,'√')
		path=self.liststore.get_path(self.treeiter)
		
		conn=sqlite3.connect('db/server.db')
		cursor=conn.cursor()
		cursor.execute("update server set progress='%s',status='1' where rowid='%s'"%(path[0],'部署成功'))
		
class CHECK(threading.Thread):
        def __init__(self,treemodel,treeiter,liststore):

                self.check_load="cat /proc/loadavg  | awk '{printf $3}'"
                self.check_mem='''awk '/MemTotal/{total=$2}/MemFree/{free=$2}/Buffers/{buffers=$2}/^Cached/{cached=$2}END{printf "%.1f",(total-free-buffers-cached)/total*100}'  /proc/meminfo'''
                self.check_swap='''awk '/SwapTotal/{total=$2}/SwapFree/{free=$2}END{if (total == 0){printf "%d",0}else{printf "%.1f", (total-free)/total*100}}'  /proc/meminfo'''
                self.check_root="df -h / | tail -1 | awk '{printf $5}'"
                self.check_process="top -bn1 | grep Tasks | awk '{printf $2}'"
                self.check_users="who | wc -l | tr -d '\n'"
                
                self.model=treemodel
		self.treeiter=treeiter
		self.liststore=liststore
		self.host=self.model.get_value(self.treeiter,1)
		conn=sqlite3.connect('db/server.db')
		c=conn.cursor()
		c.execute('''
			select port,username,password 
			from server where hostname='%s'
			''' %(self.host)
		) 
		data=c.fetchone()
		self.port=int(data[0])
		self.username=str(data[1])
		self.password=str(data[2])
		conn.close()

		threading.Thread.__init__(self)
		#self.interval=interval
		#threading.Timer.__init__(self,self.interval,self.check)
		#self.timer=threading.Timer(self.interval,self.check)
        def run(self):
		if self.treeiter is not None:
			self.check()
	#def stop(self):
        #        self.timer.cancel()
	def check(self):
                
		ssh=SSHClient()
		rc=ssh.connect(self.username,self.password,self.host,self.port)	
		if rc == 0:
			print 'connect succeed'
		else:
			print 'connect failed'
			ssh.connect_close()
			return
		#####check load#####
		stdin,stdout,stderr=ssh.execute_command(self.check_load)
		loadavg=stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,2,'%s' % loadavg)
		#####check memory#####
		(ssh_stdin, ssh_stdout, ssh_stderr) = ssh.execute_command(self.check_mem)
		mem_used=ssh_stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,3,'%s' % mem_used)
		#####check swap#####
		stdin,stdout,stderr=ssh.execute_command(self.check_swap)
		swap=stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,4,'%s' % swap)
		#####check root#####
		stdin,stdout,stderr=ssh.execute_command(self.check_root)
		root_disk=stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,5,'%s' % root_disk.strip('%'))
		#####check process#####
		stdin,stdout,stderr=ssh.execute_command(self.check_process)
		processes=stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,6,'%s' % processes)
		#####check users######
		stdin,stdout,stderr=ssh.execute_command(self.check_users)
		users=stdout.readlines()[0]
		self.liststore.set_value(self.treeiter,7,'%s' % users)
		ssh.connect_close()

                #self.stop()
		#self.timer=threading.Timer(self.interval,self.check)
		#self.start()

class CONFIG(threading.Thread):
	def __init__(self,treemodel,treeiter,liststore):

                self.set_hostname="echo %s > /etc/HOSTNAME"
                self.set_runlevel='''sed "/^id/s/[0-9]/%s/" inittab'''
                self.set_sshport="echo Port %s > /etc/ssh/sshd_config"
                self.set_rootpasswd='''echo "root:%s" | chpasswd'''
                
		self.model=treemodel
		self.treeiter=treeiter
		self.liststore=liststore
		self.host=self.model.get_value(self.treeiter,1)
		index=self.model.get_value(self.treeiter,3)
		conn=sqlite3.connect('db/config.db')
		c=conn.cursor()
		c.execute('''
			select port,username,password
			from config where hostname='%s'
				  ''' %(self.host)
				) 
		data=c.fetchone()
		self.port=int(data[0])
		self.username=str(data[1])
		self.password=str(data[2])
		conn.close()
		threading.Thread.__init__(self)
	def run(self):
		if self.treeiter is not None:
			self.config()	
	def config(self):
		ssh=SSHClient()
		rc=ssh.connect(self.username,self.password,self.host,self.port)	
		if rc == 0:
			print('成功建立连接')
		else:
			print('连接失败')
			return
		#####HOSTNAME#####
		hostname=self.model.get_value(self.treeiter,2)
		#####RUNLEVEL#####
		runlevel=self.model.get_value(self.treeiter,3)
		#####SSHPORT######
		sshport=self.model.get_value(self.treeiter,4)
		#####ROOTPASSWD####
		rootpasswd=self.model.get_value(self.treeiter,5)
		
		conn=sqlite3.connect('db/config.db')
		cursor=conn.cursor()
		cursor.execute("update config set hostname2='%s',runlevel='%s',sshport='%s',rootpasswd='%s' where hostname='%s'"%(hostname,runlevel,sshport,rootpasswd,self.host))
		cursor.close()
		conn.close()
		
class UPDATE(threading.Thread):
     def __init__(self,treeview,liststore,path):
         self.model=treeview.get_model()
         self.treeiter=self.model.get_iter(path)
         self.liststore=liststore
         threading.Thread.__init__(self)
     def run(self):
		self.liststore.set_value(self.treeiter,5,'检查更新...')
		time.sleep(3)
		self.liststore.set_value(self.treeiter,5,'正在更新...')
		time.sleep(3)
		self.liststore.set_value(self.treeiter,5,'更新完毕')
