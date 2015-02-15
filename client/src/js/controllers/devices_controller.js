/**
 * Created by brettlarder on 22/12/2014.
 */
angular.module('ClientApp.controllers.Devices', ['ClientApp.services.NetworkData', 'ClientApp.services.Cordova'])

.controller('DevicesController', ['Network', 'deviceReady', '$scope', function(Network, deviceReady, $scope) {
        var self = this;
        deviceReady(function() {
            $scope.showRegistrationButton = false;
            if(typeof device != 'undefined') {
                self.thisDevice = {
                    name: device.model,
                    device_id: device.uuid
                };
                console.log(device.uuid)
            } else {
                self.thisDevice = {}
            }


            if (window.localStorage.getItem('registrationId')) {
                self.thisDevice.extension = '/gcm/';
                self.thisDevice.registration_id = window.localStorage.getItem('registrationId');

            } else if (window.localStorage.getItem('pushToken')) {
                self.thisDevice.extension = '/apns/';
                self.thisDevice.registration_id = window.localStorage.getItem('pushToken');
            } else {
                self.thisDevice.extension = null
            }

            self.getDevicesData = function(disallowCached) {
                Network.getDevicesData(disallowCached).then(function(data) {
                    $scope.devices = data;
                    if (!self.thisDevice.extension) {
                        return
                    }
                    var alreadyRegistered = false;

                    for (var i = 0, len = $scope.devices.length; i != len; i++) {
                        if ($scope.devices[i].registration_id === self.thisDevice.registration_id) {
                            alreadyRegistered = true;
                            break
                        }
                    }
                    $scope.showRegistrationButton = !alreadyRegistered
                });
            };

            $scope.registerDevice = function() {
                Network.registerDevice(self.thisDevice)
                    .then(function() {
                        self.getDevicesData(true)
                    })
            };

            self.getDevicesData()
        });




    }]);