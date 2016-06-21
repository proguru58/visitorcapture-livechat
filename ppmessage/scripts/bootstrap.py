# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
#

"""
bootstrap is the first command to run. It create
the first user and team of the system, all api keys
for the first team. Save the data to db and generate
a python file which includes the db data. To run 
PPMessage system, definitely it is the first step.

Edit the config.py to choose your user name, user email, password and etc.

Bootstrap!

"""

try:
    from ppmessage.core.constant import API_LEVEL
except:
    print('\033[1;31;40m')
    print("PPMessage requirements not ready. Please run `scripts/require.py`")
    print('\033[0m')
    import sys
    sys.exit()

from ppmessage.bootstrap.config import BOOTSTRAP_CONFIG

from ppmessage.db.models import AppInfo
from ppmessage.db.models import ApiInfo
from ppmessage.db.models import DeviceUser
from ppmessage.db.models import AppUserData    
from ppmessage.db.models import APNSSetting
from ppmessage.db.dbinstance import getDBSessionClass

from ppmessage.core.constant import API_LEVEL
from ppmessage.core.constant import USER_STATUS
from ppmessage.core.p12converter import der2pem

from ppmessage.core.utils.getipaddress import getIPAddress

import os
import sys
import json
import uuid
import copy
import base64
import hashlib
import datetime
import traceback
import subprocess

def _encode(_key):
    _key = hashlib.sha1(_key).hexdigest()
    _key = base64.b64encode(_key)
    return _key

def _check_bootstrap_config():
    _fields = ["team", "user", "server", "js", "mysql", "nginx", "apns", "gcm"]
    for _field in _fields:
        if _field not in BOOTSTRAP_CONFIG:
            print("%s not provided in BOOTSTAP_CONFIG" % _field)
            return None
    _config = copy.deepcopy(BOOTSTRAP_CONFIG)
    return _config

def _create_bootstrap_first_user(_session, _config):
    _user_config = _config.get("user")
    _user = DeviceUser(
        createtime=datetime.datetime.now(),
        updatetime=datetime.datetime.now(),
        uuid=str(uuid.uuid1()),
        user_email=_user_config.get("user_email"),
        user_password=hashlib.sha1(_user_config.get("user_password")).hexdigest(),
        user_fullname=_user_config.get("user_fullname"),
        user_firstname=_user_config.get("user_firstname"),
        user_lastname=_user_config.get("user_lastname"),
        user_language=_user_config.get("user_language"),
        user_status=USER_STATUS.ADMIN,
        is_anonymous_user=False,
    )
    _session.add(_user)
    _session.commit()
    _user_config["user_uuid"] = _user.uuid
    return _config

def _create_bootstrap_first_team(_session, _config):
    _user_config = _config.get("user")
    _team_config = _config.get("team")
    _app = AppInfo(
        createtime=datetime.datetime.now(),
        updatetime=datetime.datetime.now(),
        uuid=str(uuid.uuid1()),
        app_key=_encode(str(uuid.uuid1())),
        app_secret=_encode(str(uuid.uuid1())),
        user_uuid=_user_config.get("user_uuid"),
        app_name=_team_config.get("app_name"),
        company_name=_team_config.get("company_name")
    )
    _session.add(_app)
    _session.commit()
    _team_config["app_uuid"] = _app.uuid
    return _config

def _create_bootstrap_team_data(_session, _config):
    _user_config = _config.get("user")
    _team_config = _config.get("team")
    _data = AppUserData(
        uuid=str(uuid.uuid1()),
        user_uuid=_user_config.get("user_uuid"),
        app_uuid=_team_config.get("app_uuid"),
        is_service_user=True,
        is_owner_user=True,
        is_distributor_user=True,
        is_portal_user=False,
    )
    _session.add(_data)
    _session.commit()
    return _config

