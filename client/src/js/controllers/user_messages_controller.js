/**
 * Created by brettlarder on 08/02/2015.
 */
angular.module('ClientApp.controllers.UserMessages', ['ClientApp.services.NetworkData'])

.controller('UserMessagesController', ['$scope', 'Network', function($scope, Network) {
        //TODO: implement full controller methods
        Network.getUserMessages()
            .then(function(data) {
                $scope.messages = data
            })
    }]);
