#!/usr/bin/env python
import os
from ConfigParser import ConfigParser

confPath = '/mnt/hgfs/PycharmProjects/autoUpdateTomcat/conf/update.conf'
if os.path.exists(confPath):
    print 'ok'