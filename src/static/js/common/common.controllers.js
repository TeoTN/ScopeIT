(function(){
    'use strict';

    angular.module('scopeit.common.controllers')
        .controller('WelcomePageController', WelcomePageController)
        .controller('NavbarController', NavbarController)
        .controller('MatchesNetworkController', MatchesNetworkController);

    function WelcomePageController() {}

    NavbarController.$inject = ['$scope', '$rootScope', '$cookies'];

    function NavbarController($scope, $rootScope, $cookies) {
        $scope.authenticated = $cookies.get('username');
        $scope.friendlyName = getFriendlyName($scope.authenticated);
        $scope.hideLoginForm = false;

        $scope.$on('AuthChanged', function(event, data) {
            $scope.authenticated = $cookies.get('username');
            $scope.friendlyName = getFriendlyName($scope.authenticated);
            $scope.hideLoginForm = data;
        });

        function getFriendlyName(username) {
            return username;
        }
    }

    MatchesNetworkController.$inject = ['$http', '$q'];

    function MatchesNetworkController($http, $q) {
        function getNodes() {
            return $http
                .get('/api/v1/profiles/')
                .then(function(response) {
                    var users = [];
                    for (var i in response.data) {
                        users.push({id: response.data[i].user_pk, label: response.data[i].user});
                    }
                    return users;
                });
        }

        function getEdges() {
            return $http
                .get('/api/v1/network/')
                .then(function(response) {
                    return response.data;
                });
        }

        function renderNetwork(args) {
            var nodes = new vis.DataSet(args[0]);
            var edges = new vis.DataSet(args[1]);
            var container = document.getElementById('mynetwork');
            var data = {
                nodes: nodes,
                edges: edges
            };
            var options = {};

            // initialize your network!
            var network = new vis.Network(container, data, options);
        }

        $q.all([getNodes(), getEdges()]).then(renderNetwork);
    }
})();