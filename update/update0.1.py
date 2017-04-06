#!/usr/bin/python
#-*- encoding:utf-8 -*-
import os
import time
import logging
from ConfigParser import ConfigParser


SERVER_IP = '192.168.184.136'
SERVER_USER = 'root'
CONFPATH = '/home/dwzq/conf/update.conf'
TMPDIR = '/tmp/dwzq'
LOGDIR = '/home/dwzq/log/'
LOCALTIME = time.strftime('%Y%m%d', time.localtime())
print LOCALTIME

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
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s %'
                                   '(levelname)s %(message)s',
                            datefmt = '%a,%b %Y %H:%M:%S',
                            filename='%s' % logPath,
                            filemode='w'
        )

        #初始化TMPDIR
        command_mkdir_tmp = 'mkdir -p %s/%s' % (TMPDIR, LOCALTIME)
        if os.path.exists(TMPDIR):
            logging.info("已经存在%s/%s目录" % (TMPDIR, LOCALTIME))
        else:
            logging.info("创建了%s/%s目录" % (TMPDIR, LOCALTIME))
            os.system(command_mkdir_tmp)

    def getUpdateConf(self):
        """返回当前ip需要升级的war包列表
        """
        # 下载服务器的配置文件到本地
        command_scp = 'scp %s@%s:%s %s/%s' % \
                      (SERVER_USER, SERVER_IP, CONFPATH, TMPDIR, LOCALTIME)
        confPath = '%s/%s/update.conf' % (TMPDIR, LOCALTIME)
        command_rmconf = 'rm -f %s' % confPath
        if os.path.exists(confPath):
            os.system(command_rmconf)
            logging.info("删除了原有配置文件 %s" % confPath)
            os.system(command_scp)
            logging.info('配置文件%s已经下载到%s/%s下' % (confPath, TMPDIR, LOCALTIME))
        else:
            os.system(command_scp)



if __name__ == '__main__':
    u = update()
    u.getUpdateConf()