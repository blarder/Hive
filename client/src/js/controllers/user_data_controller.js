angular.module('ClientApp.controllers.UserData', ['ClientApp.services.NetworkData'])

    .controller('UserDataController', ['$scope', 'Network', '$location', function($scope, Network, $location){
        $scope.verificationKey = "";
        $scope.verificationButtonText = "Submit key";
        $scope.user = {};

        $scope.showUpdateForm = false;
        $scope.userUpdateData = {};

        $scope.logout = function() {
            Network.logout()
                .success(function() {
                    $location.path('/login')
                })
        };

        $scope.attemptVerification = function() {
            $scope.verificationButtonText = "Working...";
            Network.submitVerificationKey($scope.verificationKey)
                .success(function(data) {
                    if (data.verified) {
                        $scope.user.verified = true
                    } else {
                        $scope.verificationButtonText = "Failed - pressed here to resubmit"
                    }
                })
        };

        $scope.updateUserData = function() {
            Network.updateUserData($scope.userUpdateData)
                .success(function(data) {
                    $scope.user = angular.extend($scope.user, data);
                    $scope.showUpdateForm = false;
                    $scope.userUpdateData = {}
                })
                .error(function(data) {
                    console.log('Error updating user info');
                    console.log(data)
                })
        };

        Network.getUserData()
            .then(function(data) {
                $scope.user = data;
            })

    }]);