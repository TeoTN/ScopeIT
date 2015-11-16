(function(){
    'use strict';

    angular
        .module('scopeit.accounts.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http', '$q', '$cookies', 'apiUrl'];

    function Profile($http, $q, $cookies, apiUrl) {
        var current_profile = null;

        var Profile = {
            create: create,
            retrieve: retrieve,
            update: update,
            get_current: get_current
        };
        return Profile;

        function retrieve(username) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/',
                method: 'GET',
            };
            return $http(request);
        }

        function create(profile) {
            var request = {
                url: apiUrl + 'profiles/',
                method: 'POST',
                data: profile
            };
            return $http(request);
        }

        function update(username, profile) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/',
                method: 'PATCH',
                data: profile
            };
            return $http(request);
        }

        function get_current() {
            var deferred = $q.defer(),
                username = $cookies.get('username');
            if (current_profile) {
                deferred.resolve(current_profile);
            }
            else {
                retrieve(username)
                    .then(function (response) {
                        current_profile = response.data;
                        deferred.resolve(current_profile);
                    }, function (response) {
                        deferred.reject(response);
                    });
            }
            return deferred.promise;
        }
    }
})();