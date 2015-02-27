angular.module('ClientApp.controllers.Calendar', ['ClientApp.services.NetworkData', 'ClientApp.services.ActiveShift'])

.controller('CalendarController', ['$scope', '$location', 'Network', 'Shift', function($scope, $location, Network, Shift){
    var self = this;

    self.availableShifts = {};

    $scope.eventSources = [];
    $scope.shiftSelected = false;
    $scope.shift = Shift.getActiveShift();
    $scope.buttonTexts = {};

    $scope.nextButtonText = "Next Month";
    $scope.prevButtonText = "Previous Month";

    $scope.showModal = function() {
        $scope.showmodal = true
    };

    $scope.hideModal = function() {
        $scope.showmodal = false
    };

    $scope.nextMonth = function() {
        $scope.nextButtonText = "Loading...";
        $scope.shiftCalendar.fullCalendar('next');
        $scope.nextButtonText = "Next Month"
    };

    $scope.prevMonth = function() {
        $scope.prevButtonText = "Loading...";
        $scope.shiftCalendar.fullCalendar('prev');
        $scope.prevButtonText = "Previous Month"
    };

    self.eventClicked = function(event, allDay, jsEvent, view) {
        Shift.updateActive(event);
        $scope.showModal()
    };

    self.refresh = function() {
        $scope.eventSources.length = 0;
        Network.forceReload();
        self.getAvailableShifts();
    };

    $scope.refresh = self.refresh;

    self.parseEvents = function(eventsArray) {
        for (var i = 0, len = eventsArray.length; i != len; i++) {
            eventsArray[i].allDay = false;
            eventsArray[i].title = eventsArray[i].location.name;
        }
    };

    self.getAvailableShifts = function () {
        Network.getAvailableShifts().then(function(data) {
            self.availableShifts = {color: "red", events: []};
            self.parseEvents(data);
            for (var i = 0, len = data.length; i != len; i++) {
                self.availableShifts.events.push(data[i]);
                $scope.buttonTexts[data[i].id] = 'Accept this shift';
            }
            $scope.eventSources.push(self.availableShifts)
        });
    };

    $scope.calendarConfig = {
        calendar:{
            height: "auto",
            editable: false,
            header:{
                left: 'title',
                center: '',
                right: ''
            },
            eventClick: self.eventClicked
        }
    };

    $scope.$on('pushNotificationReceived', function(event) {
        self.refresh();
        $scope.$apply(function() {})
    });

    self.getAvailableShifts();

}]);

//TODO: Test new push notification refresh event