ppmessageModule.controller("AutoLoginCtrl", [
    "$scope",
    "$state",
    "$stateParams",
    "$ionicHistory",
    "yvNav",
    "yvMain",
    "yvLogin",
    "yvUtil",
function ($scope, $state, $stateParams, $ionicHistory, yvNav, yvMain, yvLogin, yvUtil) {
        
    function login_success() {
        console.log("login successfully...");
    }

    function login_error(reason) {
        console.log("login error:", reason);
        yvNav.disable_next();
        $state.go("noapp.login-error");
    }

    $scope.$on("event:login-error", function (event, error) {
        console.error(error);
    });
    
    function init() {
        $scope.user = {
            request_body: $stateParams.request_body,
        };

        if (!$scope.user.request_body || $scope.user.request_body.length == 0) {
            login_error();
            return;
        }

        var _body_str = yvUtil.base64_decode($scope.user.request_body);
        console.log("auto login with %o", _body_str);
        _body = JSON.parse(_body_str);
        console.log("auto login with %o", _body);
        
        $scope.user.user_email = _body.user_email;
        $scope.user.user_password = _body.user_password;
        var current_session = yvLogin.current_session();
        if (current_session && current_session.user_email == _body.user_email) {
            $ionicHistory.goBack();
            return;
        }
        yvMain.init_yvdb(function (user) {
            yvLogin.login($scope.user);
        });
    }

    init();
}]);
