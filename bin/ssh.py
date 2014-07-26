#!/usr/bin/python


import socket
import errno

try:
	import paramiko
except ImportError:
	print 'paramiko is not installed'
import variables



class SSHClient():
	def __init__(self):
		self.ssh=paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	def connect(self,username,password,hostname,port):
		try:
			self.ssh.connect(hostname=hostname,port=port,username=username,password=password,timeout=60)
			return variables.CONNECT_SUCCEED 
		except paramiko.AuthenticationException:
			return variables.AUTHFAILED 
		except socket.error as e:
			if e.errno == errno.ENETUNREACH:
				return variables.UNREACH 
			if e.errno == errno.ETIMEDOUT:
				return variables.TIMEOUT 
			if e.errno == errno.ECONNREFUSED:
				return variables.REFUSED 
	def upload(self,localfile,remotefile):
		self.sftp=self.ssh.open_sftp()
		self.sftp.put(localfile,remotefile)
	def execute(self,command):
		self.channel=self.ssh.get_transport().open_session()
		self.channel.exec_command(command)
		return self.channel.recv_exit_status()
	def close(self):
		self.sftp.close()
		self.ssh.close()
	def connect_close(self):
                self.ssh.close()
	def execute_command(self,command):
                stdin,stdout,stderr = self.ssh.exec_command(command)
                return (stdin,stdout,stderr)