def _create_bootstrap_api(_type, _session, _config):
    _user_config = _config.get("user")
    _team_config = _config.get("team")
    _api = ApiInfo(
        createtime=datetime.datetime.now(),
        updatetime=datetime.datetime.now(),
        uuid=str(uuid.uuid1()),
        user_uuid=_user_config.get("user_uuid"),
        app_uuid=_team_config.get("app_uuid"),
        api_level=_type,
        api_key=_encode(str(uuid.uuid1())),
        api_secret=_encode(str(uuid.uuid1())),
    )
    _session.add(_api)
    _session.commit()

    _config[_type] = {
        "api_uuid": _api.uuid,
        "api_key": _api.api_key,
        "api_secret": _api.api_secret,
    }
    return _config

def _update_api_uuid_with_ppconsole(_session, _config):
    _app_config = _config.get("team")
    _one = _session.query(AppInfo).filter(AppInfo.uuid == _app_config.get("app_uuid")).scalar()
    _ppconsole = _config.get(API_LEVEL.PPCONSOLE)
    _one.api_uuid = _ppconsole.get("api_uuid")
    _session.commit()
    return _config

def _create_apns_settings(_session, _config):
    _dev_pem = None
    _pro_pem = None
    _dev_p12 = None
    _pro_p12 = None

    _app_uuid = _config.get("team").get("app_uuid")
    _apns_config = _config.get("apns")

    _name = _apns_config.get("name")
    _dev_file = _apns_config.get("dev")
    _pro_file = _apns_config.get("pro")

    _certs_dir = os.path.dirname(os.path.abspath(__file__))
    _certs_dir = _certs_dir + os.path.sep + ".." + os.path.sep + "certs" + os.path.sep + "apnscerts"
    _dev_file = _certs_dir + os.path.sep + _dev_file
    _pro_file = _certs_dir + os.path.sep + _pro_file

    if not os.path.exists(_dev_file) or not os.path.exists(_pro_file):
        print("No dev or pro cert file found")
        return _config
        
    with open(_dev_file, "rb") as _file:
        _dev_p12 = _file.read()
        _dev_pem = der2pem(_dev_p12)

    with open(_pro_file, "rb") as _file:
        _pro_p12 = _file.read()
        _pro_pem = der2pem(_pro_p12)

    _dev_p12 = base64.b64encode(_dev_p12)
    _dev_pem = base64.b64encode(_dev_pem)
    _pro_p12 = base64.b64encode(_pro_p12)
    _pro_pem = base64.b64encode(_pro_pem)

    _apns = APNSSetting(
        uuid=str(uuid.uuid1()),
        app_uuid=_app_uuid,
        name = _name,
        production_p12=_pro_p12,
        development_p12=_dev_p12,
        production_pem=_pro_pem,
        development_pem=_dev_pem,
        is_development=False,
        is_production=True
    )
    _session.add(_apns)
    _session.commit()
    return _config

def _create_server_config(_session, _config):
    _server_config = _config.get("server")
    _name = _server_config.get("name")
    if _name == None or len(_name) == 0:
        _name = getIPAddress()
        _server_config["name"] = _name

    _generic_store = _server_config.get("generic_store")
    _identicon_store = _server_config.get("identicon_store")

    if not os.path.exists(_generic_store):
        subprocess.check_output("mkdir -p " + _generic_store, shell=True)
        #os.makedirs(_generic_store)
        os.chmod(_generic_store, 0777)
    if not os.path.exists(_identicon_store):
        subprocess.check_output("mkdir -p " + _identicon_store, shell=True)
        #os.makedirs(_identicon_store)
        os.chmod(_identicon_store, 0777)

    return _config
                    
