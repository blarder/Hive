/**
 * Created by brettlarder on 22/12/2014.
 */
angular.module('ClientApp.services.NetworkData', ['ClientApp.services.Cordova', 'socket.io', 'ngCookies'])

.factory('Network', ['deviceReady', '$q', '$http', '$cookies', 'io', '$rootScope', function(deviceReady, $q, $http, $cookies, io, $rootScope) {
        $http.defaults.useXDomain = true;
        var _baseUrl = 'https://testappblarder.xyz:443';
        var _dataAlreadyCollected = false;
        var _userIsStaff = false;
        var _loggedIn = false;
        var _allData = $q.defer();
        var _socket = null;
        var _onWebsite = false; //Changes to true if device is undefined

        var _channelsObj = {};
        var _channelsCollected = false;

        var _enablePushNotifications = function() {
            deviceReady(function () {
                if (typeof device == 'undefined') {
                    _onWebsite = true;
                    return
                }
                var pushNotification = window.plugins.pushNotification;
                if ( device.platform == 'android' || device.platform == 'Android' || device.platform == "amazon-fireos" ) {
                    pushNotification.register(
                        successHandler,
                        errorHandler,
                        {
                            "senderID":"966247233253",
                            "ecb":"onNotification"
                        });
                } else {
                    pushNotification.register(
                        tokenHandler,
                        errorHandler,
                        {
                            "badge":"true",
                            "sound":"true",
                            "alert":"true",
                            "ecb":"onNotificationAPN"
                        });
                }

                function tokenHandler(token) {
                    window.localStorage.setItem("pushToken", token);
                    console.log(token)
                }

                function onNotification(e) {

                    switch( e.event )
                    {
                        case 'registered':
                            if ( e.regid.length > 0 )
                            {
                                window.localStorage.setItem("registrationId", e.regid);
                            }
                            break;

                        case 'message':
                            // if this flag is set, this notification happened while we were in the foreground.
                            // you might want to play a sound to get the user's attention, throw up a dialog, etc.
                            $rootScope.$broadcast('pushNotificationReceived', e);
                            if ( e.foreground )
                            {
                                console.log('Foreground notification');
                            }
                            else
                            {  // otherwise we were launched because the user touched a notification in the notification tray.
                                if ( e.coldstart )
                                {
                                    console.log('Cold start notification');
                                }
                                else
                                {
                                    console.log('Background notification');
                                }
                            }

                            console.log(e.payload.message);
                            break;

                        case 'error':
                            console.log('Received error');
                            break;

                        default:
                            console.log('Unknown event');
                            break;
                    }
                }

                function onNotificationAPN (event) {
                    $rootScope.$broadcast('pushNotificationReceived', event);
                    if ( event.alert )
                    {
                        navigator.notification.alert(event.alert);
                    }

                    if ( event.badge )
                    {
                        pushNotification.setApplicationIconBadgeNumber(successHandler, errorHandler, event.badge);
                    }
                }

                function successHandler(event){
                    console.log('Success');
                    console.log(event)
                }


                function errorHandler(event) {
                    console.log(event)
                }
            })

        };

        var _getSocket = function() {
            console.log('getting socket');
            if (_socket == null) {
                $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
                console.log('connecting socket');
                console.log(io);
                _socket = io.connect(_baseUrl)
            }

            _socket.on('message', function(message) {
                console.log(message)
            });

            _socket.on('disconnect', function() {
                _socket = null
            });
            return _socket
        };

        var _logout = function() {
            _loggedIn = false;
            _userIsStaff = false;
            return $http.get(_baseUrl + '/users/logout/');
                //.then(function() {
                //    _loggedIn = false
                //})
        };

        var _login = function(username, password) {

            return $http.post(_baseUrl + '/users/login/', {"username": username, "password": password})
                .success(function(data) {
                    window.localStorage.setItem('token', data.token);
                    $http.defaults.headers.common['Authorization'] = "Token " + data.token;
                    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
                    _userIsStaff = data.staff;
                    _loggedIn = true
                })

        };

        var _createAccount = function(userData) {
            return $http.post(_baseUrl + '/users/', userData)
        };

        var _getAllData = function(disallowCached) {
            if (_dataAlreadyCollected && !disallowCached) {
                return _allData.promise
            }

            _dataAlreadyCollected = true;
            _allData = $q.defer();
            return $http.get(_baseUrl + '/completedata/')
                .success(function(data) {
                    _allData.resolve(data)
                })
        };

        var _getPromiseForAttribute = function(attribute, disallowCached) {
            var deferred = $q.defer();
            _getAllData(disallowCached).then(function(data) {
                if (data[attribute]) {
                    deferred.resolve(data[attribute])
                } else if(data.data[attribute]) {
                    deferred.resolve(data.data[attribute])
                }
            });

            return deferred.promise
        };

        var _getUserData = function(disallowCached) {

            return _getPromiseForAttribute('user', disallowCached)
        };

        var _getDevicesData = function(disallowCached) {
            return _getPromiseForAttribute('devices', disallowCached)
        };

        var _getAvailableShifts = function(disallowCached) {
            return _getPromiseForAttribute('events', disallowCached)
        };

        var _getUserMessages = function(disallowCached) {
            return _getPromiseForAttribute('messages', disallowCached)
        };

        var _getAvailableChannels = function() {
            return $http.get(_baseUrl + '/channels/')
        };

        var _getAvailableLocations = function() {
            return $http.get(_baseUrl + '/events/locations/')
        };

        var _getAllShifts = function() {
            return $http.get(_baseUrl + '/events/')
        };

        var _getAllWarnings = function() {
            return $http.get(_baseUrl + '/users/adminwarnings/')
        };

        var _getShift = function(shiftId) {
            return $http.get(_baseUrl + '/events/' + shiftId + '/')
        };

        var _updateUserData = function(userData) {
            return $http.patch(_baseUrl + '/users/mydata/', userData)
        };

        var _registerDevice = function(device) {
            return $http.post(_baseUrl + '/devices' + device.extension, device)
        };

        var _postComment = function(comment) {
            return $http.post(_baseUrl + '/users/message/', {comment: comment})
        };

        var _postShiftLog = function(shiftId, message) {
            return $http.patch(_baseUrl + '/events/' + shiftId + '/', {log: message})
        };

        //TODO: update following two methods for new UserMessage creation API
        var _sendOutNotifications = function(shift, additionalNote) {
            return $http.post(_baseUrl + '/users/usermessages/', {event_id: shift.id, headline: additionalNote, push: true})
        };

        var _sendOutMassNotification = function(additionalNote) {
            return $http.post(_baseUrl + '/users/usermessages/', {headline: additionalNote, push: true})
        };

        var _createUserMessage = function(data) {
            return $http.post(_baseUrl + '/users/usermessages/', data)
        };

        var _getUserMessagesForManagement = function() {
            return $http.get(_baseUrl + '/users/usermessages/')
        };

        var _updateUserMessage = function(data) {
            return $http.patch(_baseUrl + '/users/usermessages/' + data.id + '/', data)
        };

        var _requestForgottenPasswordKey = function(username) {
            return $http.post(_baseUrl + '/users/changepass/', {username: username})
        };

        var _submitPasswordChangeRequest = function(data) {
            return $http.post(_baseUrl + '/users/changepass/', data)
        };

        var _toggleShiftPublicity = function(shift) {
            var newPublicity = !shift.public;
            return $http.patch(_baseUrl + '/events/' + shift.id + '/', {public: newPublicity})
        };

        var _claimShiftForProcessing = function(shift) {
            return $http.patch(_baseUrl + '/events/' + shift.id + '/', '"PROCESS"')
        };

        var _doneProcessingShift = function(shift) {
            return $http.patch(_baseUrl + '/events/' + shift.id + '/', '"DONE"')
        };

        var _modifyUser = function(data) {
            return $http.patch(_baseUrl + '/users/' + data.id + '/', data)
        };

        var _deleteWarning = function(warning) {
            return $http.delete(_baseUrl + '/users/adminwarnings/' + warning.id + '/')
        };

        var _deleteShift = function(shift) {
            return $http.delete(_baseUrl + '/events/' + shift.id + '/')
        };

        var _createLocation = function(data) {
            return $http.post(_baseUrl + '/events/locations/', data)
        };

        var _createChannel = function(data) {
            return $http.post(_baseUrl + '/channels/', data)
        };

        var _createShift = function(data) {
            var channels = [];

            for (var i = 0; i != data.channels.length; ++i) {
                if (data.channels[i].selected) {
                    channels.push(data.channels[i].id)
                }
            }

            var parsedData = {
                channels: channels,
                location: data.location.id,
                start: data.start,
                end: data.end,
                detail: data.detail,
                tags: []
            };
            return $http.post(_baseUrl + '/events/', parsedData)
        };

        _enablePushNotifications();

        return {
            getAllData: _getAllData,
            getAvailableChannels: _getAvailableChannels,
            getChannelsObj: function() {return _channelsObj},
            getAvailableLocations: _getAvailableLocations,
            getAvailableShifts: _getAvailableShifts,
            getUserMessages: _getUserMessages,
            getDevicesData: _getDevicesData,
            getUserData: _getUserData,
            getSocket: _getSocket,
            getShift: _getShift,
            getAllShifts: _getAllShifts,
            getAllWarnings: _getAllWarnings,
            getUserMessagesForManagement: _getUserMessagesForManagement,
            getBaseUrl: function() {return _baseUrl},
            postComment: _postComment,
            postShiftLog: _postShiftLog,
            sendOutNotifications: _sendOutNotifications,
            sendOutMassNotification: _sendOutMassNotification,
            submitPasswordChangeRequest: _submitPasswordChangeRequest,
            requestForgottenPasswordKey: _requestForgottenPasswordKey,
            login: _login,
            logout: _logout,
            enablePushNotifications: _enablePushNotifications,
            updateUserData: _updateUserData,
            createAccount: _createAccount,
            createChannel: _createChannel,
            createLocation: _createLocation,
            createShift: _createShift,
            createUserMessage: _createUserMessage,
            modifyUser: _modifyUser,
            deleteWarning: _deleteWarning,
            deleteShift: _deleteShift,
            registerDevice: _registerDevice,
            toggleShiftPublicity: _toggleShiftPublicity,
            claimShiftForProcessing: _claimShiftForProcessing,
            doneProcessingShift: _doneProcessingShift,
            forceReload: function() {_getAllData(true)},
            loggedIn: function() {return _loggedIn},
            onWebsite: function() {return _onWebsite},
            userIsStaff: function() {return _userIsStaff}
        }


    }]);