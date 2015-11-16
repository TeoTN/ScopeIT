(function(){
    'use strict';

    angular.module('scopeit.accounts.controllers')
        .controller('LoginFormController', LoginFormController)
        .controller('EntityController', EntityController)
        .controller('EntityListController', EntityListController)
        .controller('EntityFormController', EntityFormController);

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

    EntityController.$inject = ['$scope', '$cookies', 'Profile', 'Entity'];

    function EntityController($scope, $cookies, $profile, $entity) {
        var vm = this;
        var username = $cookies.get('username');
        vm.remove = function(entity) {
            $entity.remove(username, entity);
            entity.deleted = true;
        };
    }

    EntityListController.$inject = ['$scope', '$cookies', 'Profile', 'Entity'];

    function EntityListController($scope, $cookies, $profile, $entity) {
        var username = $cookies.get('username');

        $profile.get_current().then(function(profile) {
            $scope.is_employer = profile.is_employer;
        }, function(err) {
            console.error(err);
        });
        $scope.entity_list = [];
        $entity
            .list(username)
            .then(function(response) {
                $scope.entity_list = response.data;
            });

        $scope.can_add_entity = function() {
            return $scope.is_employer || $scope.entityList.length == 0;
        }
    }

    EntityFormController.$inject = ['$scope'];
    function EntityFormController($scope) {}
})();