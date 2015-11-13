(function(){
    'use strict';

    angular
        .module('scopeit.accounts.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http', 'apiUrl'];

    function Profile($http, apiUrl) {
        var Profile = {
            create: create,
            retrieve: retrieve,
            update: update,
        };
        return Profile;

        function retrieve(username) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/',
                method: 'GET',
            };
            var response = $http(request);
            return response;
        }

        function create(profile) {
            var request = {
                url: apiUrl + 'profiles/',
                method: 'POST',
                data: profile
            };
            var response = $http(request);
            return response;
        }

        function update(username, profile) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/',
                method: 'PATCH',
                data: profile
            };
            var response = $http(request);
            return response;
        }
    }
})();