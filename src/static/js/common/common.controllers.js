(function(){
    'use strict';

    angular.module('scopeit.common.controllers')
        .controller('WelcomePageController', WelcomePageController)
        .controller('NavbarController', NavbarController);

    function WelcomePageController() {}

    NavbarController.$inject = ['$scope', '$rootScope', '$cookies'];

    function NavbarController($scope, $rootScope, $cookies) {
        $scope.authenticated = $cookies.get('username');
        $scope.friendlyName = getFriendlyName($scope.authenticated);
        $scope.hideLoginForm = false;

        $scope.$on('AuthChanged', function(event, data) {
            $scope.authenticated = $cookies.get('username');
            $scope.friendlyName = getFriendlyName($scope.authenticated);
            $scope.hideLoginForm = data;
        });

        function getFriendlyName(username) {
            return username;
        }
    }
})();