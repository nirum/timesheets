'use strict';

angular.module('tman', ['tmanServices']).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/projects', {templateUrl: 'partials/project-list.html',   controller: ProjectListCtrl}).
      when('/projects/:projectname', {templateUrl: 'partials/project-detail.html', controller: ProjectDetailCtrl}).
      otherwise({redirectTo: '/projects'});
}]);
/* App Module */
//angular.module('tman', ['tmanServices']).
//config(['$routeProvider', function($routeProvider) {
   //$routeProvider.
   //when('/tman', {
      //templateUrl: 'partials/projects.html',
      //controller: ProjectListCtrl
   //}).
   //when('/:name', {
      //templateUrl: 'partials/project-detail.html',
      //controller: ProjectDetailCtrl
   //}).
   //otherwise({
      //redirectTo: '/tman'
   //});
//}]);
