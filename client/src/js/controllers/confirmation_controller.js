/**
 * Created by brettlarder on 23/12/2014.
 */
angular.module('ClientApp.controllers.Confirmation', ['ClientApp.services.ActiveShift'])

.controller('ConfirmationController', ['Shift', '$location', '$scope', function(Shift, $location, $scope) {
        $scope.shift = Shift.getActiveShift();
        if ($scope.shift.cancelled) {
            $scope.titleText = "Shift Cancellation"
        } else {
            $scope.titleText = "Now Awaiting Approval..."
        }
        $scope.addShiftToCalendar = function() {

            //TODO: correct this -- an error doesn't seem to be raised when a shift is not found, as assumed
            var success = function(message) {alert("Successfully added event")};
            var error = function(message) {alert("Could not add event - does app have permission?")};

            var eventAlreadyInCalendar = function() {
                alert("Event already in calendar")
            };

            //var addEventToCalendar = function() {
            //    window.plugins.calendar.createEvent("Bank Shift", shift.ward.name, shift.detail, shift.start.toDate(),
            //        shift.end.toDate(), success, error)
            //};

            var shift = $scope.shift;
            //window.plugins.calendar.findEvent("Bank Shift", shift.ward.name, shift.detail, shift.start.toDate(),
            //    shift.end.toDate(), eventAlreadyInCalendar, addEventToCalendar);
            window.plugins.calendar.createEvent("Bank Shift", shift.ward.name, shift.detail, shift.start.toDate(),
                shift.end.toDate(), success, error)
        };

        $scope.done = function() {
            $location.path('/calendar')
        }

    }]);