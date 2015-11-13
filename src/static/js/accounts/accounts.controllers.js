(function(){
    angular.module('scopeit.accounts.controllers')
        .controller('EntityController', EntityController)
        .controller('EntityListController', EntityListController);

    EntityController.$inject = ['$scope'];
    function EntityController($scope) {}

    EntityListController.$inject = ['$scope'];
    function EntityListController($scope) {}
})();