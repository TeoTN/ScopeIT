(function(){
    var app = angular.module('ScopeIT');
    app.controller('UserProfileController', function($scope, $http) {
        function getProfileUrl() {
            var base = '/api/profiles/';
            var suffix = '/admin/professional/';
            var username = $()
        }

        var requestOptions = {
            url: getProfileUrl(),
            method: "GET",
        };
        var request = $http(requestOptions);
    });
})();
