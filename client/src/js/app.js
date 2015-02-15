angular.module('Client', [
  'ngRoute',
  'ngCookies',
  'moment',
  'mobile-angular-ui',
  'ui.calendar',
  'ui.bootstrap.datetimepicker',
  'socket.io',
  'ClientApp.services.Cordova',
  'ClientApp.services.NetworkData',
  'ClientApp.services.ActiveShift',
  'ClientApp.controllers.Main',
  'ClientApp.controllers.Management',
  'ClientApp.controllers.Calendar',
  'ClientApp.controllers.Devices',
  'ClientApp.controllers.Login',
  'ClientApp.controllers.UserData',
  'ClientApp.controllers.UserMessages',
  'ClientApp.controllers.Confirmation',
  'ClientApp.controllers.ForgotPassword'
])

.config(function($routeProvider) {
    $routeProvider.when('/', {redirectTo: '/login'});
    $routeProvider.when('/userdata', {templateUrl: 'userdata.html', reloadOnSearch: false, controller: 'UserDataController'});
    $routeProvider.when('/calendar', {templateUrl: 'calendar.html', reloadOnSearch: false, controller: 'CalendarController'});
    $routeProvider.when('/devices', {templateUrl: 'devices.html', reloadOnSearch: false, controller: 'DevicesController'});
    $routeProvider.when('/login', {templateUrl: 'login.html', reloadOnSearch: false, controller: 'LoginController'});
    $routeProvider.when('/help', {templateUrl: 'help.html', reloadOnSearch: false});
    $routeProvider.when('/confirmation', {templateUrl: 'confirmation.html', reloadOnSearch: false, controller: 'ConfirmationController'});
    $routeProvider.when('/management', {templateUrl: 'management.html', reloadOnSearch: false, controller: 'ManagementController'});
    $routeProvider.when('/forgotpassword', {templateUrl: 'forgotpassword.html', reloadOnSearch: false, controller: 'ForgotPasswordController'});
    $routeProvider.when('/usermessages', {templateUrl: 'usermessages.html', reloadOnSearch: false, controller: 'UserMessagesController'});
})

.run(function(Network, $rootScope, $location) {
    $rootScope.$on("$routeChangeStart", function(event, next, current) {

        if(!Network.loggedIn() && !(next.templateUrl == "login.html" || next.templateUrl == "forgotpassword.html")) {
            $location.path('/')
        }
    })
});