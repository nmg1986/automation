#!/usr/bin/python
#-*- coding:utf-8 -*-
import os

MAIN_WINDOW_WIDTH=600
MAIN_WINDOW_HEIGHT=500

THREAD_NUM=0
SERVER_LIST=['192.168.122.1','192.168.122.2']
PKG_DIC={'0':'nginx,memcached,heartbeat,solomon,bluebird',
		 '1':'mkey3ginstall',
		 '2':'mkey3ginstall',
		 '3':'mkey3ginstall',
		 '4':'mkey3ginstall',
		 '5':'mysql',
		}

REMOTE_URL='http://121.199.34.72/package/dheaven/list.server'
SERVER_FILE='package/server.list'

SERVER_TYPE=['接入服务器','中间件服务器','数据库服务器','缓存服务器','文件服务器']

PKG_DIR=os.getcwd()+ '\package'


CONNECT_SUCCEED=0
AUTHFAILED=1
UNREACH=2
TIMEOUT=3
REFUSED=4
HOSTUNREACH=5

SHOWBOX=None
SOFTBOX=None
DEPLOYBOX=None
