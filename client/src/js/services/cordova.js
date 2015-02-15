/**
 * Created by brettlarder on 22/12/2014.
 */
angular.module('ClientApp.services.Cordova', [])

    .factory('deviceReady', function(){
        return function(done) {
            if (typeof window.cordova === 'object') {
                document.addEventListener('deviceready', function () {
                    done();
                }, false);
            } else {
                done();
            }
        };
    });
