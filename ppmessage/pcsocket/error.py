# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016.
# Guijin Ding, dingguijin@gmail.com
# All rights reserved
#

from ppmessage.core.constant import enum

DIS_ERR = enum(
    "NOERR",
    "NOUUIDS",
    "NOSERVICE",
    "NOEXTRA",
    "PARAM",
    "TYPE",
    "JSON",
    "MESSAGE",
    "NOTOKEN",
    "WRLEVEL",
    "CONVERSATION",
    "WAITING",
    "CONVERSATION_NO_GROUP",
    "CONVERSATION_NO_USER",
)

def get_error_string(_code):
    _err = {
        DIS_ERR.NOERR: "success, nothing to say.",
        DIS_ERR.NOEXTRA: "no extra data for portal user.",
        DIS_ERR.NOUUIDS: "no app_uuid/user_uuid/device_uuid.",
        DIS_ERR.NOSERVICE: "no service/portal type.",
        DIS_ERR.PARAM: "parameters error.",
        DIS_ERR.TYPE: "no type provided or type is unknown.",
        DIS_ERR.JSON: "message data is not JSON.",
        DIS_ERR.MESSAGE: "message content is illegal.",
        DIS_ERR.NOTOKEN: "no api auth token provided.",
        DIS_ERR.WRLEVEL: "wrong api auth level.",
        DIS_ERR.CONVERSATION: "can not create conversation.",
        DIS_ERR.WAITING: "keep waiting to create conversation.",
        DIS_ERR.CONVERSATION_NO_GROUP: "error to create conversation for no group",
        DIS_ERR.CONVERSATION_NO_USER: "error to create conversation for no user",
    }
    _str = _err.get(_code)
    if _str == None:
        _str = "unknown error, nothing to say."
    return _str