def _create_nginx_config(_session, _config):
    _conf_dir = os.path.dirname(os.path.abspath(__file__))
    _conf_dir = _conf_dir + os.path.sep + ".." + os.path.sep + "conf"
    _ssl_template = _conf_dir + os.path.sep + "nginx.conf.ssl.template"
    _nossl_template = _conf_dir + os.path.sep + "nginx.conf.template"
    _nginx_config = _config.get("nginx")
    _ssl = _nginx_config.get("ssl")
    
    _template = _nossl_template
    if _ssl == "on":
        _template = _ssl_template

    _origin = None
    with open(_template, "r") as _file:
        _origin = _file.read()
        for _key in _nginx_config:
            _str = "{nginx." + _key + "}"
            if _key == "server_name":
                _value = _nginx_config.get(_key)
                if isinstance(_value, list):
                    _origin = _origin.replace(_str, " ".join(_value))
                continue
            _origin = _origin.replace(_str, _nginx_config.get(_key))

    print(_origin)
    if _origin == None:
        print("no nginx template found")
        return _config

    _nginx_conf_path = _nginx_config.get("nginx_conf_path")
    with open(_nginx_conf_path, "w") as _file:
        _file.write(_origin)

    _upload_store = _nginx_config.get("upload_store")
    _upload_store_dir = _upload_store.split(" ")[0]
    _nginx_config["upload_store_dir"] = _upload_store_dir
    
    if not os.path.exists(_upload_store_dir):
        os.makedirs(_upload_store_dir)
        os.chmod(_upload_store_dir, 0777)

    for i in xrange(10):
        _dir = chr(i+ord("0"))
        _dir = _upload_store_dir + os.path.sep + _dir
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            os.chmod(_dir, 0777)
        
    for i in xrange(26):
        _dir = chr(i+ord("A"))
        _dir = _upload_store_dir + os.path.sep + _dir
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            os.chmod(_dir, 0777)

    for i in xrange(26):
        _dir = chr(i+ord("a"))
        _dir = _upload_store_dir + os.path.sep + _dir
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            os.chmod(_dir, 0777)

    return _config

# FIXME: Get log_path from config.py, and be compatible with supervisor conf.
# We need to create supervisor conf when bootstrap.
def _create_log_dir():
    log_path = "/usr/local/var/log"
    if not os.path.exists(log_path):
        subprocess.check_output("mkdir -p " + log_path, shell=True)
    return

def _print_bootstrap_result(_config):
    _header = """
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
# 
# AUTO GENERATE BY BOOTSTRAP
# NEVER EDIT THIS FILE MANUALLY
#
    """
    _user_config = _config.get("user")
    _password = _user_config.get("user_password")
    _user_config["user_password_hash"] = hashlib.sha1(_password).hexdigest()
    
    _password = "*" * len(_password)
    _user_config["user_password"] = _password
    _str = _header + "\n" + "BOOTSTRAP_DATA = " + json.dumps(_config, indent=True)
    
    _this_file_dir = os.path.dirname(os.path.abspath(__file__))
    _data_file_path = _this_file_dir + os.path.sep + ".." + os.path.sep + "bootstrap/data.py"

    with open(_data_file_path, "w") as _file:
        _file.write(_str)

    return

def _clean_bootstrap_db_data(_session):
    _session.query(DeviceUser).delete()
    _session.query(AppInfo).delete()
    _session.query(ApiInfo).delete()
    _session.query(AppUserData).delete()
    _session.query(APNSSetting).delete()
    _session.commit()
    return

def _bootstrap():

    _levels = [API_LEVEL.PPCOM, API_LEVEL.PPKEFU, API_LEVEL.PPCONSOLE,
               API_LEVEL.THIRD_PARTY_KEFU, API_LEVEL.THIRD_PARTY_CONSOLE]
    _config = _check_bootstrap_config()
    if _config == None:
        return
    _session_class = getDBSessionClass()
    _session = _session_class()
    try:
        _clean_bootstrap_db_data(_session)
        _config = _create_bootstrap_first_user(_session, _config)
        _config = _create_bootstrap_first_team(_session, _config)
        _config = _create_bootstrap_team_data(_session, _config)
        for _level in _levels:
            _config = _create_bootstrap_api(_level, _session, _config)
        _config = _update_api_uuid_with_ppconsole(_session, _config)
        _config = _create_apns_settings(_session, _config)
        _config = _create_server_config(_session, _config)
        _config = _create_nginx_config(_session, _config)
        _create_log_dir()
    except:
        traceback.print_exc()
    finally:
        _session_class.remove()

    _print_bootstrap_result(_config)
    return

if __name__ == "__main__":
    _bootstrap()
    
