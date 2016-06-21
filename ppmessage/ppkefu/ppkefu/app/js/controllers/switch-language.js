ppmessageModule.controller("SwitchLanguageCtrl", [
    "$scope",
    "$state",
    "$timeout",
    "$ionicHistory",
    "yvNav",
    "yvSys",
    "yvAlert",
    "yvLocal",
function ($scope, $state, $timeout, $ionicHistory, yvNav, yvSys, yvAlert, yvLocal) {
    
    function _select_cb(language) {
        $scope.active_language = language;
        yvAlert.success();
        if (yvSys.in_mobile()) {
            yvNav.clear(function () {
                yvNav.disable_back();
                $state.go("app.setting-list-mobile");
            });
        }
    }

    
    function _init_cb(language) {
        language = yvLocal.filter_language(language);
        angular.forEach($scope.languageList, function (lang) {
            if (lang.language === language) {
                $scope.active_language = lang.language;
                lang.is_selected = true;
            }
        });
    }

    
    $scope.select = function (language) {
        if ($scope.active_language === language.language) {
            return;
        }
        
        if (yvSys.in_mobile_app()) {
            navigator.globalization.setPreferredLanguage(language.language, function () {
                yvLocal.localize(function () {
                    _select_cb(language.language);
                });
            });
            return;
        }

        yvLocal.localize_by_language(language.language);
        _select_cb(language.language);
    };

    
    function _init() {
        $scope.languageList = [
            {display_name: "app.settings.language.ENGLISH_TAG", language: "en", is_selected: false},
            {display_name: "app.settings.language.CHINESE_TAG", language: "zh-Hans", is_selected: false}
        ];
        
        if (yvSys.in_mobile_app()) {
            navigator.globalization.getPreferredLanguage(function (language) {
                $timeout(function () {
                    _init_cb(language.value);
                });
            });
            return;
        }
        
        yvLocal.get_current_language(_init_cb);
    }

    _init(); 
    
}]);
