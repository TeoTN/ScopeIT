(function(){
    'use strict';

    angular.module('scopeit.accounts.services')
        .factory('Auth', Auth);

    Auth.$inject = ['$http', '$cookies', '$rootScope', 'apiUrl'];

    function Auth($http, $cookies, $rootScope, apiUrl) {
        var Auth = {
            http_request: http_request(),
            register: register,
            login: login,
            logout: logout
        };

        return Auth;

        var use_session = true,
            authenticated = null,
            authPromise = null;

        function http_request(request) {
            if($cookies.token) {
                $http.defaults.headers.common.Authorization = 'Token ' + $cookies.token;
            }
            request = request || {};
            var url = apiUrl + args.url,
                method = request.method || "GET",
                data = request.data || {};

            var request_promise = $http({
                url: url,
                withCredentials: use_session,
                method: method.toUpperCase(),
                headers: {
                    'X-CSRFToken': $cookies['csrftoken']
                },
                data: data
            }).catch(request_error_callback);
        }

        function register(user_data) {
            return http_request({
                method: "POST",
                url: "/registration/",
                data: user_data
            });
        }

        function login(username, password) {
            return http_request({
                method: 'POST',
                url: '/login/',
                data: {
                    username: username,
                    password: password
                }
            }).then(function(data) {
                if (!use_session) {
                    $http.defaults.headers.common.Authorization = 'Token ' + data.key;
                    $cookies.token = data.key;
                }
                authenticated = true;
                $rootScope.$broadcast("Auth.logged_in", data);
            });
        }

        function logout() {
            return http_request({
                method: 'POST',
                url: '/logout/'
            }).then(function(data){
                delete $http.defaults.headers.common.Authorization;
                delete $cookies.token;
                authenticated = false;
                $rootScope.$broadcast("Auth.logged_out");
            });
        }

        function request_error_callback(response) {
            console.error("[ERROR] Unable to authenticate user.");
            console.error(response);
        }
    }
})();