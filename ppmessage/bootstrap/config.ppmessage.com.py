# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 PPMessage.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
#

"""
BOOSTRAP_CONFIG is the first place for developer edit before run PPMessage.

"team", to run PPMessage needing a team who is the first service team of the PPMessage
"user", to run PPMessage needing a user who create the first service team and admin the whole PPMessage system
"mysql", database config
"redis", redis config
"nginx", nginx config

"""

BOOTSTRAP_CONFIG = {
    "team": {
        "app_name": "PPMessage",
        "company_name": "YOURUI",
    },

    "user": {
        "user_language": "en_us", # zh_cn, en_us, zh_tw
        "user_firstname": "Guijin",
        "user_lastname": "Ding",
        "user_fullname": "Guijin Ding",
        # email is user account
        "user_email": "dingguijin@gmail.com",
        "user_password": "123",
    },

    "mysql": {
        "db_host": "127.0.0.1",
        "db_user": "root",
        "db_pass": "test",
        "db_name": "ppmessage",
    },

    "server": {
        "name": "ppmessage.com", # `` PPMessage use the host ip address otherwise fill it with host name like `ppmessage.com`/`www.ppmessage.com`
        "identicon_store": "/usr/local/opt/ppmessage/identicon",
        "generic_store": "/usr/local/opt/ppmessage/generic",
    },

    "js": {
        "min": "no", # `yes` or `no` for minimized the PPCOM/PPKEFU javascript file
    },
    
    # nginx conf 
    "nginx": {
        "nginx_conf_path": "/usr/local/nginx/conf/nginx.conf",
        "server_name": ["ppmessage.com", "www.ppmessage.com"],
        "listen": "80", #80

        "upload_store": "/usr/local/opt/ppmessage/uploads 1",
        "upload_state_store": "/usr/local/opt/ppmessage/upload_state",

        "ssl": "on", # off/on
        "ssl_listen": "443",
        "ssl_certificate": "/home/ubuntu/certs/comodoev/z/ssl-bundle.crt",
        "ssl_certificate_key": "/home/ubuntu/certs/comodoev/private.pem",
    },

    # apns push certificate, dev for developer, pro for production
    "apns": {
        "name": "com.ppmessage.ppkefu.team",
        "dev": "team-dev.p12",
        "pro": "team-pro.p12",
    },    
    
    # google cloud message
    "gcm": {
        "api_key": "AIzaSyArXf60KTz2KwROtzAlQDJozAskFAdvzBE",
        "sender_id": "878558045932",
    },

    # email service config
    "email": {
        "service_type": "mailgun",
        "domain_name": "mg.ppmessage.com",
        "from_email": "service@ppmessage.com",
        "from_name": "PPMessage Service",
        "private_api_key": "key-7d5cf0ffe7c013db67b3f4af98108f3d",
    },
    
}
