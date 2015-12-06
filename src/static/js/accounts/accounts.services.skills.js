(function(){
    'use strict';

    angular
        .module('scopeit.accounts.services')
        .factory('Skills', Skills);

    Skills.$inject = ['$http', 'apiUrl'];

    function Skills($http, apiUrl) {
        var base_url = 'skills/';
        var skill_levels = {
            '5': 'Expert',
            '4': 'Advanced',
            '3': 'Intermediate',
            '2': 'Beginner'
        };

        var Skills = {
            create: create,
            retrieve: retrieve,
            update: update,
            remove: remove,
            list: list,
            skill_levels: skill_levels
        };
        return Skills;

        function retrieve(pk) {
            var request = {
                url: apiUrl + base_url + pk + '/',
                method: 'GET',
            };
            return $http(request);
        }

        function list() {
            var request = {
                url: apiUrl + base_url,
                method: 'GET',
            };
            return $http(request);
        }

        function create(skill) {
            var request = {
                url: apiUrl + base_url,
                method: 'POST',
                data: skill
            };
            return $http(request);
        }

        function update(skill) {
            var request = {
                url: apiUrl + base_url + skill.pk + '/',
                method: 'PATCH',
                data: skill
            };
            return $http(request);
        }

        function remove(skill) {
            var request = {
                url: apiUrl + base_url + skill.pk + '/',
                method: 'DELETE',
            };
            return $http(request);
        }
    }
})();