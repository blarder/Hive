/**
 * Created by brettlarder on 22/12/2014.
 */
angular.module('ClientApp.controllers.Login', ['ClientApp.services.NetworkData'])

.controller('LoginController', ['Network', '$scope', '$location', function(Network, $scope, $location) {
        $scope.username = "";
        $scope.password = "";
        $scope.passwordConfirmation = "";
        $scope.statusText = "";
        $scope.email = "";
        $scope.firstName = "";
        $scope.lastName = "";
        $scope.availableChannels = [];
        $scope.toggleButtonText = "Create account";
        $scope.actionButtonText = "Log in";
        $scope.currentConfig = "login";

        $scope.toggleConfig = function() {
            if ($scope.currentConfig == "login") {
                $scope.currentConfig = "signup";
                $scope.toggleButtonText = "Back to log in";
                $scope.actionButtonText = "Create account";
            } else {
                $scope.currentConfig = "login";
                $scope.toggleButtonText = "Create account";
                $scope.actionButtonText = "Log in";
            }
        };

        $scope.errors = {
            username: "",
            password: "",
            email: "",
            firstName: "",
            lastName: ""
        };

        Network.getAvailableChannels()
            .success(function(data) {
                $scope.availableChannels = data
            });

        Network.logout();

        var getSelectedSubscriptions = function() {
            var selection = [];
            for (var i = 0; i != $scope.availableChannels.length; ++i) {
                if ($scope.availableChannels[i].selected) {
                    selection.push($scope.availableChannels[i].id)
                }
            }
            return selection
        };

        var login = function() {
            $scope.statusText = "Logging in...";

            Network.login($scope.username, $scope.password)
                .success(function() {
                    $scope.statusText = 'Success!';
                    if (Network.userIsStaff() && Network.onWebsite()) { //TODO: test this condition
                        $location.path('/management')
                    } else {
                        Network.forceReload();
                        $location.path('/calendar')
                    }

                })
                .error(function(data) {
                    $scope.statusText = 'Could not log in';
                    $scope.errors = data
                })


        };

        var createAccount = function() {

            if(!$scope.password) {
                $scope.statusText = 'Could not create account';
                $scope.errors = {
                    password: ["This field is required."]
                };
                return
            }

            if($scope.password !== $scope.passwordConfirmation) {
                $scope.statusText = 'Could not create account';
                $scope.errors = {
                    password: ["Passwords do not match - please re-enter"]
                };
                return

            }

            $scope.statusText = "Creating account...";
            var userData = {
                "username": $scope.username,
                "password": $scope.password,
                "subscriptions": getSelectedSubscriptions(),
                "email": $scope.email,
                "first_name": $scope.firstName,
                "last_name": $scope.lastName
            };
            Network.createAccount(userData)
                .success(function() {
                    $scope.statusText = 'Account created!';
                    $scope.toggleConfig()
                })
                .error(function(data) {
                    $scope.statusText = 'Could not create account';
                    $scope.errors = data
                })
        };

        $scope.currentAction = function() {
            if ($scope.currentConfig == "login") {
                login()
            } else {
                createAccount()
            }
        };

        $scope.forgotPassword = function() {
            $location.path('/forgotpassword')
        };

    }]);
