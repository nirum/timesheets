'use strict';

/* Controllers */

function ProjectListCtrl($scope, Project) {
   $scope.metadata = Project.query();
}

function ProjectDetailCtrl($scope, $routeParams, Project) {
   $scope.name = $routeParams.projectname;
   $scope.timestamps = Project.get({
      name: 'projects/' + $routeParams.projectname
   })
}

function TmanCtrl($scope, $timeout, angularFireCollection) {
   var url = 'https://tman.firebaseio.com/projects';
   $scope.projects = angularFireCollection(url);
   $scope.projectname = "";
   $scope.addTime = function() {
			var now = new Date().getTime();
      $scope.projects.add({
         project: $scope.projectname,
         timestamp: now
      });
      $scope.projectname = "";
   }
}

function ChatCtrl($scope, $timeout, angularFireCollection) {
   $scope.header = "Chat";
   var url = 'https://tman.firebaseio.com/chat';
   $scope.messages = angularFireCollection(url);
   $scope.username = 'Guest' + Math.floor(Math.random() * 101);
   $scope.addMessage = function() {
      $scope.messages.add({
         from: $scope.username,
         content: $scope.message
      });
      $scope.message = "";
   }
}
