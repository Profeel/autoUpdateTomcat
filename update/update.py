#!/usr/bin/python
#-*- encoding:utf-8 -*-
import os
import time
import logging
import socket
from ConfigParser import ConfigParser

# 系统当前日期如20170407
LOCALTIME = time.strftime('%Y%m%d', time.localtime())
# 服务器ip
SERVER_IP = '192.168.184.136'
# 连接服务器使用用户名
SERVER_USER = 'root'
# 服务器配置文件位置
CONFPATH = '/home/dwzq/conf/update.conf'
# 配置tmp目录
TMPDIR = '/tmp/dwzq'
LOGDIR = '/home/dwzq/log/'
ADDIPLIST = []
UPDATEIPLIST = []
DELIPLIST = []

command_scp = 'scp %s@%s:%s %s/%s/' % \
              (SERVER_USER, SERVER_IP, CONFPATH, TMPDIR, LOCALTIME)
confPath = '%s/%s/update.conf' % (TMPDIR, LOCALTIME)
command_rmconf = 'rm -f %s' % confPath

# 步骤1：从远程获取信息，得出本机的增删改清单

class update:
    def __init__(self):
        #初始化日志
        logPath = LOGDIR + '/' + LOCALTIME + '.log'
        command_mkdirLog = 'mkdir -p %s' % (LOGDIR)
        if os.path.exists(LOGDIR):
            print '已经存在日志目录%s' % LOGDIR
        else:
            os.system(command_mkdirLog)
            print '创建日志目录%s' % LOGDIR
        print logPath
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s %'
                                   '(levelname)s %(message)s',
                            datefmt = '%a,%b %Y %H:%M:%S',
                            filename='%s' % logPath,
                            filemode='w'
        )

        #初始化本地配置文件TMPDIR
        tmpConfDir = TMPDIR + '/' + LOCALTIME
        command_mkdir_tmp = 'mkdir -p %s' % tmpConfDir
        if os.path.exists(tmpConfDir):
            logging.info("已经存在%s目录" % tmpConfDir)
        else:
            logging.info("创建了%s目录" % tmpConfDir)
            os.system(command_mkdir_tmp)

    def getUpdateConf(self):
        """返回当前ip需要升级的war包列表
        """
        # 下载服务器的配置文件到本地
        if os.path.exists(confPath):
            os.system(command_rmconf)
            logging.info("删除了原有配置文件 %s" % confPath)
            os.system(command_scp)
            logging.info('配置文件%s已经下载到%s/%s下' % (confPath, TMPDIR, LOCALTIME))
        else:
            logging.info("下载配置文件%s" % confPath)
            os.system(command_scp)

    def get_local_ip(self):
        """
        返回本机ip
        """
        try:
            csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            csock.connect(('8.8.8.8', 80))
            (addr, port) = csock.getsockname()
            csock.close()
            return addr
        except socket.error:
            return "127.0.0.1"

    def readConf(self):
        """读取配置文件内容，并匹配自己需要操作的war包
        :return: 本机需要操作的字典
        """
        # 获取本机的ip地址
        localIP = self.get_local_ip()
        cf = ConfigParser()
        # ====修改======
        #cf.read(confPath)
        cf.read('/mnt/hgfs/PycharmProjects/autoUpdateTomcat/conf/update.conf')
        for opt in cf.options('app Hosts'):
            hostname = cf.get('app Hosts', '%s' % opt)
            ADDIPLIST.append(cf.get('%s' % hostname, 'ip'))

if __name__ == '__main__':
    u = update()
    u.getUpdateConf()
    u.readConf()
    print ADDIPLIST