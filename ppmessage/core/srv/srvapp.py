# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
#

from ppmessage.core.constant import REDIS_HOST
from ppmessage.core.constant import REDIS_PORT

from ppmessage.core.singleton import singleton
from tornado.web import Application

import redis

class SrvApp(Application):
    
    def __init__(self, _web):
        self.redis = redis.Redis(REDIS_HOST, REDIS_PORT, db=1)
        settings = {}
        settings["debug"] = True
        handlers = []
        handlers.extend(_web)            
        Application.__init__(self, handlers, **settings)

    def hasCallback(self):
        return False
