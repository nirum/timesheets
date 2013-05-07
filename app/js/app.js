'use strict';

/* App Module */

angular.module('tman', ['tmanServices', 'tmanFilters', 'firebase']).
config(['$routeProvider', function($routeProvider) {
   $routeProvider.
   when('/', {
      templateUrl: 'partials/home.html',
      controller: UserCtrl
   }).
   when('/chat', {
      templateUrl: 'partials/chat.html',
      controller: ChatCtrl
   }).
   when('/firebase', {
      templateUrl: 'partials/tman.html',
      controller: TmanCtrl
   }).
   when('/projects', {
      templateUrl: 'partials/project-list.html',
      controller: ProjectListCtrl
   }).
   when('/projects/:projectname', {
      templateUrl: 'partials/project-detail.html',
      controller: ProjectDetailCtrl
   }).
   otherwise({
      redirectTo: '/'
   });
}]);
