(function () {
    'use strict';

    angular
        .module('scopeit.common', [
            'ngRoute',
            'scopeit.common.controllers',
            'scopeit.common.directives',
            'scopeit.common.services'
        ])
        .config(['$routeProvider', '$locationProvider',
            function($routeProvider, $locationProvider) {
                $routeProvider
                    .when('/', {
                        templateUrl: '/static/fragments/welcomePage.html',
                        controller: 'WelcomePageController',
                        controllerAs: 'vm',
                        redirectAuth: '/profile/'
                    })
                    .when('/logout/', {
                        templateUrl: '/static/fragments/goodbyePage.html',
                        controller: 'LogoutController',
                        controllerAs: 'vm',
                        requireAuth: true
                    })
                    .when('/profile/', {
                        templateUrl: '/static/fragments/profile.html',
                        controller: 'ProfileController',
                        controllerAs: 'vm',
                        requireAuth: true
                    })
                    .when('/matches/', {
                        templateUrl: '/static/fragments/matchesPage.html',
                        requireAuth: true
                    })
                    .when('/signup/:is_employer', {
                        templateUrl: '/static/fragments/directives/signupForm.html',
                        controller: 'SignupFormController',
                        controllerAs: 'vm'
                    });

                $locationProvider.html5Mode(true);
            }])
        .run(function($rootScope, $cookies, $location) {
            $rootScope.$on( "$routeChangeStart", function(event, next, current) {
                var username = $cookies.get('username');
                if ( !username && next.requireAuth) {
                    $location.path('/');
                }
                if (username && next.redirectAuth) {
                    $location.path(next.redirectAuth);
                }
            });
        });

    angular
        .module('scopeit.common.controllers', []);

    angular
        .module('scopeit.common.directives', []);

    angular
        .module('scopeit.common.services', []);
})();