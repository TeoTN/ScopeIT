(function () {
    'use strict';

    angular
        .module('scopeit.accounts', [
            'scopeit.accounts.controllers',
            'scopeit.accounts.directives',
            'scopeit.accounts.services'
        ])
        .filter('my_matching', function() {
            return function(input) {
                return input.filter(function(e) {return e.type == 'mine' && e.user.username != null});
            };
        })
        .filter('theirs_matching', function() {
                return function(input) {
                return input.filter(function(e) {return e.type == 'theirs' && e.user.username != null});
            };
        });

    angular
        .module('scopeit.accounts.controllers', []);

    angular
        .module('scopeit.accounts.directives', []);

    angular
        .module('scopeit.accounts.services', []);
})();