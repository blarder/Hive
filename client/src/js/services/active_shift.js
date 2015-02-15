/**
 * Created by brettlarder on 23/12/2014.
 */
angular.module('ClientApp.services.ActiveShift', [])

.factory('Shift', function() {
        var _shift = {};
        var _updateActive = function(shiftData) {
            for (var att in shiftData) {
                if (shiftData.hasOwnProperty(att)) {
                    _shift[att] = shiftData[att]
                }
            }
        };

        return {
            getActiveShift: function() {return _shift},
            updateActive: _updateActive
        }


    });