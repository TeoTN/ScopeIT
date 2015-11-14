(function(){
    'use strict';

    angular
        .module('scopeit.accounts.services')
        .factory('Entity', Entity);

    Entity.$inject = ['$http', 'apiUrl'];

    function Entity($http, apiUrl) {
        var Entity = {
            create: create,
            retrieve: retrieve,
            update: update,
            list: list
        };
        return Entity;

        function retrieve(username, pk) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/' + pk,
                method: 'GET',
            };
            return $http(request);
        }

        function list(username) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/',
                method: 'GET',
            };
            return $http(request);
        }

        function create(username, entity) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/',
                method: 'POST',
                data: entity
            };
            return $http(request);
        }

        function update(username, pk, entity) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/' + pk,
                method: 'PATCH',
                data: entity
            };
            return $http(request);
        }
    }
})();