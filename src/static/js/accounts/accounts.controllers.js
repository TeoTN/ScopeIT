(function(){
    angular.module('scopeit.accounts.controllers')
        .controller('EntityController', EntityController)
        .controller('EntityListController', EntityListController);

    EntityController.$inject = ['$scope', 'Entity'];
    function EntityController($scope, $entity) {

    }

    EntityListController.$inject = ['$scope', 'Entity'];
    function EntityListController($scope, $entity) {
        $entity.list();
    }
})();