(function(){
    var app = angular.module('ScopeIT');
    app.directive("userProfile", function(){
        return {
            restrict: 'EA',
            templateUrl: '/accounts/'
        };
    });
})();