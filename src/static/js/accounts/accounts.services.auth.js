(function(){
    'use strict';

    angular.module('scopeit.accounts.services')
        .factory('Auth', Auth);

    Auth.$inject = ['$http', '$cookies', '$rootScope', 'apiUrl'];

    function Auth($http, $cookies, $rootScope, apiUrl) {
        var use_session = true,
            auth_url = apiUrl + 'rest-auth/',
            username = null;

        var Auth = {
            http_request: http_request,
            register: register,
            login: login,
            logout: logout,
            get_username: get_username
        };
        return Auth;



        function http_request(request) {
            if($cookies.token) {
                $http.defaults.headers.common.Authorization = 'Token ' + $cookies.token;
            }
            request = request || {};
            var url = auth_url + request.url,
                method = request.method || "GET",
                data = request.data || {};

            return $http({
                url: url,
                withCredentials: use_session,
                method: method.toUpperCase(),
                headers: {
                    'X-CSRFToken': $cookies['csrftoken']
                },
                data: data
            });
        }

        function register(user_data) {
            return http_request({
                method: "POST",
                url: "registration/",
                data: user_data
            });
        }

        function login(username, password) {
            return http_request({
                method: 'POST',
                url: 'login/',
                data: {
                    username: username,
                    password: password
                }
            }).then(function(data) {
                if (!use_session) {
                    $http.defaults.headers.common.Authorization = 'Token ' + data.key;
                    $cookies.token = data.key;
                }
                username = data.config.username;
                return data;
            });
        }

        function logout() {
            return http_request({
                method: 'POST',
                url: 'logout/'
            }).then(function(data){
                delete $http.defaults.headers.common.Authorization;
                delete $cookies.token;
                username = null;
                return data;
            });
        }

        function get_username() {
            return username;
        }
    }
})();