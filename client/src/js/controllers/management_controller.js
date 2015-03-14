/**
 * Created by brettlarder on 03/01/2015.
 */
angular.module('ClientApp.controllers.Management', ['ClientApp.services.NetworkData', 'ui.bootstrap.datetimepicker', 'MiniDB'])

.controller('ManagementController', ['$scope', '$window', 'Network', 'MiniDB', function($scope, $window, Network, MiniDB) {
    $scope.applyAllUpdates = function() {
        $scope.$apply(function() {});
        console.log(MiniDB.get())
    };
    //MiniDB.setUpdateCallback($scope.applyAllUpdates);
    MiniDB.connectSocket(Network.getSocket());
    $scope.adminMode = 'shifts';
    $scope.shiftLogs = [];
    $scope.chatComments = [];
    $scope.chatComment = '';
    $scope.shifts = MiniDB.getArray('event');
    $scope.shiftsObj = MiniDB.getTable('event');
    $scope.shift = null;
    $scope.shiftToAdd = {};
    $scope.shiftLog = '';
    $scope.warnings = MiniDB.getArray('warning');
    $scope.warningsObj = MiniDB.getTable('warning');
    $scope.usersObj = MiniDB.getTable('user');
    $scope.warning = null;
    $scope.showmodal = false;
    $scope.userMessages = MiniDB.getArray('user_message');

    $scope.shiftCreationData = {channels: MiniDB.getArray('channel')};

    $scope.availableWards = MiniDB.getArray('location');

    $scope.showModal = function() {
        $scope.showmodal = true
    };

    $scope.showModalForMassMessage = function() {
        $scope.shift = null;
        $scope.showmodal = true
    };

    $scope.changeMode = function(newMode) {
        $scope.adminMode = newMode
    };

    $scope.hideModal = function() {
        $scope.showmodal = false
    };

    $scope.commentShowOrHide = "hide";
    $scope.comments = true;

    $scope.toggleComments = function() {
        if ($scope.commentShowOrHide === "hide") {
            $scope.commentShowOrHide = "show"
        } else {
            $scope.commentShowOrHide = "hide"
        }

        $scope.comments = !$scope.comments;
    };

    $scope.loadAllShifts = function() {
        $scope.loading = true;
        $scope.shift = null;
        Network.getAllShifts()
            .success(function(data) {
                MiniDB.update('event', data);
                $scope.loading = false;
            })
    };

    $scope.loadAllWarnings = function() {
        $scope.warning = null;
        Network.getAllWarnings()
            .success(function(data) {
                MiniDB.update('warning', data)
            })
    };

    $scope.loadAllUserMessages = function() {
        Network.getUserMessagesForManagement()
            .success(function(data) {
                MiniDB.update('user_message', data)
            })
    };

    $scope.openUrl = function(url) {
        $window.open(Network.getBaseUrl() + url)
    };

    $scope.postComment = function() {
        if (!$scope.chatComment) {
            return
        }
        Network.postComment($scope.chatComment);
        $scope.chatComment = '';
    };

    $scope.viewShift = function(shiftId) {
        $scope.changeMode('shifts');
        $scope.shift = $scope.shiftsObj[shiftId]
    };

    $scope.viewShiftList = function() {
        $scope.changeMode('shifts');
        $scope.shift = null;
    };

    $scope.viewMessage = function(id) {
        $scope.changeMode('userMessages');
        $scope.userMessage = MiniDB.getTable('user_message')[id]
    };

    $scope.viewUserMessages = function() {
        $scope.changeMode('userMessages');
        $scope.userMessage = null;
    };

    $scope.viewAddShiftForm = function() {
        $scope.changeMode('addShift');
    };

    $scope.viewWarning = function(warningId) {
        $scope.changeMode('warnings');
        $scope.warning = $scope.warningsObj[warningId]
    };

    $scope.viewWarningList = function() {
        $scope.changeMode('warnings');
        $scope.warning = null
    };

    $scope.postShiftLog = function() {
        if (!$scope.shiftLog) {
            return
        }
        Network.postShiftLog($scope.shift.id, $scope.shiftLog)
            .success(function() {
                //$scope.viewShift({shift_id: $scope.shift.id})
            });
        $scope.shiftLog = '';
    };

    $scope.toggleShiftPublicity = function() {
        Network.toggleShiftPublicity($scope.shift)
            .success(function() {
                //$scope.viewShift({shift_id: $scope.shift.id})
            })
    };

    $scope.toggleStaffVerification = function() {
        Network.modifyUser({'id': $scope.warning.staff_member.id, 'verified': !$scope.warning.staff_member.verified})
            .success(function() {
                //$scope.warning.staff_member.verified = !$scope.warning.staff_member.verified
            })
            .error(function(data) {
                console.log(data)
            })
    };

    $scope.claimShiftForProcessing = function() {
        Network.claimShiftForProcessing($scope.shift)
    };

    $scope.doneProcessingShift = function() {
        Network.doneProcessingShift($scope.shift)
    };

    $scope.sendOutNotifications = function(headline, detail, push) {
        $scope.hideModal();

        if($scope.shift) {
            Network.createUserMessage({event_id: $scope.shift.id, headline: headline, detail: detail, push: push})
        } else {
            Network.createUserMessage({headline: headline, detail: detail, push: push})
        }

    };

    $scope.deleteWarning = function(warning) {
        Network.deleteWarning(warning);
        $scope.warning = null
    };

    $scope.refresh = function() {
        $scope.loadAllShifts();
        $scope.loadAllWarnings();
        $scope.loadAllUserMessages()
    };

    var socket = Network.getSocket();

    socket.on('connect', function() {
        console.log('connected')
    });

    socket.on('message', function(message) {
        var messageObj = angular.fromJson(message);

        if (messageObj.message_type === 'chat') {
            $scope.chatComments.unshift(messageObj)
        } else if (messageObj.message_type === 'channel') {
            $scope.shiftCreationData.channels.unshift(messageObj)
        }
        $scope.$apply(function() {})
    });

    $scope.refresh();

    Network.getAvailableChannels()
        .success(function(data) {
            MiniDB.update('channel', data)
        });

    Network.getAvailableLocations()
        .success(function(data) {
            MiniDB.update('location', data)
        });

    // -----     FORMS     -----  Used to create new objects inline, while adding a new shift

    $scope.showChannelCreateForm = function() {
        if (!$scope.channelCreateForm) {
            $scope.channelCreateForm = {}
        } else {
            $scope.channelCreateForm = null
        }

    };

    $scope.submitChannel = function() {
        Network.createChannel($scope.channelCreateForm)
            .then(function(data) {
                console.log(data);
                $scope.channelCreateForm = null
            })
    };

    $scope.showWardCreateForm = function() {
        if (!$scope.wardCreateForm) {
            $scope.wardCreateForm = {}
        } else {
            $scope.wardCreateForm = null
        }
    };

    $scope.submitWard = function() {
        Network.createLocation($scope.wardCreateForm)
            .then(function(data) {
                console.log(data);
                $scope.wardCreateForm = null
            })
    };

    $scope.submitShift = function() {
        $scope.createShiftError = null;
        try {
            Network.createShift($scope.shiftCreationData)
                .success(function (data) {
                    if (data.data) {
                        data = data.data
                    }

                    if ($scope.shiftCreationData.send_notification) {
                        $scope.sendOutNotifications("New Event", $scope.shiftCreationData.notification)
                    }
                })
                .error(function (data) {
                    $scope.createShiftError = data
                })
        } catch(err) {
            $scope.createShiftError = "error"
        }
    }

}]);