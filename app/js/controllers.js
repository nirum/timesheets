'use strict';

/* Controllers */

function ProjectListCtrl($scope, $http, Project) {
	 $scope.metadata = Project.query();
}

function ProjectDetailCtrl($scope, $routeParams, Project) {
   $scope.name = $routeParams.projectname;
   $scope.timestamps = Project.get({
      name: 'projects/' + $routeParams.projectname
   })
}
