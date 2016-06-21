# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
#
# api/handlers/ppcreateapphandler.py
#
#

from .basehandler import BaseHandler

from ppmessage.core.constant import PPCOM_WELCOME
from ppmessage.core.constant import PPCOM_OFFLINE
from ppmessage.core.constant import APP_POLICY
from ppmessage.core.constant import SHOW_PPCOM_HOVER
from ppmessage.core.constant import PPCOM_LAUNCHER_STYLE

from ppmessage.db.models import ApiInfo
from ppmessage.db.models import AppInfo
from ppmessage.db.models import AppUserData
from ppmessage.db.models import AppBillingData
from ppmessage.db.models import DeviceUser

from ppmessage.api.error import API_ERR

from ppmessage.core.constant import API_LEVEL

import json
import uuid
import redis
import logging
import base64
import hashlib
import datetime

def encode(_key):
    '''
    @see ppmessage/scripts/bootstrap.py _encode
    '''
    _key = hashlib.sha1(_key).hexdigest()
    _key = base64.b64encode(_key)
    return _key

def _create_apiinfo(_handler, user_uuid, app_uuid, api_level):
    _redis = _handler.application.redis
    _row_data = {
        "createtime": datetime.datetime.now(),
        "updatetime": datetime.datetime.now(),
        "uuid": str(uuid.uuid1()),
        "user_uuid": user_uuid,
        "app_uuid": app_uuid,
        "api_level": api_level,
        "api_key": encode(str(uuid.uuid1())),
        "api_secret": encode(str(uuid.uuid1())),
    }
    _row = ApiInfo(**_row_data)
    _row.async_add()
    _row.create_redis_keys(_redis)
    return

def _create_kefu_client_apiinfo(_handler, user_uuid, app_uuid):
    '''
    create `PPKEFU` client apikey and apiSecret
    '''
    _create_apiinfo(_handler, user_uuid, app_uuid, API_LEVEL.THIRD_PARTY_KEFU)
    return

def _create_console_client_apiinfo(_handler, user_uuid, app_uuid):
    '''
    create `PPCONSOLE` client apiKey and apiSecret
    '''
    _create_apiinfo(_handler, user_uuid, app_uuid, API_LEVEL.THIRD_PARTY_CONSOLE)
    return

def create_app(_handler, _app_name, _user_uuid):
    _redis = _handler.application.redis                               

    _app_key = str(uuid.uuid1())
    _app_secret = str(uuid.uuid1())
    _app_uuid = str(uuid.uuid1())
    _user_email = _redis.hget(DeviceUser.__tablename__ + ".uuid." + _user_uuid, "user_email")
    _company_name = _redis.hget(DeviceUser.__tablename__ + ".uuid." + _user_uuid, "user_company")

    _app_values = {
        "uuid": _app_uuid,
        "user_uuid": _user_uuid,
        "app_name": _app_name,
        "app_key": _app_key,
        "app_secret": _app_secret,
        "app_billing_email": _user_email,
        "app_route_policy": APP_POLICY.BROADCAST,
    }
    
    if _company_name != None and len(_company_name) > 0:
        _app_values["company_name"] = _company_name
        
    _row = AppInfo(**_app_values)
    _row.async_add()
    _row.create_redis_keys(_redis)
                
    _data_uuid = str(uuid.uuid1())
    _data = {
        "uuid": _data_uuid,
        "user_uuid": _user_uuid,
        "app_uuid": _app_uuid,
        "is_owner_user": True,
        "is_service_user": True,
        "is_distributor_user": True,
        "is_portal_user": False
    }
    _row = AppUserData(**_data)
    _row.async_add()
    _row.create_redis_keys(_redis)

    # create api_info
    _create_kefu_client_apiinfo(_handler, _user_uuid, _app_uuid)
    _create_console_client_apiinfo(_handler, _user_uuid, _app_uuid)
    return _app_values

class PPCreateAppHandler(BaseHandler):

    def initialize(self):
        self.addPermission(api_level=API_LEVEL.PPCONSOLE)
        self.addPermission(api_level=API_LEVEL.THIRD_PARTY_CONSOLE)
        return

    def _Task(self):
        super(PPCreateAppHandler, self)._Task()

        _request = json.loads(self.request.body)
        _user_uuid = _request.get("user_uuid")
        _app_name = _request.get("app_name")
                
        if _user_uuid == None or _app_name == None:
            self.setErrorCode(API_ERR.NO_PARA)
            return

        _app_values = create_app(self, _app_name, _user_uuid)
        _r = self.getReturnData()
        _r.update(_app_values)
        return
    
