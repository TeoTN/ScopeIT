(function(){
    'use strict';

    angular.module('scopeit.accounts.controllers')
        .controller('LoginFormController', LoginFormController)
        .controller('EntityController', EntityController)
        .controller('EntityListController', EntityListController);

    LoginFormController.$inject = ['$scope', '$window', 'Auth'];

    function LoginFormController($scope, $window, Auth) {
        var vm = this;
        $scope.user = {};

        vm.login = function(isValid) {
            if (!isValid) return;
            var username = $scope.user.username || "";
            var password = $scope.user.password || "";
            Auth
                .login(username, password)
                .then(function(response) {
                    $window.location.reload();
                }, function(response) {
                    console.log(response);
                    $scope.non_field_errors = response.data.non_field_errors;
                });
        };
    }

    EntityController.$inject = ['$scope', 'Entity'];

    function EntityController($scope, $entity) {

    }

    EntityListController.$inject = ['$scope', 'Auth', 'Entity'];

    function EntityListController($scope, $auth, $entity) {
        var username = $auth.get_username();
        $scope.entity_list = [];
        $entity
            .list(username)
            .then(function(response) {
                $scope.entity_list = response.data;
            });
    }
})();