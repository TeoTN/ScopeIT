(function(){
    'use strict';

    angular.module('scopeit.common.directives')
        .directive('navbar', navbar)

    function navbar() {
        return {
            restrict: 'E',
            controller: 'NavbarController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/navbar.html'
        };
    }
})();