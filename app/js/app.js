'use strict';

/* App Module */

angular.module('tman', ['tmanServices', 'tmanFilters', 'firebase']).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/chat', {templateUrl: 'partials/chat.html',   controller: ChatCtrl}).
      when('/projects', {templateUrl: 'partials/project-list.html',   controller: ProjectListCtrl}).
      when('/projects/:projectname', {templateUrl: 'partials/project-detail.html', controller: ProjectDetailCtrl}).
      otherwise({redirectTo: '/projects'});
}]);
