(function(){
    'use strict';

    angular.module('scopeit.accounts.directives')
        .directive('loginForm', loginForm)
        .directive('signupForm', signupForm)
        .directive('entity', entity)
        .directive('entityList', entityList)
        .directive('entityForm', entityForm)
        .directive('matchList', matchList);


    function loginForm() {
        return {
            restrict: 'E',
            controller: 'LoginFormController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/loginForm.html'
        };
    }

    function signupForm() {
        return {
            restrict: 'EA',
            controller: 'SignUpFormController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/signupForm.html'
        };
    }

    function entity() {
        return {
            restrict: 'E',
            controller: 'EntityController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/entity.html'
        };
    }

    function entityList() {
        return {
            restrict: 'E',
            controller: 'EntityListController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/entityList.html'
        };
    }

    function entityForm() {
        return {
            restrict: 'E',
            controller: 'EntityFormController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/entityForm.html'
        };
    }

    function matchList() {
        return {
            restrict: 'E',
            controller: 'MatchListController',
            controllerAs: 'vm',
            templateUrl: '/static/fragments/directives/matchList.html'
        };
    }
})();