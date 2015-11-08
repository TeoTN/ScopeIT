(function(){
    var app = angular.module('ScopeIT');
    app.directive("userProfile", function(){
        return {
            restrict: 'E',
            templateUrl: '/accounts/user-profile/',
            controller: 'UserProfileController',
            controllerAs: 'profile'
        };
    });


    app.directive("userProfileList", function(){
        return {
            restrict: 'E',
            templateUrl: '/accounts/user-profile-list/',
            controller: 'UserProfileListController',
            controllerAs: 'profilelist'
        };
    });


    app.directive("profileForm", function(){
        return {
            restrict: 'E',
            templateUrl: '/accounts/profile-form/',
        };
    });
})();