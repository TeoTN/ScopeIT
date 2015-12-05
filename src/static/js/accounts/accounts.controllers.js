(function(){
    'use strict';

    angular.module('scopeit.accounts.controllers')
        .controller('LoginFormController', LoginFormController)
        .controller('SignupFormController', SignupFormController)
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

    SignupFormController.$inject = ['$scope', '$routeParams', '$window', 'Auth'];

    function SignupFormController($scope, $routeParams, $window, Auth) {
        $scope.model = {
            'username': '',
            'password1': '',
            'password2': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_employer': $routeParams.is_employer=='True'?true:false
        };
        $scope.complete = false;
        $scope.errors = {
            'global': []
        };

        var errorAlias = {
            'minlength': 'This value is not long enough.',
            'maxlength': 'This value is too long.',
            'email': 'A properly formatted email address is required.',
            'required': 'This field is required.'
        };

        $scope.register = function(formData){
            if(!formData.$invalid) {
                Auth.register($scope.model)
                    .then(function(data){
                        // success case
                        $scope.complete = true;
                        $window.location.href = '/accounts/profile/'
                    },function(data){
                        // error case
                        $scope.errors=data;
                    });
            }
            else {
                for(var field in formData) {
                    if (field.substr(0, 1) == '$') continue;
                    for(var error in formData[field].$error){
                        if(formData[field].$error[error]){
                            if (!$scope.errors[field]) {
                                $scope.errors[field] = [];
                            }
                            if (errorAlias.hasOwnProperty(error)) {
                                $scope.errors[field].push(errorAlias[error]);
                            }
                            else {
                                $scope.errors.global.push(errorAlias[error]);
                            }
                        }
                    }
                }
            }
        }
    }

    EntityController.$inject = ['$scope', '$cookies', 'Entity', 'Skills'];

    function EntityController($scope, $cookies,  $entity, $skills) {
        var vm = this;
        var username = $cookies.get('username');
        vm.remove = function(entity) {
            $entity.remove(username, entity);
            entity.deleted = true;
        };
        vm.skill_levels = $skills.skill_levels;
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
            return $scope.is_employer || $scope.entity_list.length == 0;
        }
    }

    EntityFormController.$inject = ['$scope', '$cookies', '$window', 'Entity', 'Skills'];
    function EntityFormController($scope, $cookies, $window, $entity, $skills) {
        var vm = this;
        $scope.new_entity = {
            'skills': [],
        };
        $scope.new_skill = {};

        vm.submit = function(valid) {
            var username = $cookies.get('username');
            $entity
                .create(username, $scope.new_entity)
                .then(function(response) {
                    $window.location.reload();
                }, function(error) {
                    console.log(error);
                })
        };

        vm.add_skill = function() {
            if (!$scope.newEntity.$valid) return;
            $scope.new_entity.skills.push($scope.new_skill);
            $scope.new_skill = {};
        };

        vm.rm_skill = function(skill) {
            var index = $scope.new_entity.skills.indexOf(skill);
            if (index != -1) {
                $scope.new_entity.skills.splice(index, 1);
            }
        }

        vm.skill_types = {
            'LNG': 'Programming language',
            'FRW': 'Framework',
            'LIB': 'Library',
            'OS': 'Operating system',
            'TOOL': 'Tool / application',
            'TECH': 'Technology'
        };

        vm.skill_levels = $skills.skill_levels;

        $skills.list().then(function(response){
            $scope.skills = response;
        });
    }
})();