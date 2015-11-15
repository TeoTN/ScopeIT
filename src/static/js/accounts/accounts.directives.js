(function(){
    'use strict';

    angular.module('scopeit.accounts.directives')
        .directive('loginForm', loginForm)
        .directive('entity', entity)
        .directive('entityList', entityList);

        function loginForm() {
            return {
                restrict: 'E',
                controller: 'LoginFormController',
                controllerAs: 'vm',
                templateUrl: '/static/fragments/directives/loginForm.html'
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
})();