/**
 * Created by brettlarder on 07/01/2015.
 */
angular.module('ClientApp.controllers.ForgotPassword', ['ClientApp.services.NetworkData'])

.controller('ForgotPasswordController', ['Network', '$scope', '$location', function(Network, $scope, $location) {
    $scope.username = "";
    $scope.forgottenPasswordKey = "";
    $scope.password = "";
    $scope.passwordConfirmation = "";
    $scope.requestKeyButtonEnabled = false;

    $scope.requestForgottenPasswordKey = function() {
        $scope.passwordError = $scope.keyError = $scope.usernameError = false;
        $scope.requestKeyButtonEnabled = false;
        Network.requestForgottenPasswordKey($scope.username)
            .success(function() {
                $scope.firstRequestSuccess = true;
            })
            .error(function() {
                $scope.usernameError = true;
            })
    };

    $scope.submitPasswordChangeRequest = function() {
        $scope.passwordError = $scope.keyError = $scope.usernameError = false;

        if ($scope.password !== $scope.passwordConfirmation) {
            //Passwords don't match
            $scope.passwordError = true;
            return
        }

        Network.submitPasswordChangeRequest({
            username: $scope.username,
            key: $scope.forgottenPasswordKey,
            password: $scope.password
        })
            .success(function() {
                $scope.secondRequestSuccess = true;
            })
            .error(function() {
                //Couldn't change password
                $scope.keyError = true;
            })
    };

    $scope.backToLogin = function() {
        $location.path('/login')
    }

}]);