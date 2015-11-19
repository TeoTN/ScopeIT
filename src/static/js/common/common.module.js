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
                        templateUrl: '/static/fragments/directives/welcomePage.html',
                        controller: 'WelcomePageController',
                        controllerAs: 'vm'
                    })
                    .when('/signup/:is_employer', {
                        templateUrl: '/static/fragments/directives/signupForm.html',
                        controller: 'SignupFormController',
                        controllerAs: 'vm'
                    });

                $locationProvider.html5Mode(true);
            }]);

    angular
        .module('scopeit.common.controllers', []);

    angular
        .module('scopeit.common.directives', []);

    angular
        .module('scopeit.common.services', []);
})();