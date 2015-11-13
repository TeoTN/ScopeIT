(function(){
    'use strict';

    angular.module('scopeit.accounts.directives')
        .directive('entity', entity)
        .directive('entityList', entityList);

        function entity() {
            var directive = {
                restrict: 'E',
                controller: 'EntityController',
                controllerAs: 'vm',
                templateUrl: '/static/fragments/directives/entity.html'
            };
            return directive;
        }

        function entityList() {
            var directive = {
                restrict: 'E',
                controller: 'EntityListController',
                controllerAs: 'vm',
                templateUrl: '/static/fragments/directives/entityList.html'
            };
            return directive;
        }
})();