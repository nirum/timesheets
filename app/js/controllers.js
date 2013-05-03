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
