#-*- encoding:utf-8 -*-
from ConfigParser import ConfigParser

if __name__ == '__main__':
    cf = ConfigParser()
    # 读取配置
    cf.read('/mnt/hgfs/PycharmProjects/autoUpdateTomcat/conf/update.conf')
    # 返回所有的分块
    secs = cf.sections()
    print 'sections:', secs
    gzh = cf.options('WJ-weixin-gzh01')
    print 'WJ-weixin-gzh01:', gzh
    # 返回分块的值
    gzh_ip = cf.get('WJ-weixin-gzh01', 'ip')