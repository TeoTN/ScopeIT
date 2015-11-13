(function() {
    'use strict';
    angular.module('scopeit', [
        'scopeit.config',
        'scopeit.common',
        'scopeit.accounts'
    ])
    .run(run).
    constant('apiUrl', '/api/v1/');

    run.$inject = ['$http'];

    /**
     * @name run
     * @desc Update xsrf $http headers to align with Django's defaults
     */
    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    };

    angular.module('scopeit.config', []);
})();