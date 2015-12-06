(function(){
    'use strict';

    angular
        .module('scopeit.accounts.services')
        .factory('Match', Match);

    Match.$inject = ['$http', 'apiUrl'];

    function Match($http, apiUrl) {
        var Match = {
            retrieve: retrieve,
            list: list
        };
        return Match;

        //TODO
        function retrieve(username, entity_pk, pk) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/' + entity_pk + '/matches/',
                method: 'GET',
            };
            return $http(request);
        }

        function list(username, entity_pk) {
            var request = {
                url: apiUrl + 'profiles/' + username + '/entity/' + entity_pk + '/matches/',
                method: 'GET',
            };
            return $http(request);
        }
    }
})();