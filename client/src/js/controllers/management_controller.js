/**
 * Created by brettlarder on 03/01/2015.
 */
angular.module('ClientApp.controllers.Management', ['ClientApp.services.NetworkData', 'ui.bootstrap.datetimepicker'])

.controller('ManagementController', ['$scope', '$window', 'Network', function($scope, $window, Network) {

    $scope.adminMode = 'shifts';
    $scope.shiftLogs = [];
    $scope.chatComments = [];
    $scope.chatComment = '';
    $scope.shifts = [];
    $scope.shiftsObj = {};
    $scope.shift = null;
    $scope.shiftToAdd = {};
    $scope.shiftLog = '';
    $scope.warnings = [];
    $scope.warningsObj = {};
    $scope.usersObj = {};
    $scope.warning = null;
    $scope.showmodal = false;

    $scope.shiftCreationData = {};

    $scope.availableWards = [];

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

    var processShiftsData = function(data) {
        for (var i = 0; i != data.length; ++i) {
            data[i].start = moment(data[i].start);
            data[i].startString = data[i].start.format('lll');
            data[i].end = moment(data[i].end);
            data[i].endString = data[i].end.format('lll');

            for (var j = 0; j != data[i].log.length; ++j) {
                data[i].log[j].time = moment(data[i].log[j].time)
            }
        }
    };

    var processWarningsData = function(data) {
        for (var i = 0; i != data.length; ++i) {
            data[i].time = moment(data[i].time);
            data[i].timeString = data[i].time.format('lll')
        }
    };

    var formHash = function(objList) {
        var hashObj = {};
        for (var i = 0; i != objList.length; ++i) {
            if (objList[i].staff_member) {
                if ($scope.usersObj[objList[i].staff_member.id]) { //User already exists in hash table
                    angular.extend($scope.usersObj[objList[i].staff_member.id], objList[i].staff_member);
                    objList[i].staff_member = $scope.usersObj[objList[i].staff_member.id]
                } else { //User not yet in hash table
                    $scope.usersObj[objList[i].staff_member.id] = objList[i].staff_member
                }
            }
            hashObj[objList[i].id] = objList[i];
        }

        return hashObj
    };

    var extendHash = function(existingHash, newObj) { //Update object in hash, or add a new one if it's not currently there
        if (newObj.staff_member) {
            if ($scope.usersObj[newObj.staff_member.id]) {
                angular.extend($scope.usersObj[newObj.staff_member.id], newObj.staff_member);
                newObj.staff_member = $scope.usersObj[newObj.staff_member.id]
            } else {
                $scope.usersObj[newObj.staff_member.id] = newObj.staff_member
            }
        }
        if (existingHash[newObj.id]) {
            angular.extend(existingHash[newObj.id], newObj);
            return false; //Return false if a new object was not inserted into hash
        } else {
            existingHash[newObj.id] = newObj;
            return true; //Return true if object was new
        }
    };

    var handleIncomingShift = function(shift) {
        processShiftsData([shift]);
        if (extendHash($scope.shiftsObj, shift)) {
            $scope.shifts.unshift(shift)
        }
    };

    var handleIncomingWarning = function(warning) {
        processWarningsData([warning]);
        if (extendHash($scope.warningsObj, warning)) {
            $scope.warnings.unshift(warning)
        }
    };

    //TODO: same hash extension/creation for user messages

    var handleIncomingWarningDeletion = function(warning) {
        //TODO: test this implementation (note minor memory leak req. for speed)
        if ($scope.warning && $scope.warning.id === warning.id) {
            $scope.warning = null
        }
        for (var key in $scope.warningsObj[warning.id]) {
            if ($scope.warningsObj[warning.id].hasOwnProperty(key)) {
                delete $scope.warningsObj[warning.id][key]
            }
        }
    };

    var handleIncomingUser = function(user) {
        extendHash($scope.usersObj, user)
    };

    $scope.loadAllShifts = function() {
        $scope.loading = true;
        $scope.shift = null;
        Network.getAllShifts()
            .success(function(data) {
                processShiftsData(data);
                $scope.shifts = data;
                $scope.shiftsObj = formHash($scope.shifts);
                $scope.loading = false;
            })
    };

    $scope.loadAllWarnings = function() {
        $scope.warning = null;
        Network.getAllWarnings()
            .success(function(data) {
                console.log(data);
                processWarningsData(data);
                $scope.warnings = data;
                $scope.warningsObj = formHash($scope.warnings);
        })
    };

    $scope.loadAllUserMessages = function() {
        Network.getUserMessagesForManagement()
            .success(function(data) {
                $scope.userMessages = data
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

    $scope.viewUserMessages = function() {
        $scope.changeMode('userMessages');
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

    $scope.changeStaffRosterProId = function() {
        Network.modifyUser({'id': $scope.warning.staff_member.id, 'roster_pro_id': $scope.newRosterProId})
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
        Network.deleteWarning(warning)
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
        console.log(messageObj);

        if (messageObj.message_type === 'event_log') {
            messageObj.time = moment(messageObj.time);
            $scope.shiftLogs.unshift(messageObj);
            $scope.shiftsObj[messageObj.event_id].log.push(messageObj);
        } else if (messageObj.message_type === 'chat') {
            $scope.chatComments.unshift(messageObj)
        } else if (messageObj.message_type === 'event') {
            handleIncomingShift(messageObj);
        } else if (messageObj.message_type === 'warning') {
            handleIncomingWarning(messageObj);
        } else if (messageObj.message_type === 'user') {
            handleIncomingUser(messageObj);
        } else if (messageObj.message_type === 'user_message') {
            $scope.userMessages.unshift(messageObj);
        } else if (messageObj.message_type === 'warning_deletion') {
            handleIncomingWarningDeletion(messageObj);
        } else if (messageObj.message_type === 'job') {
            $scope.availableJobs.unshift(messageObj)
        } else if (messageObj.message_type === 'location') {
            $scope.availableWards.unshift(messageObj)
        } else if (messageObj.message_type === 'channel') {
            $scope.shiftCreationData.channels.unshift(messageObj)
        }
        $scope.$apply(function() {})
    });

    $scope.refresh();

    Network.getAvailableChannels()
        .success(function(data) {
            $scope.shiftCreationData.channels = data
        });

    Network.getAvailableLocations()
        .success(function(data) {
            $scope.availableWards = data
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
        Network.createShift($scope.shiftCreationData)
            .success(function(data) {
                if (data.data) {
                    data = data.data
                }

                if ($scope.shiftCreationData.send_notification) {
                    $scope.sendOutNotifications(data, $scope.shiftCreationData.notification)
                }
            })
    }

}]);