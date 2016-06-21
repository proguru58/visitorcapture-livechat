((function(Service) {

    function PPAPI() {

        var _apiToken = null,
            _apiKey = null,
            _apiSecret = null,
            _appUuid = null,

            // Internal Server Error
            _onError = function(response, fail) {
                Service.$debug.d('[PPAPI] [Error]: ', response);
                Service.$errorHint.warn(Service.ErrorHint.ERROR_SERVICE_NOT_AVALIABLE);
                if (fail) fail(response);
            },

            _onApiError = function(response, fail) {
                Service.$debug.d('[PPAPI] [Fail]: ', response);
                if (fail) fail(response);
            },
            
            _onApiSuccess = function(response, success) {
                Service.$debug.d('[PPAPI] [Success]: ', response);
                if (success) success(response);
            },
            
            _onResponse = function(response, success, fail) {
                if (response && (response['error_code'] !== undefined)) {
                    var succ = false;
                    switch(response['error_code']) {
                    case 0:
                        succ = true;
                        break;
                        
                    // case 25: // no imapp info
                    //     Service.$errorHint.warn(Service.ErrorHint.ERROR_ILLEGAL_APPKEY_OR_SECRET);
                    //     break;
                        
                    default:
                        break;
                    }

                    if (succ) {
                        _onApiSuccess(response, success);                                
                    } else {
                        _onApiError(response, fail);
                    }
                } else {
                    _onApiError(response, fail);
                }
            },
            
            _onBeforeSend = function(url, data) {
                Service.$debug.d('[PPAPI] [Request]: ', url, data);
            };
                        
        this._post = function(url, data, success, fail) {

            if (_apiToken == null) {
                Service.$debug.d('[PPAPI] [Error]: ', "no token");
                Service.$errorHint.warn(Service.ErrorHint.ERROR_SERVICE_NOT_AVALIABLE);
                return;
            }
           
            var urlPath = Configuration.api + url;
            $.support.cors = true;

            // DON'T set `dataType` to `json` here !!!
            //
            // If you set `dataType: 'json'`, then when you send `??`, jQuery will throw a `parsererror` exception
            // 
            // As the jQuery offical doc says:
            // The JSON data is parsed in a strict manner; any malformed JSON is rejected and a parse error is thrown
            //
            // @see http://api.jquery.com/jquery.ajax/
            // @see http://stackoverflow.com/questions/5061310/jquery-returning-parsererror-for-ajax-request
            $.ajax({
                url: urlPath,
                type: 'post',
                data: Service.$json.stringify(data),
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authorization": "OAuth " + _apiToken,
                },
                cache: false,
                crossDomain : true,
                beforeSend: function() {
                    _onBeforeSend(urlPath, data);
                },
                success: function(response) {
                    _onResponse(response, success, fail);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    _onError(textStatus, fail);
                }
            });
        };

        this.init = function(appUuid, apiKey, apiSecret) {
            _appUuid = appUuid;
            _apiKey = apiKey;
            _apiSecret = apiSecret;            
        };

        this.getPPComToken = function(success, fail) {
            var urlPath = Configuration.auth + "/token";
            var requestData = "client_id=" + _apiKey + "&client_secret=" + _apiSecret + "&grant_type=client_credentials"
            
            $.support.cors = true;
            $.ajax({
                url: urlPath,
                type: 'post',
                data: requestData,
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                cache: false,
                crossDomain : true,
                beforeSend: function() {
                    _onBeforeSend(urlPath, requestData);
                },
                success: function(response) {
                    _apiToken = response.access_token;
                    _onApiSuccess(response, success);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    _onError(textStatus, fail);
                }
            });
        };

        this.updateUser = function(data, success, fail) {
            this._post("/PP_UPDATE_USER", $.extend( {}, data ), success, fail );
        };

        this.getConversationList = function(data, success, fail) {
            this._post("/PP_GET_USER_CONVERSATION_LIST", $.extend({}, data), success, fail);
        };

        this.getConversation = function(data, success, fail) {
            this.getConversationList(data, success, fail);
        };

        // data : { user_uuid: xxx, app_uuid: xxx, member_list: [ 'xxxxx', 'xxxxx' ], group_uuid: xxx }
        this.createConversation = function(data, success, fail) {
            this._post("/PP_CREATE_CONVERSATION", $.extend( {}, data ), success, fail);
        };

        this.sendMessage = function(data, success, fail) {
            this._post("/PP_SEND_MESSAGE", data, success, fail);
        };

        /*
         * Get unacked messages
         */
        this.getUnackedMessages = function(data, success, fail) {
            this._post("/GET_UNACKED_MESSAGES", $.extend( {}, data ), success, fail);
        };

        // { list: [ 'xxx', 'xxxx' ] }
        this.ackMessage = function(data, success, fail) {
            this._post("/ACK_MESSAGE", $.extend( {}, data ), success, fail);
        };

        this.createAnonymousUser = function(data, success, fail) {
            this._post("/PP_CREATE_ANONYMOUS", $.extend( {}, data ), success, fail);
        };

        // {
        //     app_uuid: xxx,
        //     user_uuid: xxx,
        //     device_ostype: xxx,
        //     ppcom_trace_uuid: xxx,
        //     device_id: xxx
        // }
        this.createDevice = function(data, success, fail) {
            this._post("/PP_CREATE_DEVICE", $.extend( true, {}, data ), success, fail);
        };

        // @device_os_type: `Service.$device.getOSType()`;
        this.updateDevice = function(data, success, fail) {
            this._post("/PP_UPDATE_DEVICE", $.extend( {}, data ), success, fail);
        };

        /*
         * Get user_uuid by the third-web-site's user_email
         */
        this.getUserUuid = function(data, success, fail) {
            this._post("/PP_GET_USER_UUID", $.extend( {}, data ), success, fail);
        };

        this.getUserDetailInfo = function(data, success, fail) {
            this._post("/GET_YVOBJECT_DETAIL", $.extend( {}, data ), success, fail);
        };

        /**
         * Get message conversation historys
         */
        this.getMessageHistory = function(data, success, fail) {
            this._post("/PP_GET_HISTORY_MESSAGE", $.extend( {}, data ), success, fail);
        };

        /**
         * Get ImappInfo
         */
        this.getAppInfo = function(data, success, fail) {  
            this._post("/PP_GET_APP_INFO", $.extend( {}, data ), success, fail);
        };

        /**
         * Get welcome team
         */
        this.getWelcomeTeam = function(data, success, fail) {
            this._post("/PP_GET_WELCOME_TEAM", $.extend( {}, data ), success, fail);
        };

        // data: { app_uuid: xxx }
        this.getAppOrgGroupList = function(data, success, fail) {
            this._post('/PP_GET_APP_ORG_GROUP_LIST', $.extend({}, data), success, fail);
        };

        // data: { app_uuid: xxx, group_uuid: xxx }
        this.getOrgGroupUserList = function ( data, success, fail ) {
            this._post( '/PP_GET_ORG_GROUP_USER_LIST', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, group_uuid: xxx }
        this.getOrgGroupConversationId = function ( data, success, fail ) {
            this._post( '/PP_GET_ORG_GROUP_CONVERSATION', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, user_uuid: xxx }
        this.getDefaultConversation = function ( data, success, fail ) {
            this._post( '/PP_GET_DEFAULT_CONVERSATION', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, conversation_uuid: xxx }
        this.getConversationUserList = function ( data, success, fail ) {
            this._post( '/PP_GET_CONVERSATION_USER_LIST', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, user_uuid: xxx, device_uuid: xxx, group_uuid: xxx }
        this.cancelWaitingCreateConversation = function ( data, success, fail ) {
            this._post( '/PP_CANCEL_WAITING_CREATE_CONVERSATION', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, user_uuid: xxx, device_uuid: xxx }
        this.getPPComDefaultConversation = function ( data, success, fail ) {
            this._post( '/PPCOM_GET_DEFAULT_CONVERSATION', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, user_uuid: xxx, member_list: [ 'user_uuid' ], group_uuid: xxx }
        this.createPPComConversation = function ( data, success, fail ) {
            this._post( '/PPCOM_CREATE_CONVERSATION', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx, user_uuid: xxx, conversation_uuid: xxx }
        this.getConversationInfo = function ( data, success, fail ) {
            this._post( '/PP_GET_CONVERSATION_INFO', $.extend( {}, data ), success, fail );
        };

        // data: { app_uuid: xxx }
        this.getWaitingQueueLength = function( data, success, fail ) {
            this._post( '/PP_GET_AMD_QUEUE_LENGTH', $.extend( {}, data ), success, fail );
        };

        this.getAppUuid = function() {
            return _appUuid;
        };

        this.getApiToken = function() {
            return _apiToken;
        };

    }

    Service.$api = new PPAPI();
    
})(Service));
